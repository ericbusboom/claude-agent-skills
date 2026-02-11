---
status: draft
---

# Sprint 005 Use Cases

## SUC-001: Rename process and agent
Parent: (none — housekeeping)

- **Actor**: Developer or AI agent
- **Preconditions**: Codebase references "Systems Engineering" and has
  `systems-engineer.md` agent
- **Main Flow**:
  1. Rename `agents/systems-engineer.md` to `agents/technical-lead.md`
  2. Update all references from "Systems Engineering" to "Software Engineering"
     in instructions, agents, skills, init_command.py, and tests
  3. Verify no stale references remain via grep
- **Postconditions**: All naming is consistent with "Software Engineering" and
  "Technical Lead"
- **Acceptance Criteria**:
  - [ ] `agents/technical-lead.md` exists, `agents/systems-engineer.md` does not
  - [ ] `grep -ri "systems.engineer"` returns zero matches (excluding done/ archives)
  - [ ] All tests pass

## SUC-002: Project initiation with overview document
Parent: (none — new capability)

- **Actor**: Stakeholder starting a new project
- **Preconditions**: Repository initialized with `clasi init`
- **Main Flow**:
  1. Stakeholder describes what they want to build (narration)
  2. Product manager agent asks clarifying questions via AskUserQuestion
  3. Agent synthesizes answers into `docs/plans/overview.md`
  4. Overview is linked into `.claude/rules/` and `.github/copilot/instructions/`
- **Postconditions**: A single overview document captures brief, use cases, and
  technical direction; IDE agents can see it
- **Acceptance Criteria**:
  - [ ] `product-manager.md` agent definition exists
  - [ ] `create_overview` produces the combined document
  - [ ] `clasi init` sets up scaffolding for the initiation workflow
  - [ ] Overview is linked into IDE instruction directories

## SUC-003: TODO frontmatter and traceability
Parent: (none — process improvement)

- **Actor**: AI agent managing TODOs
- **Preconditions**: TODO files exist in `docs/plans/todo/`
- **Main Flow**:
  1. When a TODO is created, it gets `status: pending` frontmatter
  2. When a TODO is moved to done, `move_todo_to_done` updates frontmatter
     with `status: done`, `sprint: "NNN"`, and `tickets: [...]`
  3. `list_todos` returns status from frontmatter
- **Postconditions**: Every done TODO traces back to the sprint/tickets that
  addressed it
- **Acceptance Criteria**:
  - [ ] New TODOs get `status: pending` frontmatter
  - [ ] `move_todo_to_done` accepts sprint_id and ticket_ids parameters
  - [ ] Done TODOs have sprint and ticket references in frontmatter
  - [ ] `list_todos` shows status field

## SUC-004: Interactive open questions during planning review
Parent: (none — process improvement)

- **Actor**: Stakeholder reviewing a sprint plan
- **Preconditions**: Sprint technical plan has an "Open Questions" section
- **Main Flow**:
  1. During stakeholder review gate, plan-sprint skill parses open questions
  2. Each question is presented via `AskUserQuestion` with proposed options
  3. Stakeholder's answers are recorded back into the technical plan
  4. Only then does the skill ask for stakeholder approval
- **Postconditions**: All open questions are resolved before sprint proceeds
- **Acceptance Criteria**:
  - [ ] Open questions are parsed from technical plan markdown
  - [ ] Each question presented interactively with options
  - [ ] Answers written back into the technical plan
  - [ ] Stakeholder approval follows question resolution

## SUC-005: Harden instructions against premature ticket creation
Parent: (none — process enforcement)

- **Actor**: AI agent following the SE process
- **Preconditions**: Sprint is in planning-docs phase
- **Main Flow**:
  1. Agent reads sprint planning skill/instructions
  2. Instructions explicitly state: do NOT create tickets until stakeholder
     approves and advances the sprint to ticketing phase
  3. The `create_ticket` MCP tool already enforces this via phase gates, but
     the skill instructions should also make it unambiguous
- **Postconditions**: AI agents do not attempt ticket creation during planning
- **Acceptance Criteria**:
  - [ ] plan-sprint skill explicitly says "do not create tickets yet"
  - [ ] system-engineering (or renamed) instruction reinforces phase ordering
  - [ ] Retroactive frontmatter added to the 4 TODOs moved to done/ without it
