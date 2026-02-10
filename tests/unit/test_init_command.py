"""Tests for claude_agent_skills.init_command module."""

import json

import pytest

from claude_agent_skills.init_command import run_init, INSTRUCTION_CONTENT, MCP_CONFIG, SKILL_STUBS


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

    def test_does_not_create_settings_json(self, target_dir):
        target_dir.mkdir()
        run_init(str(target_dir))

        settings_path = target_dir / ".claude" / "settings.json"
        assert not settings_path.exists()

    def test_installs_skill_stubs(self, target_dir):
        target_dir.mkdir()
        run_init(str(target_dir))

        skills_dir = target_dir / ".claude" / "skills"
        for filename, content in SKILL_STUBS.items():
            stub = skills_dir / filename
            assert stub.exists(), f"Missing stub: {filename}"
            assert stub.read_text(encoding="utf-8") == content

    def test_skill_stubs_reference_mcp(self):
        for filename, content in SKILL_STUBS.items():
            assert "get_skill_definition" in content, (
                f"Stub {filename} should reference get_skill_definition"
            )

    def test_skill_stubs_idempotent(self, target_dir):
        target_dir.mkdir()
        run_init(str(target_dir))
        run_init(str(target_dir))

        skills_dir = target_dir / ".claude" / "skills"
        for filename in SKILL_STUBS:
            assert (skills_dir / filename).exists()

    def test_instruction_content_has_tool_reference(self):
        assert "get_se_overview" in INSTRUCTION_CONTENT
        assert "create_sprint" in INSTRUCTION_CONTENT
        assert "get_activity_guide" in INSTRUCTION_CONTENT
