---
status: done
sprint: '002'
tickets:
- '017'
---

# Move Active Subagent/Task Markers to State DB

The `.active/` directory under `docs/clasi/log/` uses JSON marker files to link SubagentStart → SubagentStop and TaskCreated → TaskCompleted events. This is redundant — we have a SQLite state DB (`docs/clasi/.clasi.db`) that should hold this state instead.

Also applies to `.clasi-agent-tier` — the tier marker written by SubagentStart for the role guard. This should be a DB record, not a file that goes stale when subagents crash.

Move all runtime markers into a new `active_agents` table in the state DB. Benefits:
- Single source of truth
- Automatic cleanup via TTL (like recovery_state)
- No orphaned files when subagents crash
- Transactional writes
