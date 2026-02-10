"""Tests for claude_agent_skills.state_db module."""

import sqlite3

import pytest

from claude_agent_skills.state_db import (
    PHASES,
    init_db,
    register_sprint,
    get_sprint_state,
)


@pytest.fixture
def db_path(tmp_path):
    """Return a temporary database path."""
    return tmp_path / "test.db"


class TestInitDb:
    def test_creates_database_file(self, db_path):
        init_db(db_path)
        assert db_path.exists()

    def test_creates_tables(self, db_path):
        init_db(db_path)
        conn = sqlite3.connect(str(db_path))
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        conn.close()
        assert "sprints" in tables
        assert "sprint_gates" in tables
        assert "execution_locks" in tables

    def test_idempotent(self, db_path):
        init_db(db_path)
        init_db(db_path)  # Should not raise
        assert db_path.exists()

    def test_enables_wal_mode(self, db_path):
        init_db(db_path)
        conn = sqlite3.connect(str(db_path))
        mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
        conn.close()
        assert mode == "wal"

    def test_creates_parent_directories(self, tmp_path):
        deep_path = tmp_path / "a" / "b" / "c" / "test.db"
        init_db(deep_path)
        assert deep_path.exists()


class TestRegisterSprint:
    def test_registers_sprint(self, db_path):
        result = register_sprint(db_path, "001", "test-sprint", "sprint/001-test-sprint")
        assert result["id"] == "001"
        assert result["slug"] == "test-sprint"
        assert result["phase"] == "planning-docs"
        assert result["branch"] == "sprint/001-test-sprint"
        assert result["created_at"] is not None
        assert result["updated_at"] is not None

    def test_lazy_init(self, db_path):
        """register_sprint creates the DB if it doesn't exist."""
        assert not db_path.exists()
        register_sprint(db_path, "001", "test", None)
        assert db_path.exists()

    def test_duplicate_raises(self, db_path):
        register_sprint(db_path, "001", "test", None)
        with pytest.raises(ValueError, match="already registered"):
            register_sprint(db_path, "001", "test", None)

    def test_multiple_sprints(self, db_path):
        r1 = register_sprint(db_path, "001", "first", None)
        r2 = register_sprint(db_path, "002", "second", None)
        assert r1["id"] == "001"
        assert r2["id"] == "002"

    def test_branch_optional(self, db_path):
        result = register_sprint(db_path, "001", "test")
        assert result["branch"] is None


class TestGetSprintState:
    def test_returns_state(self, db_path):
        register_sprint(db_path, "001", "test", "sprint/001-test")
        state = get_sprint_state(db_path, "001")
        assert state["id"] == "001"
        assert state["slug"] == "test"
        assert state["phase"] == "planning-docs"
        assert state["branch"] == "sprint/001-test"
        assert state["gates"] == []
        assert state["lock"] is None

    def test_not_registered_raises(self, db_path):
        init_db(db_path)
        with pytest.raises(ValueError, match="not registered"):
            get_sprint_state(db_path, "999")

    def test_lazy_init(self, db_path):
        """get_sprint_state initializes DB if needed, then raises for missing sprint."""
        assert not db_path.exists()
        with pytest.raises(ValueError, match="not registered"):
            get_sprint_state(db_path, "001")
        assert db_path.exists()


class TestPhaseConstants:
    def test_phase_order(self):
        assert PHASES[0] == "planning-docs"
        assert PHASES[-1] == "done"
        assert len(PHASES) == 7

    def test_all_phases_present(self):
        expected = {
            "planning-docs", "architecture-review", "stakeholder-review",
            "ticketing", "executing", "closing", "done",
        }
        assert set(PHASES) == expected
