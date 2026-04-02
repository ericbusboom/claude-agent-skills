---
id: '017'
title: Move active markers to state DB
status: done
use-cases: []
depends-on: []
github-issue: ''
todo: move-active-markers-to-state-db.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Move active markers to state DB

## Description

The `.active/` directory under `docs/clasi/log/` uses JSON marker files to link SubagentStart→SubagentStop and TaskCreated→TaskCompleted events. The `.clasi-agent-tier` file is a runtime marker for the role guard. Both should move into a new `active_agents` table in the state DB (`docs/clasi/.clasi.db`). This eliminates orphaned files when subagents crash and provides a single source of truth.

## Acceptance Criteria

- [x] New `active_agents` table in state DB schema
- [x] SubagentStart/TaskCreated write to DB instead of `.active/` JSON files
- [x] SubagentStop/TaskCompleted read from DB and clean up
- [x] Role guard reads agent tier from DB instead of `.clasi-agent-tier` file
- [x] `.active/` directories and `.clasi-agent-tier` file no longer created
- [x] Stale records auto-cleared (TTL like recovery_state)
- [x] All existing tests pass

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: Tests verifying `active_agents` table creation, insert on SubagentStart/TaskCreated, cleanup on SubagentStop/TaskCompleted, role guard reads tier from DB, and TTL/stale record clearing
- **Verification command**: `uv run pytest`
