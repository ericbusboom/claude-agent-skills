"""Unit tests for TODO management MCP tools."""

import json

import pytest

from claude_agent_skills.artifact_tools import list_todos, move_todo_to_done


@pytest.fixture
def todo_dir(tmp_path, monkeypatch):
    """Set up a temporary working directory with docs/plans/todo/."""
    monkeypatch.chdir(tmp_path)
    todo = tmp_path / "docs" / "plans" / "todo"
    todo.mkdir(parents=True)
    return todo


class TestListTodos:
    def test_lists_todos(self, todo_dir):
        (todo_dir / "idea-one.md").write_text("# Idea One\n\nSome details.\n")
        (todo_dir / "idea-two.md").write_text("# Idea Two\n\nMore details.\n")

        result = json.loads(list_todos())
        assert len(result) == 2
        assert result[0] == {"filename": "idea-one.md", "title": "Idea One"}
        assert result[1] == {"filename": "idea-two.md", "title": "Idea Two"}

    def test_excludes_done_directory(self, todo_dir):
        (todo_dir / "active.md").write_text("# Active\n")
        done = todo_dir / "done"
        done.mkdir()
        (done / "finished.md").write_text("# Finished\n")

        result = json.loads(list_todos())
        assert len(result) == 1
        assert result[0]["filename"] == "active.md"

    def test_empty_directory(self, todo_dir):
        result = json.loads(list_todos())
        assert result == []

    def test_no_todo_directory(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = json.loads(list_todos())
        assert result == []

    def test_file_without_heading(self, todo_dir):
        (todo_dir / "no-heading.md").write_text("Just some text.\n")

        result = json.loads(list_todos())
        assert len(result) == 1
        assert result[0]["title"] == "no-heading"


class TestMoveTodoToDone:
    def test_moves_file(self, todo_dir):
        (todo_dir / "idea.md").write_text("# Idea\n")

        result = json.loads(move_todo_to_done("idea.md"))
        assert not (todo_dir / "idea.md").exists()
        assert (todo_dir / "done" / "idea.md").exists()
        assert result["new_path"].endswith("done/idea.md")

    def test_creates_done_directory(self, todo_dir):
        (todo_dir / "idea.md").write_text("# Idea\n")
        assert not (todo_dir / "done").exists()

        move_todo_to_done("idea.md")
        assert (todo_dir / "done").is_dir()

    def test_error_on_nonexistent(self, todo_dir):
        with pytest.raises(ValueError, match="TODO not found"):
            move_todo_to_done("nonexistent.md")

    def test_writes_traceability_frontmatter(self, todo_dir):
        (todo_dir / "idea.md").write_text("# Idea\n\nDetails.\n")

        move_todo_to_done("idea.md", sprint_id="005", ticket_ids=["001", "002"])

        content = (todo_dir / "done" / "idea.md").read_text()
        assert "status: done" in content
        assert 'sprint: "005"' in content or "sprint: '005'" in content
        assert "001" in content
        assert "002" in content

    def test_writes_status_done_without_sprint(self, todo_dir):
        (todo_dir / "idea.md").write_text("# Idea\n")

        move_todo_to_done("idea.md")

        content = (todo_dir / "done" / "idea.md").read_text()
        assert "status: done" in content

    def test_preserves_existing_frontmatter(self, todo_dir):
        (todo_dir / "idea.md").write_text(
            "---\nstatus: pending\n---\n\n# Idea\n"
        )

        move_todo_to_done("idea.md", sprint_id="005")

        content = (todo_dir / "done" / "idea.md").read_text()
        assert "status: done" in content
        assert 'sprint: "005"' in content or "sprint: '005'" in content
