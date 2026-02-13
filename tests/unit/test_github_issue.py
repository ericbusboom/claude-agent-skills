"""Unit tests for GitHub issue creation MCP tool."""

import json

import pytest

from claude_agent_skills.artifact_tools import create_github_issue


class TestCreateGitHubIssue:
    def test_creates_issue_with_title_and_body(self):
        result = json.loads(create_github_issue(
            title="Add authentication",
            body="Need to implement OAuth2 authentication"
        ))
        
        assert result["tool"] == "create_github_issue"
        assert result["title"] == "Add authentication"
        assert result["body"] == "Need to implement OAuth2 authentication"
        assert result["labels"] == []
        assert "note" in result

    def test_creates_issue_with_labels(self):
        result = json.loads(create_github_issue(
            title="Fix bug",
            body="Bug description",
            labels=["bug", "high-priority"]
        ))
        
        assert result["labels"] == ["bug", "high-priority"]

    def test_creates_issue_without_labels(self):
        result = json.loads(create_github_issue(
            title="Feature request",
            body="New feature description"
        ))
        
        assert result["labels"] == []

    def test_includes_usage_note(self):
        result = json.loads(create_github_issue(
            title="Test",
            body="Test body"
        ))
        
        assert "note" in result
        assert "GitHub MCP" in result["note"]
