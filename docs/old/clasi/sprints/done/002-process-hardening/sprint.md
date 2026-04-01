---
id: "002"
title: Process Hardening
status: done
branch: sprint/002-process-hardening
use-cases: [UC-004]
---

# Sprint 002: Process Hardening

## Goals

Make the sprint lifecycle enforceable rather than just documented. Sprint 001
showed that AI agents skip review gates and generate all artifacts in a single
batch. This sprint adds structural enforcement: a SQLite state database for
lifecycle tracking, MCP tools for phase management, a Definition of Ready
checklist, and explicit traceability between sprint and project use cases.

## Scope

### In Scope

1. **SQLite state database**: A database managed by the CLASI MCP server that
   tracks sprint lifecycle phase, review gate status, and execution locks. AIs
   interact with it exclusively through MCP tools — no direct database writes.

2. **Sprint phase tracking via MCP**: Tools to query current phase, advance
   phase (with gate checks), and record review gate results. Phases:
   `planning-docs`, `architecture-review`, `stakeholder-review`, `ticketing`,
   `executing`, `closing`, `done`.

3. **Execution lock coordination**: A mechanism to prevent two sprints from
   executing simultaneously in the same repository. One sprint holds the
   execution lock; others must wait or plan in parallel.

4. **Definition of Ready checklist**: A checklist in the sprint.md template
   (like the ticket Definition of Done) that must be satisfied before tickets
   can be created. Includes: planning docs complete, architecture review
   passed, stakeholder approved.

5. **Use case traceability**: Sprint use cases explicitly reference their
   parent top-level use case(s). The project-status tool reports coverage.

6. **Update plan-sprint and close-sprint skills**: Integrate phase tracking
   into the sprint lifecycle skills so they use the database.

### Out of Scope

- Multi-repository coordination (only single-repo for now)
- Web UI or dashboard for sprint state (CLI/MCP only)
- Migrating sprint 001 data into the database retroactively
- Changes to the document structure (that is sprint 003)

## Architecture Notes

- SQLite database lives at `docs/plans/.clasi.db` (inside the plans directory,
  alongside the sprint directories it tracks).
- Database is created/migrated automatically when the MCP server starts or
  when `clasi init` runs.
- All database mutations go through MCP tool functions. The AI calls the tool;
  the tool validates and writes.
- Phase advancement is gated: `advance_sprint_phase` checks that required
  conditions are met (e.g., architecture review recorded) before allowing
  transition.
- The execution lock is advisory but enforced by MCP tools: `create_ticket`
  and `update_ticket_status` check that the sprint holds the execution lock.

## Source TODOs

- `docs/plans/todo/sprint-review-gates.md`
- `docs/plans/todo/sprint-state-database.md`
- `docs/plans/todo/use-case-traceability.md`

## Tickets

| ID  | Title | Depends On |
|-----|-------|-----------|
| 001 | State DB schema and core functions | — |
| 002 | Phase transition logic | 001 |
| 003 | Gate recording | 001 |
| 004 | Execution locks | 001 |
| 005 | State MCP tools | 002, 003, 004 |
| 006 | Gate enforcement in create_ticket and update_ticket_status | 005 |
| 007 | Integrate state DB with create_sprint and close_sprint | 005 |
| 008 | Sprint template Definition of Ready | — |
| 009 | Use case traceability | — |
| 010 | Update skills for phase tracking | 007 |

Independent starting points: 001, 008, 009

Critical path: 001 → 002/003/004 → 005 → 006/007 → 010
