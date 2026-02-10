"""Tests for the TODO file splitting logic."""

import pytest

from claude_agent_skills.todo_split import split_todo_files, _parse_sections


class TestParseSections:
    """Unit tests for _parse_sections."""

    def test_single_heading(self):
        content = "# One Heading\n\nSome content.\n"
        sections = _parse_sections(content)
        assert len(sections) == 1
        assert sections[0][0] == "# One Heading"

    def test_multiple_headings(self):
        content = "# First\n\nBody 1.\n\n# Second\n\nBody 2.\n"
        sections = _parse_sections(content)
        assert len(sections) == 2
        assert sections[0][0] == "# First"
        assert sections[1][0] == "# Second"
        assert "Body 1." in sections[0][1]
        assert "Body 2." in sections[1][1]

    def test_preamble_prepended_to_first(self):
        content = "Some preamble text.\n\n# First\n\nBody.\n"
        sections = _parse_sections(content)
        assert len(sections) == 1
        assert "preamble" in sections[0][1]
        assert "Body." in sections[0][1]

    def test_no_headings(self):
        content = "Just some text without headings.\n"
        sections = _parse_sections(content)
        assert len(sections) == 0

    def test_empty_sections(self):
        content = "# First\n# Second\n"
        sections = _parse_sections(content)
        assert len(sections) == 2

    def test_h2_not_treated_as_split(self):
        content = "# Main\n\n## Sub\n\nContent.\n"
        sections = _parse_sections(content)
        assert len(sections) == 1
        assert "## Sub" in sections[0][1]


class TestSplitTodoFiles:
    """Integration tests for split_todo_files."""

    def test_splits_multi_heading_file(self, tmp_path):
        todo_dir = tmp_path / "todo"
        todo_dir.mkdir()
        multi = todo_dir / "ideas.md"
        multi.write_text("# Idea One\n\nFirst idea.\n\n# Idea Two\n\nSecond idea.\n")

        actions = split_todo_files(todo_dir)

        assert not multi.exists(), "Original file should be deleted"
        assert (todo_dir / "idea-one.md").exists()
        assert (todo_dir / "idea-two.md").exists()
        assert "# Idea One" in (todo_dir / "idea-one.md").read_text()
        assert len(actions) == 3  # 2 created + 1 deleted

    def test_leaves_single_heading_alone(self, tmp_path):
        todo_dir = tmp_path / "todo"
        todo_dir.mkdir()
        single = todo_dir / "one-thing.md"
        single.write_text("# Single Idea\n\nContent.\n")

        actions = split_todo_files(todo_dir)

        assert single.exists(), "Single-heading file should not be touched"
        assert len(actions) == 0

    def test_leaves_no_heading_alone(self, tmp_path):
        todo_dir = tmp_path / "todo"
        todo_dir.mkdir()
        bare = todo_dir / "notes.md"
        bare.write_text("Just some notes without headings.\n")

        actions = split_todo_files(todo_dir)

        assert bare.exists()
        assert len(actions) == 0

    def test_preserves_preamble(self, tmp_path):
        todo_dir = tmp_path / "todo"
        todo_dir.mkdir()
        f = todo_dir / "mixed.md"
        f.write_text("Preamble text.\n\n# First\n\nBody.\n\n# Second\n\nMore.\n")

        split_todo_files(todo_dir)

        content = (todo_dir / "first.md").read_text()
        assert "Preamble text." in content
        assert "Body." in content

    def test_handles_heading_collision(self, tmp_path):
        todo_dir = tmp_path / "todo"
        todo_dir.mkdir()
        # Create existing file that would collide
        (todo_dir / "idea.md").write_text("# Existing\n\nAlready here.\n")
        # Create multi-heading file with a heading that collides
        multi = todo_dir / "batch.md"
        multi.write_text("# Idea\n\nFirst.\n\n# Other\n\nSecond.\n")

        split_todo_files(todo_dir)

        assert (todo_dir / "idea.md").exists()  # original untouched
        assert (todo_dir / "idea-2.md").exists()  # collision resolved
        assert (todo_dir / "other.md").exists()

    def test_nonexistent_dir(self, tmp_path):
        actions = split_todo_files(tmp_path / "nonexistent")
        assert actions == []

    def test_ignores_done_subdir(self, tmp_path):
        todo_dir = tmp_path / "todo"
        todo_dir.mkdir()
        done_dir = todo_dir / "done"
        done_dir.mkdir()
        # File in done/ should not be processed
        done_file = done_dir / "old.md"
        done_file.write_text("# Old\n\nArchived.\n\n# Ancient\n\nVery old.\n")

        actions = split_todo_files(todo_dir)

        assert done_file.exists(), "Files in done/ should not be touched"
        assert len(actions) == 0

    def test_empty_section_still_creates_file(self, tmp_path):
        todo_dir = tmp_path / "todo"
        todo_dir.mkdir()
        f = todo_dir / "sparse.md"
        f.write_text("# Has Content\n\nSome text.\n\n# Empty\n")

        split_todo_files(todo_dir)

        empty_file = todo_dir / "empty.md"
        assert empty_file.exists()
        content = empty_file.read_text()
        assert "# Empty" in content
