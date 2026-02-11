"""Smoke tests for MCP content access.

Verifies that the packaged content (agents, skills, instructions) is
accessible through the MCP tool functions and content_path resolver.
"""

import json

from claude_agent_skills.mcp_server import content_path
from claude_agent_skills.process_tools import (
    list_agents,
    list_skills,
    list_instructions,
    get_agent_definition,
    get_instruction,
    get_skill_definition,
)


class TestContentSmoke:
    def test_agents_directory_has_md_files(self):
        agents_dir = content_path("agents")
        md_files = list(agents_dir.glob("*.md"))
        assert len(md_files) > 0, "No .md files in agents directory"

    def test_list_agents_returns_content(self):
        result = json.loads(list_agents())
        assert isinstance(result, list)
        assert len(result) > 0
        assert all("name" in a and "description" in a for a in result)

    def test_list_skills_returns_content(self):
        result = json.loads(list_skills())
        assert isinstance(result, list)
        assert len(result) > 0
        assert all("name" in s and "description" in s for s in result)

    def test_list_instructions_returns_content(self):
        result = json.loads(list_instructions())
        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_agent_returns_markdown(self):
        content = get_agent_definition("project-manager")
        assert "# " in content
        assert len(content) > 100

    def test_get_instruction_returns_markdown(self):
        content = get_instruction("coding-standards")
        assert "# " in content
        assert len(content) > 100

    def test_get_skill_returns_markdown(self):
        content = get_skill_definition("execute-ticket")
        assert "# " in content
        assert len(content) > 100
