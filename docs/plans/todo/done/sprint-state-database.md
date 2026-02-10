# Sprint State Database

Consider adding a SQLite database for "you are here" state tracking across
multiple AI model invocations. Files remain the primary record, but the database
provides coordination and state that is hard to express in files alone.

## Why

- Multiple sprints may exist simultaneously (one executing, one planning).
- Multiple Claude sessions may interact with the same project.
- An agent needs to know "where am I in the sprint lifecycle?" without
  re-reading and re-analyzing all artifacts every time.
- Review gates need persistent state: "has the architecture review passed?"
  cannot be reliably inferred from file contents alone.

## Design Principles

- Track at the unit of a sprint. Each sprint has a state record.
- Files remain the source of truth for content (briefs, tickets, etc.).
  The database tracks lifecycle state and coordination metadata.
- AIs do NOT write to the database directly. All database operations go
  through MCP tools exposed by the CLASI server. The AI asks the MCP server
  to perform an action, and the server does the work.
- The database enables coordination: if sprint A is executing and sprint B
  is planning, the system can tell the planning agent "you cannot begin
  execution until sprint A merges."

## Possible Schema

- `sprints` table: id, slug, status, branch, phase (planning-docs,
  architecture-review, stakeholder-review, ticketing, executing, closing, done),
  created_at, updated_at
- `sprint_gates` table: sprint_id, gate_name (arch_review, stakeholder_approval),
  status (pending, passed, failed), reviewed_at, notes
- `sprint_locks` table: sprint_id, lock_type (execution), acquired_at —
  prevents two sprints from executing simultaneously on the same repo

## MCP Tools

- `get_sprint_phase(sprint_id)` — returns current lifecycle phase
- `advance_sprint_phase(sprint_id)` — moves to next phase if gates are met
- `record_gate_result(sprint_id, gate, result)` — records review gate outcome
- `acquire_execution_lock(sprint_id)` — claims execution slot
- `release_execution_lock(sprint_id)` — releases execution slot
