"""Tests for claude_agent_skills.init_command module."""

import json

import pytest

from claude_agent_skills.init_command import run_init, INSTRUCTION_CONTENT, MCP_CONFIG


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

    def test_creates_mcp_settings(self, target_dir):
        target_dir.mkdir()
        run_init(str(target_dir))

        settings_path = target_dir / ".claude" / "settings.json"
        assert settings_path.exists()

        data = json.loads(settings_path.read_text(encoding="utf-8"))
        assert data["mcpServers"]["clasi"] == MCP_CONFIG["clasi"]

    def test_idempotent(self, target_dir):
        target_dir.mkdir()
        run_init(str(target_dir))
        run_init(str(target_dir))

        settings_path = target_dir / ".claude" / "settings.json"
        data = json.loads(settings_path.read_text(encoding="utf-8"))
        assert data["mcpServers"]["clasi"] == MCP_CONFIG["clasi"]

        claude_rules = target_dir / ".claude" / "rules" / "clasi-se-process.md"
        assert claude_rules.read_text(encoding="utf-8") == INSTRUCTION_CONTENT

    def test_merges_existing_settings(self, target_dir):
        target_dir.mkdir()
        settings_path = target_dir / ".claude" / "settings.json"
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        existing = {"existingKey": "value", "mcpServers": {"other": {"command": "other"}}}
        settings_path.write_text(json.dumps(existing), encoding="utf-8")

        run_init(str(target_dir))

        data = json.loads(settings_path.read_text(encoding="utf-8"))
        assert data["existingKey"] == "value"
        assert data["mcpServers"]["other"] == {"command": "other"}
        assert data["mcpServers"]["clasi"] == MCP_CONFIG["clasi"]

    def test_global_config(self, target_dir, tmp_path, monkeypatch):
        target_dir.mkdir()
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: fake_home)

        run_init(str(target_dir), global_config=True)

        global_settings = fake_home / ".claude" / "settings.json"
        assert global_settings.exists()
        data = json.loads(global_settings.read_text(encoding="utf-8"))
        assert data["mcpServers"]["clasi"] == MCP_CONFIG["clasi"]

    def test_instruction_content_has_tool_reference(self):
        assert "get_se_overview" in INSTRUCTION_CONTENT
        assert "create_sprint" in INSTRUCTION_CONTENT
        assert "get_activity_guide" in INSTRUCTION_CONTENT
