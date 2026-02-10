---
status: draft
sprint: "002"
---

# Sprint 002 Technical Plan

## Architecture Overview

This sprint adds a SQLite state database to the CLASI MCP server. The database
tracks sprint lifecycle phases and review gate results. All mutations go
through MCP tools — AI agents never write to the database directly.

```
┌─────────────────────────────────────────────────┐
│                  AI Agent                        │
│  (calls MCP tools, never touches DB directly)    │
└───────────────┬─────────────────────────────────┘
                │ MCP tool calls
                ▼
┌─────────────────────────────────────────────────┐
│              CLASI MCP Server                    │
│  ┌──────────────┐  ┌─────────────────────────┐  │
│  │ process_tools │  │    artifact_tools       │  │
│  │ (read-only)   │  │ (create/update/query)   │  │
│  └──────────────┘  └──────────┬──────────────┘  │
│                               │                  │
│  ┌────────────────────────────▼──────────────┐  │
│  │           state_db.py (NEW)               │  │
│  │  - init_db() / migrate()                  │  │
│  │  - get_sprint_phase()                     │  │
│  │  - advance_sprint_phase()                 │  │
│  │  - record_gate_result()                   │  │
│  │  - acquire/release_execution_lock()       │  │
│  │  - get_sprint_state()                     │  │
│  └────────────────────────────┬──────────────┘  │
│                               │                  │
│                    ┌──────────▼──────────┐       │
│                    │  docs/plans/.clasi.db│       │
│                    │  (SQLite)           │       │
│                    └─────────────────────┘       │
└─────────────────────────────────────────────────┘
```

## Technology Stack

- **SQLite**: Via Python's built-in `sqlite3` module. No additional
  dependencies needed.
- **Database location**: `docs/plans/.clasi.db`. This keeps it with the
  planning artifacts it tracks. Add to `.gitignore` — the database is
  local coordination state, not a versioned artifact.

## Component Design

### Component: State Database Module (`claude_agent_skills/state_db.py`)

**Use Cases**: SUC-001, SUC-002, SUC-003, SUC-004

New module providing all database operations. Pure Python functions that
take a database path and return results. No MCP decorators — the MCP tools
call these functions.

**Schema**:

```sql
CREATE TABLE sprints (
    id TEXT PRIMARY KEY,          -- "002"
    slug TEXT NOT NULL,           -- "process-hardening"
    phase TEXT NOT NULL DEFAULT 'planning-docs',
    branch TEXT,
    created_at TEXT NOT NULL,     -- ISO 8601
    updated_at TEXT NOT NULL
);

CREATE TABLE sprint_gates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sprint_id TEXT NOT NULL REFERENCES sprints(id),
    gate_name TEXT NOT NULL,      -- 'architecture_review', 'stakeholder_approval'
    result TEXT NOT NULL,         -- 'passed', 'failed'
    recorded_at TEXT NOT NULL,
    notes TEXT,
    UNIQUE(sprint_id, gate_name)
);

CREATE TABLE execution_locks (
    id INTEGER PRIMARY KEY CHECK (id = 1),  -- singleton row
    sprint_id TEXT NOT NULL REFERENCES sprints(id),
    acquired_at TEXT NOT NULL
);
```

**Phase values** (in order):
1. `planning-docs` — sprint directory created, planning docs being written
2. `architecture-review` — docs complete, architecture review in progress
3. `stakeholder-review` — arch review passed, awaiting stakeholder approval
4. `ticketing` — approved, tickets being created
5. `executing` — tickets being implemented
6. `closing` — all tickets done, closing the sprint
7. `done` — sprint archived

**Phase transition rules**:
- `planning-docs` → `architecture-review`: No gate (agent decides docs are ready)
- `architecture-review` → `stakeholder-review`: Requires `architecture_review`
  gate result = `passed`
- `stakeholder-review` → `ticketing`: Requires `stakeholder_approval` gate
  result = `passed`
- `ticketing` → `executing`: Requires at least one ticket exists AND execution
  lock acquired
- `executing` → `closing`: All tickets in `done` status
- `closing` → `done`: Sprint directory moved to `done/`, branch deleted

**Functions**:
- `init_db(db_path)` — create tables if not exists
- `register_sprint(db_path, sprint_id, slug, branch)` — insert sprint record
- `get_sprint_state(db_path, sprint_id)` — returns phase, gates, lock status
- `advance_phase(db_path, sprint_id)` — validate and advance to next phase
- `record_gate(db_path, sprint_id, gate_name, result, notes)` — record gate
- `acquire_lock(db_path, sprint_id)` — attempt to acquire execution lock
- `release_lock(db_path, sprint_id)` — release execution lock
- `get_lock_holder(db_path)` — who holds the lock, if anyone

### Component: State MCP Tools (`claude_agent_skills/artifact_tools.py`)

**Use Cases**: SUC-001, SUC-002, SUC-003, SUC-004

New MCP tools added to the artifact tools module. These are thin wrappers
around `state_db.py` functions.

| Tool | Description |
|------|-------------|
| `get_sprint_phase(sprint_id)` | Returns current phase and gate status |
| `advance_sprint_phase(sprint_id)` | Advances to next phase if gates pass |
| `record_gate_result(sprint_id, gate, result, notes)` | Records review result |
| `acquire_execution_lock(sprint_id)` | Claims execution slot |
| `release_execution_lock(sprint_id)` | Releases execution slot |

### Component: Gate Enforcement in Existing Tools

**Use Cases**: SUC-004

Modify `create_ticket` to check the sprint's phase before allowing ticket
creation. If the sprint is not in `ticketing` phase or later, refuse with
an error explaining what phase the sprint is in and what must happen first.

Similarly, modify `update_ticket_status` to check that the sprint holds
the execution lock before allowing status changes during execution.

### Component: Sprint Template Updates

**Use Cases**: SUC-001

Add a **Definition of Ready** checklist to the sprint.md template:

```markdown
## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (brief, use cases, technical plan)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan
```

This is documentation — the actual enforcement comes from the database.
But the checklist makes the requirement visible in the document.

### Component: Use Case Traceability

**Use Cases**: SUC-005

Update the use case template to include a `parent` field:

```markdown
## SUC-001: Description
Parent: UC-XXX
```

Update `project_status` (or add a new `get_use_case_coverage` tool) to
read top-level use cases and sprint use cases, match parents, and report
coverage.

### Component: Automatic Sprint Registration

**Use Cases**: SUC-001

When `create_sprint` runs, it also calls `register_sprint` to add the
sprint to the database. This ensures every sprint has a state record
from the moment it is created.

When `close_sprint` runs, it advances the phase to `done` and releases
any execution lock.

## Dependencies

- SQLite is in the Python standard library — no new dependencies.
- This sprint modifies `artifact_tools.py` and `templates.py` from
  sprint 001.
- The `state_db.py` module is entirely new.

## Open Questions

None — all design decisions are resolved in this plan.
