"""Unit tests for claude_agent_skills.versioning module."""

from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from claude_agent_skills.versioning import (
    VERSION_PATTERN,
    compute_next_version,
    update_pyproject_version,
    create_version_tag,
)


def _mock_today(year, month, day):
    """Create a mock date.today() that returns a proper date object."""
    real_date = date(year, month, day)
    mock_date = MagicMock()
    mock_date.today.return_value = real_date
    return mock_date


class TestVersionPattern:
    def test_matches_valid_version(self):
        assert VERSION_PATTERN.match("0.20260210.1")
        assert VERSION_PATTERN.match("1.20260210.42")

    def test_matches_with_v_prefix(self):
        assert VERSION_PATTERN.match("v0.20260210.1")

    def test_rejects_invalid(self):
        assert not VERSION_PATTERN.match("0.1.0")
        assert not VERSION_PATTERN.match("abc")
        assert not VERSION_PATTERN.match("0.2026021.1")  # 7 digits


class TestComputeNextVersion:
    @patch("claude_agent_skills.versioning._get_existing_tags")
    @patch("claude_agent_skills.versioning.date", _mock_today(2026, 2, 10))
    def test_first_version_of_day(self, mock_tags):
        mock_tags.return_value = []
        assert compute_next_version() == "0.20260210.1"

    @patch("claude_agent_skills.versioning._get_existing_tags")
    @patch("claude_agent_skills.versioning.date", _mock_today(2026, 2, 10))
    def test_increments_build(self, mock_tags):
        mock_tags.return_value = ["v0.20260210.1", "v0.20260210.2"]
        assert compute_next_version() == "0.20260210.3"

    @patch("claude_agent_skills.versioning._get_existing_tags")
    @patch("claude_agent_skills.versioning.date", _mock_today(2026, 2, 11))
    def test_resets_on_new_date(self, mock_tags):
        mock_tags.return_value = ["v0.20260210.5"]
        assert compute_next_version() == "0.20260211.1"

    @patch("claude_agent_skills.versioning._get_existing_tags")
    @patch("claude_agent_skills.versioning.date", _mock_today(2026, 2, 10))
    def test_respects_major(self, mock_tags):
        mock_tags.return_value = ["v0.20260210.3", "v1.20260210.1"]
        assert compute_next_version(major=1) == "1.20260210.2"

    @patch("claude_agent_skills.versioning._get_existing_tags")
    @patch("claude_agent_skills.versioning.date", _mock_today(2026, 2, 10))
    def test_ignores_non_matching_tags(self, mock_tags):
        mock_tags.return_value = ["release-1.0", "v0.2.0", "v0.20260210.1"]
        assert compute_next_version() == "0.20260210.2"


class TestUpdatePyprojectVersion:
    def test_updates_version(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[project]\nname = "test"\nversion = "0.2.0"\n')

        update_pyproject_version("0.20260210.1", pyproject)

        content = pyproject.read_text()
        assert 'version = "0.20260210.1"' in content
        assert 'name = "test"' in content

    def test_raises_on_missing_version(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[project]\nname = "test"\n')

        with pytest.raises(ValueError, match="Could not find version"):
            update_pyproject_version("0.20260210.1", pyproject)


class TestCreateVersionTag:
    @patch("claude_agent_skills.versioning.subprocess")
    def test_creates_tag(self, mock_subprocess):
        mock_subprocess.run.return_value.returncode = 0

        create_version_tag("0.20260210.1")

        mock_subprocess.run.assert_called_once_with(
            ["git", "tag", "v0.20260210.1"],
            capture_output=True,
            text=True,
            check=False,
        )

    @patch("claude_agent_skills.versioning.subprocess")
    def test_raises_on_failure(self, mock_subprocess):
        mock_subprocess.run.return_value.returncode = 1
        mock_subprocess.run.return_value.stderr = "tag already exists"

        with pytest.raises(RuntimeError, match="Failed to create tag"):
            create_version_tag("0.20260210.1")
