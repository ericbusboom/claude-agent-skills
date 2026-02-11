"""Tests for claude_agent_skills.mcp_server module."""

from claude_agent_skills.mcp_server import server, content_path


class TestContentPath:
    def test_resolves_agents_directory(self):
        assert content_path("agents").is_dir()

    def test_resolves_skills_directory(self):
        assert content_path("skills").is_dir()

    def test_resolves_instructions_directory(self):
        assert content_path("instructions").is_dir()

    def test_resolves_nested_path(self):
        assert content_path("instructions", "languages").is_dir()

    def test_resolves_specific_file(self):
        assert content_path("agents", "project-manager.md").is_file()


class TestServer:
    def test_server_instance_exists(self):
        assert server is not None
        assert server.name == "clasi"
