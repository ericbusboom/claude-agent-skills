---
status: draft
---

# Sprint 009 Use Cases

## SUC-001: Stakeholder Confirms Before Sprint Close
Parent: UC-009

- **Actor**: Stakeholder (via AskUserQuestion)
- **Preconditions**: All tickets in the sprint are done.
- **Main Flow**:
  1. close-sprint skill verifies all tickets are done.
  2. Skill presents a summary of completed tickets and asks the
     stakeholder to confirm closing.
  3. Stakeholder confirms. Skill proceeds with merge, archive, tag, push.
- **Postconditions**: Stakeholder had a chance to review before
  irreversible actions.
- **Acceptance Criteria**:
  - [ ] `close-sprint.md` has an AskUserQuestion between steps 2 and 3
  - [ ] The breakpoint presents a summary of completed tickets

## SUC-002: next.md Is a Thin Dispatcher
Parent: UC-009

- **Actor**: AI agent (invoking `/next`)
- **Preconditions**: User invokes `/next`.
- **Main Flow**:
  1. `/next` runs project-status to assess state.
  2. `/next` determines the next action.
  3. `/next` invokes the appropriate skill — no AskUserQuestion.
- **Postconditions**: The invoked skill handles its own breakpoints.
- **Acceptance Criteria**:
  - [ ] `next.md` has no AskUserQuestion or breakpoint logic
  - [ ] `next.md` is 3 steps: assess state, determine action, invoke skill

## SUC-003: Stakeholder Confirms Before First Ticket Execution
Parent: UC-009

- **Actor**: Stakeholder (via AskUserQuestion)
- **Preconditions**: Sprint is in executing phase, all tickets are todo.
- **Main Flow**:
  1. plan-sprint skill finishes setting sprint status to active.
  2. Before handing off to ticket execution, skill asks stakeholder to
     confirm starting execution.
  3. Stakeholder confirms. Execution proceeds without further breakpoints
     between tickets.
- **Postconditions**: Stakeholder confirmed before bulk ticket execution.
- **Acceptance Criteria**:
  - [ ] `plan-sprint.md` has an AskUserQuestion after step 14
  - [ ] No breakpoints between individual tickets

## SUC-004: Approval Steps Use Explicit AskUserQuestion
Parent: UC-009

- **Actor**: Stakeholder (via AskUserQuestion)
- **Preconditions**: Skill reaches an approval gate step.
- **Main Flow**:
  1. Skill reaches an approval step (e.g., stakeholder review gate).
  2. Skill presents a structured `AskUserQuestion` with concrete options
     (e.g., "Approve" / "Request changes").
  3. Stakeholder selects an option. Skill proceeds accordingly.
- **Postconditions**: All approval steps use the same explicit mechanism.
- **Acceptance Criteria**:
  - [ ] `plan-sprint.md` step 10 uses `AskUserQuestion` with options
  - [ ] `project-initiation.md` step 5 uses `AskUserQuestion` with options
  - [ ] No approval steps use vague "wait for approval" wording
