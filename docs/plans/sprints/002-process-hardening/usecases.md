---
status: draft
sprint: "002"
---

# Sprint 002 Use Cases

## SUC-001: Enforce Sprint Phase Transitions
Parent: UC-004

- **Actor**: AI agent (any)
- **Preconditions**: A sprint exists in the state database.
- **Main Flow**:
  1. Agent attempts to advance the sprint to the next phase (e.g., from
     `planning-docs` to `architecture-review`).
  2. MCP tool checks whether the current phase's exit conditions are met.
  3. If conditions are met, phase advances and the database is updated.
  4. If conditions are not met, the tool returns an error explaining what
     is missing.
- **Postconditions**: Sprint is in the correct phase. Skipping is not possible.
- **Acceptance Criteria**:
  - [ ] Phase transitions are validated before execution
  - [ ] Cannot skip from `planning-docs` to `ticketing`
  - [ ] Error messages explain what conditions are unmet
  - [ ] Phase history is recorded with timestamps

## SUC-002: Record Review Gate Results
Parent: UC-004

- **Actor**: AI agent (project-manager)
- **Preconditions**: Sprint is in `architecture-review` or `stakeholder-review`
  phase.
- **Main Flow**:
  1. Agent completes the review (architecture review or stakeholder discussion).
  2. Agent calls `record_gate_result` with the sprint ID, gate name, and
     result (passed/failed).
  3. MCP tool records the result with a timestamp.
  4. If the gate passed, the sprint can advance to the next phase.
  5. If the gate failed, the agent must address the issues and re-submit.
- **Postconditions**: Gate result is persistently recorded. Sprint can only
  advance if the gate passed.
- **Acceptance Criteria**:
  - [ ] Architecture review result is recorded and queryable
  - [ ] Stakeholder approval result is recorded and queryable
  - [ ] Failed gates block phase advancement
  - [ ] Gate results include timestamps and optional notes

## SUC-003: Prevent Concurrent Sprint Execution
Parent: UC-004

- **Actor**: AI agent (project-manager)
- **Preconditions**: Sprint A is executing. Agent wants to start executing
  sprint B.
- **Main Flow**:
  1. Agent calls `acquire_execution_lock` for sprint B.
  2. MCP tool checks if another sprint holds the lock.
  3. Lock is denied. Tool returns which sprint holds it and since when.
  4. Agent reports to stakeholder that execution must wait.
- **Postconditions**: Only one sprint can execute at a time.
- **Acceptance Criteria**:
  - [ ] Execution lock prevents concurrent execution
  - [ ] Lock holder information is returned when denied
  - [ ] Lock is released when sprint closes
  - [ ] `create_ticket` and `update_ticket_status` check the lock

## SUC-004: Block Ticket Creation Before Approval
Parent: UC-004

- **Actor**: AI agent (systems-engineer)
- **Preconditions**: Sprint exists, planning documents written, but
  stakeholder review has not passed.
- **Main Flow**:
  1. Agent calls `create_ticket` for the sprint.
  2. MCP tool checks the sprint's phase in the database.
  3. Sprint is in `planning-docs` phase (not yet past `stakeholder-review`).
  4. Tool refuses to create the ticket, explaining the sprint has not been
     approved.
- **Postconditions**: No tickets exist for unapproved sprints.
- **Acceptance Criteria**:
  - [ ] `create_ticket` checks sprint phase before creating
  - [ ] Tickets can only be created in `ticketing` phase or later
  - [ ] Clear error message when blocked

## SUC-005: Track Use Case Coverage Across Sprints
Parent: UC-004

- **Actor**: AI agent (project-manager)
- **Preconditions**: Top-level use cases exist. One or more sprints have
  been completed.
- **Main Flow**:
  1. Agent calls `project_status` or a new coverage tool.
  2. Tool reads top-level use cases, then reads each sprint's use cases
     and their `parent` references.
  3. Tool reports which top-level use cases are covered by completed
     sprints, which are in-progress, and which are not yet addressed.
- **Postconditions**: Stakeholder can see overall project coverage.
- **Acceptance Criteria**:
  - [ ] Sprint use cases have a `parent` field in their format
  - [ ] Coverage report lists all top-level use cases with their status
  - [ ] project-status or a new tool exposes this information
