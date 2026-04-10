"""Tests for the plan_to_todo module."""

import time
from pathlib import Path

import pytest

from clasi.plan_to_todo import plan_to_todo


def _make_plan_file(plans_dir: Path, name: str = "my-plan.md", content: str = "# My Plan\n\nSome content.") -> Path:
    plans_dir.mkdir(parents=True, exist_ok=True)
    p = plans_dir / name
    p.write_text(content, encoding="utf-8")
    return p


class TestPlanToTodoBasic:
    def test_no_debug_block_in_output(self, tmp_path):
        """Output TODO should not contain any debug block."""
        plans_dir = tmp_path / "plans"
        todo_dir = tmp_path / "todo"
        _make_plan_file(plans_dir)

        result = plan_to_todo(plans_dir, todo_dir)

        assert result is not None
        content = result.read_text(encoding="utf-8")
        assert "Hook Debug Info" not in content

    def test_returns_none_when_plans_dir_missing(self, tmp_path):
        """Returns None when the plans directory does not exist."""
        plans_dir = tmp_path / "nonexistent"
        todo_dir = tmp_path / "todo"

        result = plan_to_todo(plans_dir, todo_dir)

        assert result is None


class TestPlanToTodoPlanFileParam:
    def test_uses_plan_file_when_provided(self, tmp_path):
        """When plan_file is provided, that specific file is used regardless of mtime."""
        plans_dir = tmp_path / "plans"
        plans_dir.mkdir(parents=True)
        todo_dir = tmp_path / "todo"

        older = plans_dir / "older-plan.md"
        older.write_text("# Older Plan\n\nOlder content.", encoding="utf-8")
        # Ensure newer has a later mtime
        time.sleep(0.01)
        newer = plans_dir / "newer-plan.md"
        newer.write_text("# Newer Plan\n\nNewer content.", encoding="utf-8")

        result = plan_to_todo(plans_dir, todo_dir, plan_file=older)

        assert result is not None
        content = result.read_text(encoding="utf-8")
        assert "Older Plan" in content
        assert "Newer Plan" not in content

    def test_plan_file_is_deleted_after_conversion(self, tmp_path):
        """The specific plan_file is deleted after conversion."""
        plans_dir = tmp_path / "plans"
        plans_dir.mkdir(parents=True)
        todo_dir = tmp_path / "todo"

        plan = plans_dir / "specific.md"
        plan.write_text("# Specific Plan\n\nContent.", encoding="utf-8")

        result = plan_to_todo(plans_dir, todo_dir, plan_file=plan)

        assert result is not None
        assert not plan.exists()

    def test_returns_none_when_plan_file_missing(self, tmp_path):
        """Returns None when plan_file points to a non-existent file."""
        plans_dir = tmp_path / "plans"
        plans_dir.mkdir(parents=True)
        todo_dir = tmp_path / "todo"
        nonexistent = tmp_path / "ghost.md"

        result = plan_to_todo(plans_dir, todo_dir, plan_file=nonexistent)

        assert result is None

    def test_falls_back_to_mtime_when_plan_file_none(self, tmp_path):
        """When plan_file=None, the newest file in plans_dir is used."""
        plans_dir = tmp_path / "plans"
        plans_dir.mkdir(parents=True)
        todo_dir = tmp_path / "todo"

        older = plans_dir / "alpha.md"
        older.write_text("# Alpha Plan\n\nOlder.", encoding="utf-8")
        time.sleep(0.01)
        newer = plans_dir / "beta.md"
        newer.write_text("# Beta Plan\n\nNewer.", encoding="utf-8")

        result = plan_to_todo(plans_dir, todo_dir, plan_file=None)

        assert result is not None
        content = result.read_text(encoding="utf-8")
        assert "Beta Plan" in content
        assert "Alpha Plan" not in content

    def test_plan_file_ignores_plans_dir_when_provided(self, tmp_path):
        """When plan_file is outside plans_dir, it is still converted correctly."""
        plans_dir = tmp_path / "plans"
        plans_dir.mkdir(parents=True)
        todo_dir = tmp_path / "todo"

        outside = tmp_path / "external-plan.md"
        outside.write_text("# External Plan\n\nContent from outside.", encoding="utf-8")

        result = plan_to_todo(plans_dir, todo_dir, plan_file=outside)

        assert result is not None
        content = result.read_text(encoding="utf-8")
        assert "External Plan" in content
        assert not outside.exists()
