"""Tests for claude_agent_skills.artifact_tools module."""

import json
import os

import pytest

from claude_agent_skills.artifact_tools import (
    create_sprint,
    create_ticket,
    insert_sprint,
    list_sprints,
    list_tickets,
    get_sprint_status,
    update_ticket_status,
    move_ticket_to_done,
    close_sprint,
)
from claude_agent_skills.frontmatter import read_frontmatter
from claude_agent_skills.state_db import (
    advance_phase,
    record_gate,
)


@pytest.fixture
def work_dir(tmp_path, monkeypatch):
    """Set up a temporary working directory with docs/plans/sprints/ structure."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _advance_to_ticketing(work_dir, sprint_id: str) -> None:
    """Advance a sprint through review gates to ticketing phase for testing."""
    db_path = work_dir / "docs" / "plans" / ".clasi.db"
    advance_phase(db_path, sprint_id)  # planning-docs → architecture-review
    record_gate(db_path, sprint_id, "architecture_review", "passed")
    advance_phase(db_path, sprint_id)  # architecture-review → stakeholder-review
    record_gate(db_path, sprint_id, "stakeholder_approval", "passed")
    advance_phase(db_path, sprint_id)  # stakeholder-review → ticketing


class TestCreateSprint:
    def test_creates_directory_structure(self, work_dir):
        result = json.loads(create_sprint("Test Sprint"))
        sprint_dir = work_dir / "docs" / "plans" / "sprints" / "001-test-sprint"
        assert sprint_dir.is_dir()
        assert (sprint_dir / "sprint.md").exists()
        assert not (sprint_dir / "brief.md").exists()
        assert (sprint_dir / "usecases.md").exists()
        assert (sprint_dir / "technical-plan.md").exists()
        assert (sprint_dir / "tickets").is_dir()
        assert (sprint_dir / "tickets" / "done").is_dir()
        assert result["id"] == "001"
        assert result["branch"] == "sprint/001-test-sprint"

    def test_auto_increments_id(self, work_dir):
        create_sprint("First")
        result = json.loads(create_sprint("Second"))
        assert result["id"] == "002"

    def test_same_title_gets_different_id(self, work_dir):
        r1 = json.loads(create_sprint("Test Sprint"))
        r2 = json.loads(create_sprint("Test Sprint"))
        assert r1["id"] == "001"
        assert r2["id"] == "002"

    def test_sprint_template_has_merged_sections(self, work_dir):
        create_sprint("My Sprint")
        sprint_dir = work_dir / "docs" / "plans" / "sprints" / "001-my-sprint"
        content = (sprint_dir / "sprint.md").read_text()
        assert "## Problem" in content
        assert "## Solution" in content
        assert "## Success Criteria" in content
        assert "## Test Strategy" in content


class TestCreateTicket:
    def test_creates_ticket(self, work_dir):
        create_sprint("My Sprint")
        _advance_to_ticketing(work_dir, "001")
        result = json.loads(create_ticket("001", "Add Feature"))
        assert result["id"] == "001"
        assert "001-add-feature.md" in result["path"]

    def test_auto_increments(self, work_dir):
        create_sprint("My Sprint")
        _advance_to_ticketing(work_dir, "001")
        create_ticket("001", "First")
        result = json.loads(create_ticket("001", "Second"))
        assert result["id"] == "002"

    def test_ticket_template_includes_testing_section(self, work_dir):
        create_sprint("My Sprint")
        _advance_to_ticketing(work_dir, "001")
        ticket = json.loads(create_ticket("001", "Test Feature"))
        from pathlib import Path
        content = Path(ticket["path"]).read_text(encoding="utf-8")
        assert "## Testing" in content
        assert "Existing tests to run" in content
        assert "New tests to write" in content
        assert "Verification command" in content
        assert "`uv run pytest`" in content

    def test_invalid_sprint(self, work_dir):
        with pytest.raises(ValueError, match="not found"):
            create_ticket("999", "Orphan")

    def test_blocked_before_ticketing_phase(self, work_dir):
        create_sprint("My Sprint")
        with pytest.raises(ValueError, match="planning-docs.*phase"):
            create_ticket("001", "Too Early")




class TestListSprints:
    def test_lists_sprints(self, work_dir):
        create_sprint("Sprint A")
        create_sprint("Sprint B")
        result = json.loads(list_sprints())
        assert len(result) == 2
        assert result[0]["id"] == "001"
        assert result[1]["id"] == "002"

    def test_filter_by_status(self, work_dir):
        create_sprint("Active Sprint")
        result = json.loads(list_sprints(status="planning"))
        assert len(result) == 1
        result = json.loads(list_sprints(status="done"))
        assert len(result) == 0

    def test_empty(self, work_dir):
        result = json.loads(list_sprints())
        assert result == []


class TestListTickets:
    def test_lists_tickets(self, work_dir):
        create_sprint("Sprint")
        _advance_to_ticketing(work_dir, "001")
        create_ticket("001", "Task A")
        create_ticket("001", "Task B")
        result = json.loads(list_tickets())
        assert len(result) == 2

    def test_filter_by_sprint(self, work_dir):
        create_sprint("Sprint 1")
        create_sprint("Sprint 2")
        _advance_to_ticketing(work_dir, "001")
        _advance_to_ticketing(work_dir, "002")
        create_ticket("001", "Task in S1")
        create_ticket("002", "Task in S2")
        result = json.loads(list_tickets(sprint_id="001"))
        assert len(result) == 1
        assert result[0]["sprint_id"] == "001"

    def test_filter_by_status(self, work_dir):
        create_sprint("Sprint")
        _advance_to_ticketing(work_dir, "001")
        create_ticket("001", "Todo Task")
        result = json.loads(list_tickets(status="todo"))
        assert len(result) == 1
        result = json.loads(list_tickets(status="done"))
        assert len(result) == 0


class TestGetSprintStatus:
    def test_status_with_tickets(self, work_dir):
        create_sprint("Sprint")
        _advance_to_ticketing(work_dir, "001")
        create_ticket("001", "Task A")
        create_ticket("001", "Task B")
        result = json.loads(get_sprint_status("001"))
        assert result["id"] == "001"
        assert result["status"] == "planning"
        assert result["tickets"]["todo"] == 2
        assert result["tickets"]["done"] == 0

    def test_not_found(self, work_dir):
        with pytest.raises(ValueError, match="not found"):
            get_sprint_status("999")


class TestUpdateTicketStatus:
    def test_updates_status(self, work_dir):
        create_sprint("Sprint")
        _advance_to_ticketing(work_dir, "001")
        ticket = json.loads(create_ticket("001", "Task"))
        result = json.loads(update_ticket_status(ticket["path"], "in-progress"))
        assert result["old_status"] == "todo"
        assert result["new_status"] == "in-progress"
        fm = read_frontmatter(ticket["path"])
        assert fm["status"] == "in-progress"

    def test_invalid_status(self, work_dir):
        create_sprint("Sprint")
        _advance_to_ticketing(work_dir, "001")
        ticket = json.loads(create_ticket("001", "Task"))
        with pytest.raises(ValueError, match="Invalid status"):
            update_ticket_status(ticket["path"], "invalid")


class TestMoveTicketToDone:
    def test_moves_ticket(self, work_dir):
        create_sprint("Sprint")
        _advance_to_ticketing(work_dir, "001")
        ticket = json.loads(create_ticket("001", "Task"))
        result = json.loads(move_ticket_to_done(ticket["path"]))
        assert not os.path.exists(result["old_path"])
        assert os.path.exists(result["new_path"])
        assert "done" in result["new_path"]

    def test_moves_plan_too(self, work_dir):
        create_sprint("Sprint")
        _advance_to_ticketing(work_dir, "001")
        ticket = json.loads(create_ticket("001", "Task"))
        # Create a plan file
        from pathlib import Path
        plan_path = Path(ticket["path"]).parent / "001-task-plan.md"
        plan_path.write_text("# Plan\n", encoding="utf-8")
        result = json.loads(move_ticket_to_done(ticket["path"]))
        assert "plan_new_path" in result


class TestCloseSprint:
    def test_closes_sprint(self, work_dir):
        create_sprint("Sprint")
        result = json.loads(close_sprint("001"))
        assert "done" in result["new_path"]
        assert not os.path.exists(result["old_path"])
        # Verify status was updated
        from pathlib import Path
        sprint_file = Path(result["new_path"]) / "sprint.md"
        fm = read_frontmatter(sprint_file)
        assert fm["status"] == "done"


class TestInsertSprint:
    def test_inserts_and_renumbers(self, work_dir):
        create_sprint("Alpha")
        create_sprint("Beta")
        create_sprint("Gamma")

        result = json.loads(insert_sprint("001", "Urgent Fix"))

        # New sprint gets ID 002
        assert result["id"] == "002"
        assert "002-urgent-fix" in result["path"]
        assert result["phase"] == "planning-docs"

        # Old 002 (Beta) -> 003, old 003 (Gamma) -> 004
        assert len(result["renumbered"]) == 2
        assert result["renumbered"][0]["old_id"] == "002"
        assert result["renumbered"][0]["new_id"] == "003"
        assert result["renumbered"][1]["old_id"] == "003"
        assert result["renumbered"][1]["new_id"] == "004"

        # Verify directories exist with correct names
        sprints = work_dir / "docs" / "plans" / "sprints"
        assert (sprints / "001-alpha").is_dir()
        assert (sprints / "002-urgent-fix").is_dir()
        assert (sprints / "003-beta").is_dir()
        assert (sprints / "004-gamma").is_dir()
        # Old directories should be gone
        assert not (sprints / "002-beta").exists()
        assert not (sprints / "003-gamma").exists()

    def test_renumbered_sprint_frontmatter_updated(self, work_dir):
        create_sprint("Alpha")
        create_sprint("Beta")
        insert_sprint("001", "Inserted")

        # Beta was 002, now should be 003
        sprints = work_dir / "docs" / "plans" / "sprints"
        fm = read_frontmatter(sprints / "003-beta" / "sprint.md")
        assert fm["id"] == "003"
        assert fm["branch"] == "sprint/003-beta"

    def test_renumbered_sprint_body_updated(self, work_dir):
        create_sprint("Alpha")
        create_sprint("Beta")
        insert_sprint("001", "Inserted")

        sprints = work_dir / "docs" / "plans" / "sprints"
        content = (sprints / "003-beta" / "sprint.md").read_text(encoding="utf-8")
        assert "Sprint 003" in content
        assert "Sprint 002" not in content

    def test_insert_at_end_no_renumbering(self, work_dir):
        create_sprint("Alpha")
        create_sprint("Beta")
        result = json.loads(insert_sprint("002", "Final"))

        assert result["id"] == "003"
        assert result["renumbered"] == []

        sprints = work_dir / "docs" / "plans" / "sprints"
        assert (sprints / "003-final").is_dir()

    def test_refuses_renumbering_active_sprint(self, work_dir):
        create_sprint("Alpha")
        create_sprint("Beta")
        # Advance Beta (002) past planning-docs
        _advance_to_ticketing(work_dir, "002")

        with pytest.raises(ValueError, match="cannot be renumbered"):
            insert_sprint("001", "Urgent")

    def test_insert_with_tickets_updates_references(self, work_dir):
        create_sprint("Alpha")
        create_sprint("Beta")
        _advance_to_ticketing(work_dir, "002")

        # Create tickets in Beta (002)
        create_ticket("002", "Task A")
        create_ticket("002", "Task B")

        # Now insert after Alpha — but Beta is in ticketing phase, should fail
        with pytest.raises(ValueError, match="cannot be renumbered"):
            insert_sprint("001", "Inserted")

    def test_insert_after_nonexistent_sprint(self, work_dir):
        create_sprint("Alpha")
        with pytest.raises(ValueError, match="not found"):
            insert_sprint("999", "Ghost")

    def test_new_sprint_has_full_structure(self, work_dir):
        create_sprint("Alpha")
        result = json.loads(insert_sprint("001", "New Sprint"))

        from pathlib import Path
        sprint_dir = Path(result["path"])
        assert (sprint_dir / "sprint.md").exists()
        assert (sprint_dir / "usecases.md").exists()
        assert (sprint_dir / "technical-plan.md").exists()
        assert (sprint_dir / "tickets").is_dir()
        assert (sprint_dir / "tickets" / "done").is_dir()

    def test_insert_before_multiple_planning_sprints(self, work_dir):
        create_sprint("Alpha")
        create_sprint("Beta")
        create_sprint("Gamma")
        create_sprint("Delta")

        result = json.loads(insert_sprint("001", "Urgent"))
        assert result["id"] == "002"
        assert len(result["renumbered"]) == 3

        sprints = work_dir / "docs" / "plans" / "sprints"
        assert (sprints / "001-alpha").is_dir()
        assert (sprints / "002-urgent").is_dir()
        assert (sprints / "003-beta").is_dir()
        assert (sprints / "004-gamma").is_dir()
        assert (sprints / "005-delta").is_dir()


class TestCreateOverview:
    def test_creates_overview(self, work_dir):
        from claude_agent_skills.artifact_tools import create_overview
        result = json.loads(create_overview())
        path = work_dir / "docs" / "plans" / "overview.md"
        assert path.exists()
        content = path.read_text()
        assert "# Project Overview" in content
        assert "## Problem Statement" in content
        assert "## Sprint Roadmap" in content

    def test_rejects_duplicate(self, work_dir):
        from claude_agent_skills.artifact_tools import create_overview
        create_overview()
        with pytest.raises(ValueError, match="already exists"):
            create_overview()
