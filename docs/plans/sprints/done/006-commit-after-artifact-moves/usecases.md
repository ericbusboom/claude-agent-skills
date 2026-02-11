---
status: draft
---

# Sprint 006 Use Cases

## SUC-001: Explicit commit after every file-move operation
Parent: none (process gap)

- **Actor**: AI agent executing a skill
- **Preconditions**: Agent is following a skill that calls an MCP file-move tool
- **Main Flow**:
  1. Agent completes a file-move operation (move_ticket_to_done,
     close_sprint, move_todo_to_done)
  2. Agent reads the skill and sees an explicit instruction to commit
  3. Agent runs `git add` + `git commit` for the moved files
- **Postconditions**: Working tree is clean after every file-move step
- **Acceptance Criteria**:
  - [ ] `execute-ticket.md` has a commit step after moving ticket/plan to done/
  - [ ] `close-sprint.md` has a commit step after `close_sprint` MCP tool
  - [ ] `plan-sprint.md` has a commit step after moving TODOs to done/
