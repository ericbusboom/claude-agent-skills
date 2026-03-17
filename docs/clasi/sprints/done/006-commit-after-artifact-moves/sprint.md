---
id: '006'
title: Commit After Artifact Moves
status: done
branch: sprint/006-commit-after-artifact-moves
use-cases:
- SUC-001
---

# Sprint 006: Commit After Artifact Moves

## Goals

Ensure that MCP file-move operations (`move_ticket_to_done`, `close_sprint`,
`move_todo_to_done`) are always followed by a git commit, so nothing is left
uncommitted at the end of a sprint.

## Problem

The MCP tools move files on disk but do not run `git commit`. The skill
instructions (`execute-ticket`, `close-sprint`, `plan-sprint`) don't
explicitly say to commit after these moves. In Sprint 005 this left 22
uncommitted file changes after the sprint was "closed."

## Solution

Update the three skill files to add explicit commit steps after every
file-move operation. No Python code changes — skills only.

## Success Criteria

- Each skill explicitly instructs committing after file moves
- Reading the skills end-to-end, there is no point where files are moved
  without a subsequent commit step

## Scope

### In Scope

- `skills/execute-ticket.md` — commit after ticket/plan move to done/
- `skills/close-sprint.md` — commit after `close_sprint` MCP tool
- `skills/plan-sprint.md` — commit after `move_todo_to_done` calls

### Out of Scope

- Changing the MCP tools themselves to auto-commit (they should stay
  git-unaware)
- Adding new tests (no Python changes)

## Test Strategy

No code changes, so no new tests. Verify by reading each skill for
completeness.

## Architecture Notes

Skills are markdown instruction files — this is a documentation-only sprint.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, technical plan)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
