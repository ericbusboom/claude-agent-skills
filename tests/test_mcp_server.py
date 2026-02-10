"""Tests for claude_agent_skills.mcp_server module."""

from claude_agent_skills.mcp_server import server, get_repo_root


class TestGetRepoRoot:
    def test_finds_repo_root(self):
        root = get_repo_root()
        assert (root / "agents").is_dir()
        assert (root / "skills").is_dir()
        assert (root / "instructions").is_dir()


class TestServer:
    def test_server_instance_exists(self):
        assert server is not None
        assert server.name == "clasi"
