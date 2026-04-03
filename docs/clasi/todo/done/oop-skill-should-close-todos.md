---
status: done
sprint: '003'
tickets:
- 008
---

# OOP skill should close TODOs after implementation

When implementing a TODO out-of-process, the `oop` skill has no step for moving the
TODO to done. The ticket-based flow handles this automatically (move_ticket_to_done
triggers TODO completion), but OOP bypasses tickets entirely.

Add a step to the OOP skill: after committing, check if the work addressed a TODO.
If so, call `move_todo_to_done`. This makes TODO closure a structural requirement
of the process, not something the agent has to remember.

Also consider: should the team-lead agent's "implement TODO directly" paths always
include a TODO closure step? Audit all paths where a TODO can be implemented without
going through a ticket.
