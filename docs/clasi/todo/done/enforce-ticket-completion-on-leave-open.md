---
status: done
sprint: '002'
tickets:
- '004'
---

# Enforce Ticket Completion When Stakeholder Says "Leave Open"

When a stakeholder says "leave the ticket open" after implementation is complete, the agent should always mark the ticket done and leave the sprint open. There is no valid reason to leave a ticket in an incomplete state once its work is finished.

The agent should either:
1. **Interpret automatically** — treat "leave it open" as "leave the sprint open" and mark the ticket done, or
2. **Flag the ambiguity** — ask the stakeholder to clarify, noting that tickets should be marked done when work is complete.

This could be enforced via agent instructions (in the team-lead agent or execute-ticket skill) or as a CLASI process rule that tickets must be closed when their acceptance criteria are met.
