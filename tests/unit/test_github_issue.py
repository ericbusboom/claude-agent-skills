"""Unit tests for GitHub issue creation MCP tool."""

import json
import subprocess
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from claude_agent_skills.artifact_tools import (
    _create_github_issue_api,
    _get_github_repo,
    _get_github_token,
    create_github_issue,
)


class TestCreateGitHubIssueMetadataFallback:
    """Tests for the metadata fallback path (no token / during tests)."""

    def test_returns_metadata_with_title_and_body(self):
        result = json.loads(create_github_issue(
            title="Add authentication",
            body="Need to implement OAuth2 authentication",
        ))
        assert result["tool"] == "create_github_issue"
        assert result["title"] == "Add authentication"
        assert result["body"] == "Need to implement OAuth2 authentication"
        assert result["labels"] == []
        assert "note" in result

    def test_returns_metadata_with_labels(self):
        result = json.loads(create_github_issue(
            title="Fix bug",
            body="Bug description",
            labels=["bug", "high-priority"],
        ))
        assert result["labels"] == ["bug", "high-priority"]

    def test_returns_metadata_without_labels(self):
        result = json.loads(create_github_issue(
            title="Feature request",
            body="New feature description",
        ))
        assert result["labels"] == []

    def test_includes_usage_note(self):
        result = json.loads(create_github_issue(
            title="Test",
            body="Test body",
        ))
        assert "note" in result
        assert "GitHub MCP" in result["note"]

    def test_note_mentions_disabled_during_tests(self):
        result = json.loads(create_github_issue(
            title="Test",
            body="Body",
        ))
        assert "disabled during tests" in result["note"]


class TestGetGitHubToken:
    def test_returns_github_token(self, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "ghp_abc123")
        monkeypatch.delenv("GH_TOKEN", raising=False)
        assert _get_github_token() == "ghp_abc123"

    def test_returns_gh_token_fallback(self, monkeypatch):
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        monkeypatch.setenv("GH_TOKEN", "ghp_xyz789")
        assert _get_github_token() == "ghp_xyz789"

    def test_prefers_github_token_over_gh_token(self, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "ghp_first")
        monkeypatch.setenv("GH_TOKEN", "ghp_second")
        assert _get_github_token() == "ghp_first"

    def test_returns_none_when_no_token(self, monkeypatch):
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        monkeypatch.delenv("GH_TOKEN", raising=False)
        assert _get_github_token() is None

    def test_strips_whitespace(self, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "  ghp_trimmed  ")
        assert _get_github_token() == "ghp_trimmed"

    def test_empty_string_returns_none(self, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "")
        monkeypatch.delenv("GH_TOKEN", raising=False)
        assert _get_github_token() is None


class TestGetGitHubRepo:
    def test_returns_env_var(self, monkeypatch):
        monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
        assert _get_github_repo() == "owner/repo"

    def test_strips_env_var(self, monkeypatch):
        monkeypatch.setenv("GITHUB_REPOSITORY", "  owner/repo  ")
        assert _get_github_repo() == "owner/repo"

    @patch("claude_agent_skills.artifact_tools.subprocess.run")
    def test_parses_https_remote(self, mock_run, monkeypatch):
        monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0,
            stdout="https://github.com/owner/repo.git\n",
        )
        assert _get_github_repo() == "owner/repo"

    @patch("claude_agent_skills.artifact_tools.subprocess.run")
    def test_parses_ssh_remote(self, mock_run, monkeypatch):
        monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0,
            stdout="git@github.com:owner/repo.git\n",
        )
        assert _get_github_repo() == "owner/repo"

    @patch("claude_agent_skills.artifact_tools.subprocess.run")
    def test_returns_none_for_non_github_remote(self, mock_run, monkeypatch):
        monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0,
            stdout="https://gitlab.com/owner/repo.git\n",
        )
        assert _get_github_repo() is None

    @patch("claude_agent_skills.artifact_tools.subprocess.run")
    def test_returns_none_on_git_failure(self, mock_run, monkeypatch):
        monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
        mock_run.side_effect = subprocess.CalledProcessError(1, "git")
        assert _get_github_repo() is None

    @patch("claude_agent_skills.artifact_tools.subprocess.run")
    def test_returns_none_on_empty_remote(self, mock_run, monkeypatch):
        monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="",
        )
        assert _get_github_repo() is None


class TestCreateGitHubIssueApi:
    @patch("claude_agent_skills.artifact_tools.urllib.request.urlopen")
    def test_success_returns_parsed_json(self, mock_urlopen):
        response_body = json.dumps({
            "number": 42,
            "html_url": "https://github.com/owner/repo/issues/42",
            "title": "Test issue",
        }).encode("utf-8")
        mock_response = MagicMock()
        mock_response.read.return_value = response_body
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = _create_github_issue_api(
            repo="owner/repo",
            title="Test issue",
            body="Test body",
            labels=["bug"],
            token="ghp_test",
        )
        assert result["number"] == 42
        assert result["title"] == "Test issue"

    @patch("claude_agent_skills.artifact_tools.urllib.request.urlopen")
    def test_http_error_raises_runtime_error(self, mock_urlopen):
        error = urllib.error.HTTPError(
            url="https://api.github.com/repos/owner/repo/issues",
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=None,
        )
        mock_urlopen.side_effect = error

        with pytest.raises(RuntimeError, match="GitHub API error 401"):
            _create_github_issue_api(
                repo="owner/repo",
                title="Test",
                body="Body",
                labels=[],
                token="ghp_bad",
            )

    @patch("claude_agent_skills.artifact_tools.urllib.request.urlopen")
    def test_sends_correct_headers(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"number": 1}'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        _create_github_issue_api(
            repo="owner/repo",
            title="T",
            body="B",
            labels=[],
            token="ghp_tok",
        )

        request = mock_urlopen.call_args[0][0]
        assert request.get_header("Authorization") == "Bearer ghp_tok"
        assert request.get_header("Accept") == "application/vnd.github+json"
        assert request.get_header("Content-type") == "application/json"

    @patch("claude_agent_skills.artifact_tools.urllib.request.urlopen")
    def test_includes_labels_in_payload(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"number": 1}'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        _create_github_issue_api(
            repo="owner/repo",
            title="T",
            body="B",
            labels=["bug", "p1"],
            token="ghp_tok",
        )

        request = mock_urlopen.call_args[0][0]
        payload = json.loads(request.data)
        assert payload["labels"] == ["bug", "p1"]

    @patch("claude_agent_skills.artifact_tools.urllib.request.urlopen")
    def test_omits_labels_when_empty(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"number": 1}'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        _create_github_issue_api(
            repo="owner/repo",
            title="T",
            body="B",
            labels=[],
            token="ghp_tok",
        )

        request = mock_urlopen.call_args[0][0]
        payload = json.loads(request.data)
        assert "labels" not in payload
