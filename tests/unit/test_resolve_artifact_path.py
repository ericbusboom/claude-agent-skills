"""Unit tests for resolve_artifact_path."""

from pathlib import Path

import pytest

from claude_agent_skills.artifact_tools import resolve_artifact_path


class TestResolveArtifactPath:
    def test_finds_file_at_original_location(self, tmp_path):
        f = tmp_path / "tickets" / "001-foo.md"
        f.parent.mkdir(parents=True)
        f.write_text("hello")

        assert resolve_artifact_path(str(f)) == f

    def test_finds_file_in_done_subdirectory(self, tmp_path):
        done_file = tmp_path / "tickets" / "done" / "001-foo.md"
        done_file.parent.mkdir(parents=True)
        done_file.write_text("hello")

        # Ask for the original (non-done) path
        original = tmp_path / "tickets" / "001-foo.md"
        assert resolve_artifact_path(str(original)) == done_file

    def test_finds_file_when_path_contains_done_but_file_moved_back(self, tmp_path):
        # File was moved out of done/ back to parent
        f = tmp_path / "tickets" / "001-foo.md"
        f.parent.mkdir(parents=True)
        f.write_text("hello")

        # Ask for the done/ path
        done_path = tmp_path / "tickets" / "done" / "001-foo.md"
        assert resolve_artifact_path(str(done_path)) == f

    def test_handles_path_already_in_done(self, tmp_path):
        done_file = tmp_path / "tickets" / "done" / "001-foo.md"
        done_file.parent.mkdir(parents=True)
        done_file.write_text("hello")

        # Ask for the done/ path directly — should find it as-is
        assert resolve_artifact_path(str(done_file)) == done_file

    def test_raises_file_not_found_error(self, tmp_path):
        missing = tmp_path / "tickets" / "nonexistent.md"
        with pytest.raises(FileNotFoundError, match="Artifact not found"):
            resolve_artifact_path(str(missing))

    def test_error_message_includes_path(self, tmp_path):
        missing = tmp_path / "tickets" / "nonexistent.md"
        with pytest.raises(FileNotFoundError, match="nonexistent.md"):
            resolve_artifact_path(str(missing))
