---
status: draft
---

# Sprint 008 Use Cases

## SUC-001: Ticket Template Includes Testing Section
Parent: UC-007

- **Actor**: Technical lead (creating tickets via `create_ticket` MCP tool)
- **Preconditions**: Sprint is in the ticketing phase.
- **Main Flow**:
  1. Technical lead calls `create_ticket(sprint_id, title)`.
  2. The generated ticket markdown includes a `## Testing` section with
     placeholder guidance for the implementer.
  3. The implementer fills in the testing section during ticket planning
     (step 2 of execute-ticket) with specific test files, new tests to
     write, and the verification command.
- **Postconditions**: Every new ticket has a testing section by default.
- **Acceptance Criteria**:
  - [ ] `TICKET_TEMPLATE` in `templates.py` includes a `## Testing` section
  - [ ] The section has placeholder text guiding what to fill in
  - [ ] Existing tests for `create_ticket` still pass

## SUC-002: Execute-Ticket References Ticket Testing Section
Parent: UC-007

- **Actor**: AI agent (executing a ticket via execute-ticket skill)
- **Preconditions**: A ticket with a `## Testing` section exists.
- **Main Flow**:
  1. Agent reads the ticket and its testing section.
  2. During the "Run tests" step, the agent follows the testing section's
     guidance to know which tests to run and what new tests to write.
  3. Before marking the ticket done, the agent verifies the testing section's
     requirements are met.
- **Postconditions**: Tests described in the ticket's testing section are
  written and passing.
- **Acceptance Criteria**:
  - [ ] `execute-ticket.md` skill references the ticket's Testing section
  - [ ] Steps 5-6 of execute-ticket are updated to use ticket testing guidance

## SUC-003: Interactive Breakpoint Before Ticket Execution
Parent: UC-009

- **Actor**: Stakeholder (via AskUserQuestion)
- **Preconditions**: Sprint is in executing phase. Tickets have been created
  and approved but execution hasn't started yet.
- **Main Flow**:
  1. The `/next` skill detects that a sprint has todo tickets and execution
     hasn't started.
  2. Before starting ticket execution, it presents an AskUserQuestion with
     options: "Start executing tickets" / "Review tickets first" / Other.
  3. Stakeholder approves, and tickets execute without further interruption.
- **Postconditions**: Stakeholder had a chance to pause before bulk execution.
- **Acceptance Criteria**:
  - [ ] `next.md` skill includes a breakpoint before starting ticket execution
  - [ ] No breakpoints between individual tickets during execution
  - [ ] Breakpoints exist between initial scope and first sprint planning

## SUC-004: Interactive Breakpoint During Sprint Planning
Parent: UC-009

- **Actor**: Stakeholder (via AskUserQuestion)
- **Preconditions**: Sprint is being planned (between planning-docs and
  stakeholder-review phases).
- **Main Flow**:
  1. After architecture review passes, the plan-sprint skill presents
     the sprint plan to the stakeholder (already exists in step 9).
  2. The `/next` skill includes breakpoints at natural phase transitions
     during planning: after architecture review, after stakeholder review.
- **Postconditions**: Stakeholder can intervene at planning phase boundaries.
- **Acceptance Criteria**:
  - [ ] `plan-sprint.md` or `next.md` includes breakpoints at planning phase
        transitions
  - [ ] No new breakpoints are added between tickets
