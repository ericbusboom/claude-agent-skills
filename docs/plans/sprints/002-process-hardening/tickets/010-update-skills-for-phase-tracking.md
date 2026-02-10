---
id: "010"
title: Update skills for phase tracking
status: todo
use-cases:
  - SUC-001
  - SUC-002
depends-on:
  - "007"
---

# Update skills for phase tracking

## Description

Update the Claude agent skill definitions and system engineering instructions to
document the new state database, phase model, and review gates introduced by
this sprint. Without these updates, agents will not know to use the new phase
advancement and gate recording tools during sprint planning and closure.

### Skill updates

**`skills/plan-sprint.md`**: Update the sprint planning skill to include steps
for phase advancement. After the planning documents are complete, the skill
should instruct the agent to:

1. Call `advance_sprint_phase` to move from `planning-docs` to
   `architecture-review`.
2. Conduct the architecture review and call `record_gate_result` with the
   outcome.
3. If the architecture review passes, call `advance_sprint_phase` to move to
   `stakeholder-review`.
4. Conduct the stakeholder review and call `record_gate_result` with the
   outcome.
5. If stakeholder approval passes, call `advance_sprint_phase` to move to
   `ticketing`.
6. After tickets are created, call `acquire_execution_lock` and
   `advance_sprint_phase` to move to `executing`.

**`skills/close-sprint.md`**: Update the sprint closure skill to include steps
for phase advancement and lock release. The skill should instruct the agent to:

1. Verify all tickets are done.
2. Call `advance_sprint_phase` to move from `executing` to `closing`.
3. Call `close_sprint` (which internally advances to `done` and releases the
   execution lock).

### Instruction updates

**`instructions/system-engineering.md`**: Add a section documenting:

- The state database (`docs/plans/.clasi.db`) and its purpose.
- The seven-phase lifecycle model.
- The two review gates (architecture review, stakeholder approval).
- The execution lock mechanism.
- How the MCP tools (`get_sprint_phase`, `advance_sprint_phase`,
  `record_gate_result`, `acquire_execution_lock`, `release_execution_lock`)
  are used throughout the lifecycle.

## Acceptance Criteria

- [ ] `skills/plan-sprint.md` includes steps for calling `advance_sprint_phase` at each phase transition
- [ ] `skills/plan-sprint.md` includes steps for calling `record_gate_result` after reviews
- [ ] `skills/plan-sprint.md` includes steps for calling `acquire_execution_lock` before execution
- [ ] `skills/close-sprint.md` includes steps for phase advancement during closure
- [ ] `skills/close-sprint.md` references the execution lock release in `close_sprint`
- [ ] `instructions/system-engineering.md` documents the state database and its location
- [ ] `instructions/system-engineering.md` documents the seven-phase lifecycle model
- [ ] `instructions/system-engineering.md` documents the review gates and execution lock
- [ ] `instructions/system-engineering.md` lists the five new MCP tools and their usage
- [ ] All updated documents are consistent with the actual tool implementations from tickets 001-007
