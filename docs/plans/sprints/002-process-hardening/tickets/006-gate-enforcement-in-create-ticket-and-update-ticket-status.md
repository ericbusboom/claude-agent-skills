---
id: "006"
title: Gate enforcement in create_ticket and update_ticket_status
status: todo
use-cases:
  - SUC-004
depends-on:
  - "005"
---

# Gate enforcement in create_ticket and update_ticket_status

## Description

Modify two existing MCP tools in `artifact_tools.py` to enforce sprint lifecycle
constraints via the state database. This prevents agents from creating tickets
before a sprint is approved or modifying ticket status without holding the
execution lock.

### Changes to `create_ticket`

Before creating a ticket, `create_ticket` must check the sprint's current phase
in the state database. Ticket creation is only allowed when the sprint is in the
`ticketing` phase or later (`ticketing`, `executing`, `closing`). If the sprint
is in an earlier phase (`planning-docs`, `architecture-review`,
`stakeholder-review`), the tool must refuse with a clear error message that:

- States what phase the sprint is currently in.
- Explains what must happen before tickets can be created (e.g., "Sprint 002 is
  in phase 'architecture-review'. Tickets cannot be created until the sprint
  reaches the 'ticketing' phase. The architecture review and stakeholder
  approval gates must pass first.").

If the state database does not exist or the sprint is not registered, ticket
creation proceeds without enforcement (graceful degradation for sprints created
before the state DB existed).

### Changes to `update_ticket_status`

During the `executing` phase, `update_ticket_status` must verify that the sprint
holds the execution lock before allowing status changes. This prevents ticket
work from proceeding on a sprint that has not formally entered execution.

The check applies by resolving which sprint the ticket belongs to (from the file
path), then checking the lock holder. If the sprint does not hold the lock, the
tool refuses with a clear error.

If the state database does not exist or the sprint is not registered, the tool
proceeds without enforcement (graceful degradation).

## Acceptance Criteria

- [ ] `create_ticket` checks the sprint phase before creating a ticket
- [ ] `create_ticket` refuses with a clear error if the sprint is in `planning-docs`, `architecture-review`, or `stakeholder-review`
- [ ] `create_ticket` allows creation in `ticketing`, `executing`, or `closing` phases
- [ ] `create_ticket` error message identifies the current phase and what must happen to proceed
- [ ] `create_ticket` degrades gracefully if the state DB or sprint registration does not exist
- [ ] `update_ticket_status` checks that the sprint holds the execution lock during the `executing` phase
- [ ] `update_ticket_status` refuses with a clear error if the sprint does not hold the lock
- [ ] `update_ticket_status` degrades gracefully if the state DB or sprint registration does not exist
- [ ] Both tools continue to work normally for sprints created before the state DB was introduced
- [ ] Unit tests cover enforcement, graceful degradation, and error messages
