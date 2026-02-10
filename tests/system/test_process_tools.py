"""Tests for claude_agent_skills.process_tools module."""

import json

import pytest

from claude_agent_skills.process_tools import (
    _list_definitions,
    _get_definition,
    get_se_overview,
    list_agents,
    list_skills,
    list_instructions,
    get_agent_definition,
    get_skill_definition,
    get_instruction,
    get_activity_guide,
    list_language_instructions,
    get_language_instruction,
    ACTIVITY_GUIDES,
)
from claude_agent_skills.mcp_server import get_repo_root


class TestListDefinitions:
    def test_lists_agents(self):
        root = get_repo_root()
        results = _list_definitions(root / "agents")
        names = [r["name"] for r in results]
        assert "project-manager" in names
        assert "python-expert" in names
        assert all(r["description"] for r in results)

    def test_empty_dir(self, tmp_path):
        results = _list_definitions(tmp_path / "nonexistent")
        assert results == []


class TestGetDefinition:
    def test_gets_agent(self):
        root = get_repo_root()
        content = _get_definition(root / "agents", "project-manager")
        assert "Project Manager" in content

    def test_not_found(self):
        root = get_repo_root()
        with pytest.raises(ValueError, match="not found"):
            _get_definition(root / "agents", "nonexistent-agent")


class TestMCPTools:
    def test_get_se_overview(self):
        result = get_se_overview()
        assert "CLASI SE Process Overview" in result
        assert "project-manager" in result
        assert "execute-ticket" in result

    def test_list_agents(self):
        result = json.loads(list_agents())
        assert isinstance(result, list)
        assert any(a["name"] == "project-manager" for a in result)

    def test_list_skills(self):
        result = json.loads(list_skills())
        assert isinstance(result, list)
        assert any(s["name"] == "execute-ticket" for s in result)

    def test_list_instructions(self):
        result = json.loads(list_instructions())
        assert isinstance(result, list)
        assert any(i["name"] == "system-engineering" for i in result)

    def test_get_agent_definition(self):
        result = get_agent_definition("project-manager")
        assert "Project Manager" in result

    def test_get_skill_definition(self):
        result = get_skill_definition("execute-ticket")
        assert "Execute Ticket" in result

    def test_get_instruction(self):
        result = get_instruction("system-engineering")
        assert "System Engineering" in result


class TestLanguageInstructions:
    def test_list_language_instructions(self):
        result = json.loads(list_language_instructions())
        assert isinstance(result, list)
        assert any(lang["name"] == "python" for lang in result)
        python_entry = next(l for l in result if l["name"] == "python")
        assert python_entry["description"]

    def test_get_language_instruction_python(self):
        result = get_language_instruction("python")
        assert "Python Language Instructions" in result
        assert "Virtual Environments" in result
        assert "uv" in result
        assert "pyproject.toml" in result
        assert "Type Hints" in result
        assert "pytest" in result

    def test_get_language_instruction_not_found(self):
        with pytest.raises(ValueError, match="not found"):
            get_language_instruction("nonexistent-language")


class TestActivityGuide:
    def test_all_activities_valid(self):
        for activity in ACTIVITY_GUIDES:
            result = get_activity_guide(activity)
            assert f"Activity Guide: {activity}" in result

    def test_unknown_activity(self):
        with pytest.raises(ValueError, match="Unknown activity"):
            get_activity_guide("nonexistent")

    def test_implementation_guide_contains_all_sections(self):
        result = get_activity_guide("implementation")
        assert "Agent: python-expert" in result
        assert "Skill: execute-ticket" in result
        assert "Instruction: coding-standards" in result
        assert "Instruction: testing" in result
