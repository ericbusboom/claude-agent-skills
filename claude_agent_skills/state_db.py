"""Sprint lifecycle state database.

Provides SQLite-backed tracking of sprint phases, review gates, and
execution locks. All functions take a db_path parameter and return
results — no MCP decorators. The MCP tool layer calls these functions.
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


PHASES = [
    "planning-docs",
    "architecture-review",
    "stakeholder-review",
    "ticketing",
    "executing",
    "closing",
    "done",
]

VALID_GATE_NAMES = {"architecture_review", "stakeholder_approval"}
VALID_GATE_RESULTS = {"passed", "failed"}

_SCHEMA = """\
CREATE TABLE IF NOT EXISTS sprints (
    id TEXT PRIMARY KEY,
    slug TEXT NOT NULL,
    phase TEXT NOT NULL DEFAULT 'planning-docs',
    branch TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sprint_gates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sprint_id TEXT NOT NULL REFERENCES sprints(id),
    gate_name TEXT NOT NULL,
    result TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    notes TEXT,
    UNIQUE(sprint_id, gate_name)
);

CREATE TABLE IF NOT EXISTS execution_locks (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    sprint_id TEXT NOT NULL REFERENCES sprints(id),
    acquired_at TEXT NOT NULL
);
"""


def _now() -> str:
    """Return the current time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _connect(db_path: str | Path) -> sqlite3.Connection:
    """Open a connection with WAL mode and foreign keys enabled."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(db_path: str | Path) -> None:
    """Create the database file and all tables if they do not exist."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = _connect(path)
    try:
        conn.executescript(_SCHEMA)
    finally:
        conn.close()


def register_sprint(
    db_path: str | Path,
    sprint_id: str,
    slug: str,
    branch: Optional[str] = None,
) -> dict[str, Any]:
    """Register a new sprint in the state database.

    Calls init_db internally (lazy initialization).

    Raises ValueError if the sprint is already registered.
    """
    init_db(db_path)
    now = _now()
    conn = _connect(db_path)
    try:
        try:
            conn.execute(
                "INSERT INTO sprints (id, slug, phase, branch, created_at, updated_at) "
                "VALUES (?, ?, 'planning-docs', ?, ?, ?)",
                (sprint_id, slug, branch, now, now),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"Sprint '{sprint_id}' is already registered")
        return {
            "id": sprint_id,
            "slug": slug,
            "phase": "planning-docs",
            "branch": branch,
            "created_at": now,
            "updated_at": now,
        }
    finally:
        conn.close()


def get_sprint_state(db_path: str | Path, sprint_id: str) -> dict[str, Any]:
    """Return a dict with the sprint's phase, gates, and lock status.

    Raises ValueError if the sprint is not registered.
    """
    init_db(db_path)
    conn = _connect(db_path)
    try:
        row = conn.execute(
            "SELECT id, slug, phase, branch, created_at, updated_at "
            "FROM sprints WHERE id = ?",
            (sprint_id,),
        ).fetchone()
        if row is None:
            raise ValueError(f"Sprint '{sprint_id}' is not registered")

        gates = []
        for g in conn.execute(
            "SELECT gate_name, result, recorded_at, notes "
            "FROM sprint_gates WHERE sprint_id = ? ORDER BY gate_name",
            (sprint_id,),
        ):
            gates.append({
                "gate_name": g["gate_name"],
                "result": g["result"],
                "recorded_at": g["recorded_at"],
                "notes": g["notes"],
            })

        lock_row = conn.execute(
            "SELECT sprint_id, acquired_at FROM execution_locks WHERE id = 1"
        ).fetchone()
        lock = None
        if lock_row and lock_row["sprint_id"] == sprint_id:
            lock = {
                "sprint_id": lock_row["sprint_id"],
                "acquired_at": lock_row["acquired_at"],
            }

        return {
            "id": row["id"],
            "slug": row["slug"],
            "phase": row["phase"],
            "branch": row["branch"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "gates": gates,
            "lock": lock,
        }
    finally:
        conn.close()
