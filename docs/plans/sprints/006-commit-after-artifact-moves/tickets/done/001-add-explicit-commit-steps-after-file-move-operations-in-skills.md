---
id: '001'
title: Add explicit commit steps after file-move operations in skills
status: done
use-cases:
- SUC-001
depends-on: []
---

# Add explicit commit steps after file-move operations in skills

## Description

MCP tools (`move_ticket_to_done`, `close_sprint`, `move_todo_to_done`) move
files on disk but don't commit. The skill instructions need explicit commit
steps after these operations.

Update three skill files:

1. **`skills/execute-ticket.md`** — Step 11 moves ticket/plan to `done/` after
   the implementation commit in step 10. Add a commit step after the moves.
2. **`skills/close-sprint.md`** — Step 6 calls `close_sprint` (moves sprint dir,
   bumps version). Add a commit step between steps 6 and 7 (branch delete).
3. **`skills/plan-sprint.md`** — Step 2 moves consumed TODOs to `done/`. Add a
   note to commit after the moves (on the sprint branch, after step 4).

## Acceptance Criteria

- [ ] `execute-ticket.md` has a commit step after moving ticket/plan to done/
- [ ] `close-sprint.md` has a commit step after `close_sprint` MCP tool
- [ ] `plan-sprint.md` has a commit step after moving TODOs to done/
