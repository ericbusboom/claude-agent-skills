"""Unit tests for gh CLI helpers and list_github_issues MCP tool."""

import json
import subprocess
from unittest.mock import patch

import pytest

from clasi.tools.artifact_tools import (
    _check_gh_access,
    close_github_issue,
    list_github_issues,
)


class TestCheckGhAccess:
    """Tests for _check_gh_access helper."""

    @patch("clasi.tools.artifact_tools.subprocess.run")
    def test_success_returns_true_and_repo(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout='[{"number":1}]',
        )
        ok, result = _check_gh_access("owner/repo")
        assert ok is True
        assert result == "owner/repo"
        mock_run.assert_called_once_with(
            ["gh", "issue", "list", "--repo", "owner/repo",
             "--limit", "1", "--json", "number"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("clasi.tools.artifact_tools.subprocess.run")
    def test_auth_failure_returns_false(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(
            1, "gh", stderr="auth required",
        )
        ok, result = _check_gh_access("owner/repo")
        assert ok is False
        assert "Cannot access issues for owner/repo" in result
        assert "gh auth login" in result

    @patch("clasi.tools.artifact_tools.subprocess.run")
    def test_missing_gh_binary_returns_false(self, mock_run):
        mock_run.side_effect = FileNotFoundError("No such file or directory: 'gh'")
        ok, result = _check_gh_access("owner/repo")
        assert ok is False
        assert "gh CLI not found" in result
        assert "https://cli.github.com/" in result

    @patch("clasi.tools.artifact_tools._get_github_repo")
    def test_no_repo_returns_false(self, mock_get_repo):
        mock_get_repo.return_value = None
        ok, result = _check_gh_access(None)
        assert ok is False
        assert "Could not determine repository" in result

    @patch("clasi.tools.artifact_tools._get_github_repo")
    @patch("clasi.tools.artifact_tools.subprocess.run")
    def test_resolves_repo_when_none(self, mock_run, mock_get_repo):
        mock_get_repo.return_value = "auto/detected"
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="[]",
        )
        ok, result = _check_gh_access(None)
        assert ok is True
        assert result == "auto/detected"
        mock_get_repo.assert_called_once()


class TestListGithubIssues:
    """Tests for list_github_issues MCP tool."""

    @patch("clasi.tools.artifact_tools.subprocess.run")
    @patch("clasi.tools.artifact_tools._check_gh_access")
    def test_success_returns_json(self, mock_check, mock_run, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        mock_check.return_value = (True, "owner/repo")
        issues = [
            {"number": 1, "title": "Bug", "body": "desc",
             "labels": [], "url": "https://github.com/owner/repo/issues/1"},
            {"number": 2, "title": "Feature", "body": "desc2",
             "labels": [{"name": "enhancement"}],
             "url": "https://github.com/owner/repo/issues/2"},
        ]
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=json.dumps(issues),
        )
        result = json.loads(list_github_issues(repo="owner/repo"))
        assert len(result) == 2
        assert result[0]["number"] == 1
        assert result[1]["title"] == "Feature"

    @patch("clasi.tools.artifact_tools.subprocess.run")
    @patch("clasi.tools.artifact_tools._check_gh_access")
    def test_with_labels_adds_flag(self, mock_check, mock_run, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        mock_check.return_value = (True, "owner/repo")
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="[]",
        )
        list_github_issues(repo="owner/repo", labels="bug,enhancement")
        cmd = mock_run.call_args[0][0]
        assert "--label" in cmd
        label_idx = cmd.index("--label")
        assert cmd[label_idx + 1] == "bug,enhancement"

    @patch("clasi.tools.artifact_tools._check_gh_access")
    def test_access_failure_returns_error(self, mock_check, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        mock_check.return_value = (False, "Cannot access issues for owner/repo. Run `gh auth login` or check `gh auth status`.")
        result = json.loads(list_github_issues(repo="owner/repo"))
        assert "error" in result
        assert "Cannot access issues" in result["error"]

    def test_pytest_env_returns_empty_list(self, monkeypatch):
        monkeypatch.setenv("PYTEST_CURRENT_TEST", "tests/unit/test_gh_import.py::test")
        result = json.loads(list_github_issues(repo="owner/repo"))
        assert result == []

    @patch("clasi.tools.artifact_tools.subprocess.run")
    @patch("clasi.tools.artifact_tools._check_gh_access")
    def test_without_labels_omits_flag(self, mock_check, mock_run, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        mock_check.return_value = (True, "owner/repo")
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="[]",
        )
        list_github_issues(repo="owner/repo")
        cmd = mock_run.call_args[0][0]
        assert "--label" not in cmd

    @patch("clasi.tools.artifact_tools.subprocess.run")
    @patch("clasi.tools.artifact_tools._check_gh_access")
    def test_custom_state_and_limit(self, mock_check, mock_run, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        mock_check.return_value = (True, "owner/repo")
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="[]",
        )
        list_github_issues(repo="owner/repo", state="closed", limit=10)
        cmd = mock_run.call_args[0][0]
        assert "--state" in cmd
        state_idx = cmd.index("--state")
        assert cmd[state_idx + 1] == "closed"
        assert "--limit" in cmd
        limit_idx = cmd.index("--limit")
        assert cmd[limit_idx + 1] == "10"

    @patch("clasi.tools.artifact_tools.subprocess.run")
    @patch("clasi.tools.artifact_tools._check_gh_access")
    def test_subprocess_failure_returns_error(self, mock_check, mock_run, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        mock_check.return_value = (True, "owner/repo")
        mock_run.side_effect = subprocess.CalledProcessError(
            1, "gh", stderr="something went wrong",
        )
        result = json.loads(list_github_issues(repo="owner/repo"))
        assert "error" in result
        assert "gh issue list failed" in result["error"]


class TestCloseGithubIssue:
    """Tests for close_github_issue MCP tool."""

    @patch("clasi.tools.artifact_tools.subprocess.run")
    @patch("clasi.tools.artifact_tools._check_gh_access")
    def test_close_success(self, mock_check, mock_run, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        mock_check.return_value = (True, "owner/repo")
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr="",
        )
        result = json.loads(close_github_issue(issue_number=42, repo="owner/repo"))
        assert result["issue_number"] == 42
        assert result["repo"] == "owner/repo"
        assert result["closed"] is True
        assert "error" not in result
        mock_run.assert_called_once_with(
            ["gh", "issue", "close", "42", "--repo", "owner/repo"],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_close_invalid_issue_number_zero(self):
        result = json.loads(close_github_issue(issue_number=0, repo="owner/repo"))
        assert result["closed"] is False
        assert "positive integer" in result["error"]

    def test_close_invalid_issue_number_negative(self):
        result = json.loads(close_github_issue(issue_number=-5, repo="owner/repo"))
        assert result["closed"] is False
        assert "positive integer" in result["error"]

    @patch("clasi.tools.artifact_tools._check_gh_access")
    def test_close_access_failure(self, mock_check, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        mock_check.return_value = (False, "Cannot access issues for owner/repo. Run `gh auth login` or check `gh auth status`.")
        result = json.loads(close_github_issue(issue_number=1, repo="owner/repo"))
        assert result["closed"] is False
        assert "Cannot access issues" in result["error"]

    @patch("clasi.tools.artifact_tools.subprocess.run")
    @patch("clasi.tools.artifact_tools._check_gh_access")
    def test_close_subprocess_failure(self, mock_check, mock_run, monkeypatch):
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        mock_check.return_value = (True, "owner/repo")
        mock_run.side_effect = subprocess.CalledProcessError(
            1, "gh", stderr="issue not found",
        )
        result = json.loads(close_github_issue(issue_number=999, repo="owner/repo"))
        assert result["issue_number"] == 999
        assert result["closed"] is False
        assert "issue not found" in result["error"]

    def test_pytest_env_returns_mock_success(self, monkeypatch):
        monkeypatch.setenv("PYTEST_CURRENT_TEST", "tests/unit/test_gh_import.py::test")
        result = json.loads(close_github_issue(issue_number=10, repo="owner/repo"))
        assert result["issue_number"] == 10
        assert result["repo"] == "owner/repo"
        assert result["closed"] is True
