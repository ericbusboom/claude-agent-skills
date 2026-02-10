---
id: "001"
title: State DB schema and core functions
status: done
use-cases:
  - SUC-001
depends-on: []
---

# State DB schema and core functions

## Description

Create a new module `claude_agent_skills/state_db.py` that provides the SQLite
database schema and core functions for tracking sprint lifecycle state. This is
the foundation for all process hardening in sprint 002 -- every other database
ticket builds on this schema and these functions.

The module introduces three tables:

- **sprints**: Stores sprint registration data including ID, slug, current phase,
  branch name, and timestamps.
- **sprint_gates**: Records review gate results (architecture review, stakeholder
  approval) with timestamps and optional notes. Uses a UNIQUE constraint on
  `(sprint_id, gate_name)` so re-recording a gate overwrites the previous result.
- **execution_locks**: A singleton table (enforced by `CHECK (id = 1)`) that
  tracks which sprint currently holds the execution lock.

The database file lives at `docs/plans/.clasi.db`, co-located with the planning
artifacts it tracks. It is local coordination state, not a versioned artifact,
so it must be added to `.gitignore`.

The module uses lazy initialization: the database and tables are created on first
use. All functions are pure Python, taking a `db_path` parameter and returning
results. No MCP decorators -- the MCP tool layer calls these functions.

### Functions to implement

- `init_db(db_path)` -- Create the database file and all tables if they do not
  exist. Uses `CREATE TABLE IF NOT EXISTS`. Enables WAL mode for safe concurrent
  reads.
- `register_sprint(db_path, sprint_id, slug, branch)` -- Insert a new sprint
  record with phase set to `planning-docs` and timestamps set to now (ISO 8601).
  Calls `init_db` internally (lazy init).
- `get_sprint_state(db_path, sprint_id)` -- Return a dict containing the
  sprint's current phase, all gate results, and lock status. Raises if the
  sprint is not registered.

### Schema

```sql
CREATE TABLE sprints (
    id TEXT PRIMARY KEY,
    slug TEXT NOT NULL,
    phase TEXT NOT NULL DEFAULT 'planning-docs',
    branch TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE sprint_gates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sprint_id TEXT NOT NULL REFERENCES sprints(id),
    gate_name TEXT NOT NULL,
    result TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    notes TEXT,
    UNIQUE(sprint_id, gate_name)
);

CREATE TABLE execution_locks (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    sprint_id TEXT NOT NULL REFERENCES sprints(id),
    acquired_at TEXT NOT NULL
);
```

## Acceptance Criteria

- [ ] `claude_agent_skills/state_db.py` exists with the three-table schema
- [ ] `init_db(db_path)` creates the database and all tables idempotently (`CREATE TABLE IF NOT EXISTS`)
- [ ] `init_db` enables WAL mode on the SQLite connection
- [ ] `register_sprint(db_path, sprint_id, slug, branch)` inserts a sprint record with phase `planning-docs` and ISO 8601 timestamps
- [ ] `register_sprint` calls `init_db` internally (lazy initialization)
- [ ] Registering a sprint that already exists raises a clear error
- [ ] `get_sprint_state(db_path, sprint_id)` returns a dict with `phase`, `gates` (list), and `lock` (holder or None)
- [ ] `get_sprint_state` raises a clear error if the sprint is not registered
- [ ] `.clasi.db` is added to the project `.gitignore`
- [ ] No external dependencies are introduced (only Python stdlib `sqlite3`)
- [ ] All functions accept `db_path` as their first argument; the default path is `docs/plans/.clasi.db`
- [ ] Unit tests cover `init_db`, `register_sprint`, and `get_sprint_state`
