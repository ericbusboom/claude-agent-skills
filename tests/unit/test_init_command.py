"""Tests for claude_agent_skills.init_command module."""

import json

import pytest

from claude_agent_skills.init_command import (
    run_init, INSTRUCTION_CONTENT, MCP_CONFIG, SKILL_STUBS, SETTINGS_PERMISSIONS,
)


@pytest.fixture
def target_dir(tmp_path):
    """Return a temp directory to use as init target."""
    return tmp_path / "target_repo"


class TestRunInit:
    def test_creates_instruction_files(self, target_dir):
        target_dir.mkdir()
        run_init(str(target_dir))

        claude_rules = target_dir / ".claude" / "rules" / "clasi-se-process.md"
        copilot_inst = (
            target_dir / ".github" / "copilot" / "instructions" / "clasi-se-process.md"
        )

        assert claude_rules.exists()
        assert copilot_inst.exists()
        assert claude_rules.read_text(encoding="utf-8") == INSTRUCTION_CONTENT
        assert copilot_inst.read_text(encoding="utf-8") == INSTRUCTION_CONTENT

    def test_creates_mcp_json(self, target_dir):
        target_dir.mkdir()
        run_init(str(target_dir))

        mcp_json = target_dir / ".mcp.json"
        assert mcp_json.exists()

        data = json.loads(mcp_json.read_text(encoding="utf-8"))
        assert data["mcpServers"]["clasi"] == MCP_CONFIG["clasi"]

    def test_idempotent(self, target_dir):
        target_dir.mkdir()
        run_init(str(target_dir))
        run_init(str(target_dir))

        mcp_json = target_dir / ".mcp.json"
        data = json.loads(mcp_json.read_text(encoding="utf-8"))
        assert data["mcpServers"]["clasi"] == MCP_CONFIG["clasi"]

        claude_rules = target_dir / ".claude" / "rules" / "clasi-se-process.md"
        assert claude_rules.read_text(encoding="utf-8") == INSTRUCTION_CONTENT

    def test_merges_existing_mcp_json(self, target_dir):
        target_dir.mkdir()
        mcp_json = target_dir / ".mcp.json"
        existing = {"mcpServers": {"other": {"command": "other"}}}
        mcp_json.write_text(json.dumps(existing), encoding="utf-8")

        run_init(str(target_dir))

        data = json.loads(mcp_json.read_text(encoding="utf-8"))
        assert data["mcpServers"]["other"] == {"command": "other"}
        assert data["mcpServers"]["clasi"] == MCP_CONFIG["clasi"]

    def test_creates_settings_local_json(self, target_dir):
        target_dir.mkdir()
        run_init(str(target_dir))

        settings_path = target_dir / ".claude" / "settings.local.json"
        assert settings_path.exists()
        data = json.loads(settings_path.read_text(encoding="utf-8"))
        assert "mcp__clasi__*" in data["permissions"]["allow"]

    def test_settings_idempotent(self, target_dir):
        target_dir.mkdir()
        run_init(str(target_dir))
        run_init(str(target_dir))

        settings_path = target_dir / ".claude" / "settings.local.json"
        data = json.loads(settings_path.read_text(encoding="utf-8"))
        assert data["permissions"]["allow"].count("mcp__clasi__*") == 1

    def test_settings_merges_existing(self, target_dir):
        target_dir.mkdir()
        settings_path = target_dir / ".claude" / "settings.local.json"
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        existing = {"permissions": {"allow": ["Bash(*)"]}}
        settings_path.write_text(json.dumps(existing), encoding="utf-8")

        run_init(str(target_dir))

        data = json.loads(settings_path.read_text(encoding="utf-8"))
        assert "Bash(*)" in data["permissions"]["allow"]
        assert "mcp__clasi__*" in data["permissions"]["allow"]

    def test_installs_skill_stubs(self, target_dir):
        target_dir.mkdir()
        run_init(str(target_dir))

        skills_dir = target_dir / ".claude" / "skills"
        for name, content in SKILL_STUBS.items():
            stub = skills_dir / name / "SKILL.md"
            assert stub.exists(), f"Missing stub: {name}/SKILL.md"
            assert stub.read_text(encoding="utf-8") == content

    def test_skill_stubs_reference_mcp(self):
        for name, content in SKILL_STUBS.items():
            assert "get_skill_definition" in content, (
                f"Stub {name} should reference get_skill_definition"
            )

    def test_skill_stubs_idempotent(self, target_dir):
        target_dir.mkdir()
        run_init(str(target_dir))
        run_init(str(target_dir))

        skills_dir = target_dir / ".claude" / "skills"
        for name in SKILL_STUBS:
            assert (skills_dir / name / "SKILL.md").exists()

    def test_instruction_content_has_tool_reference(self):
        assert "get_se_overview" in INSTRUCTION_CONTENT
        assert "create_sprint" in INSTRUCTION_CONTENT
        assert "get_activity_guide" in INSTRUCTION_CONTENT
        assert "create_overview" in INSTRUCTION_CONTENT

    def test_instruction_content_no_deprecated_tools(self):
        assert "create_brief" not in INSTRUCTION_CONTENT
        assert "create_technical_plan" not in INSTRUCTION_CONTENT
        assert "create_use_cases" not in INSTRUCTION_CONTENT
