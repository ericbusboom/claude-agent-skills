---
status: draft
---

# Sprint 008 Technical Plan

## Architecture Overview

This sprint makes two independent changes to the skill/template layer:

1. **Ticket testing section**: Add a `## Testing` section to the ticket
   template and update the `execute-ticket` skill to reference it.
2. **Interactive breakpoints**: Update the `next` and `plan-sprint` skills
   to use `AskUserQuestion` at natural phase boundaries (but never between
   individual tickets).

Both changes are content-only (markdown templates and skill definitions).
The only Python change is adding lines to `TICKET_TEMPLATE` in
`templates.py`.

## Component Design

### Component: Ticket Template Update (`claude_agent_skills/templates.py`)

**Use Cases**: SUC-001

The `TICKET_TEMPLATE` string currently has `## Description` and
`## Acceptance Criteria` sections. Add a `## Testing` section after
Acceptance Criteria with placeholder guidance:

```markdown
## Testing

- **Existing tests to run**: (list test files/commands to verify no regressions)
- **New tests to write**: (describe tests that validate this ticket's changes)
- **Verification command**: `uv run pytest`
```

This guides the implementer (during ticket planning, execute-ticket step 2)
to specify what testing is expected.

### Component: Execute-Ticket Skill Update (`claude_agent_skills/skills/execute-ticket.md`)

**Use Cases**: SUC-002

Update steps 5 and 6 to reference the ticket's `## Testing` section:

- Step 5 becomes: "**Write tests**: Read the ticket's `## Testing` section
  for guidance on which new tests to write and where to place them. Create
  tests as specified in the plan, following the testing instructions (unit
  tests in `tests/unit/`, system tests in `tests/system/`, dev tests in
  `tests/dev/`)."
- Step 6 becomes: "**Run tests**: Execute the verification command from the
  ticket's `## Testing` section (default: `uv run pytest`). Also run any
  existing tests listed in the Testing section to verify no regressions.
  All tests must pass."

### Component: Next Skill Breakpoints (`claude_agent_skills/skills/next.md`)

**Use Cases**: SUC-003, SUC-004

Update the `next` skill to add `AskUserQuestion` breakpoints. The updated
logic after step 1 (run project-status):

```
2. Based on the current stage, determine the next action:
   - ...existing cases...

3. **Breakpoint check** — before executing the determined action, check:

   a. If the action is "Plan a sprint" (technical plan exists, no active
      sprint): present AskUserQuestion with options:
      - "Plan a new sprint" (recommended)
      - "Review project status first"

   b. If the action is "Execute next ticket" AND no tickets are
      in-progress or done yet (all are todo — first ticket of the sprint):
      present AskUserQuestion with options:
      - "Start executing tickets" (recommended)
      - "Review tickets first"

   c. Otherwise (mid-execution, closing, etc.): proceed without asking.

4. Execute the determined action using the appropriate skill and agent.
```

Key rule: **Do NOT add breakpoints between individual tickets.** Once
execution starts, tickets proceed without interruption until all are done.

### Component: Plan-Sprint Skill Breakpoints (`claude_agent_skills/skills/plan-sprint.md`)

**Use Cases**: SUC-004

The plan-sprint skill already has interactive breakpoints at step 8
(resolve open questions via AskUserQuestion) and step 9 (stakeholder
review gate). Add a conditional breakpoint after architecture review:

- **After step 7** (advance to stakeholder-review): If the technical plan
  has NO `## Open Questions` section (or the section is empty), present
  an `AskUserQuestion` asking: "Architecture review passed. Proceed to
  stakeholder review?" with options:
  - "Continue to stakeholder review" (recommended)
  - "Review architecture feedback first"
- If open questions DO exist, proceed directly to step 8 (which already
  presents AskUserQuestion for each question — no double-checking).

## Test Verification

Add a test `test_ticket_template_includes_testing_section` to
`tests/system/test_artifact_tools.py` that:
1. Creates a ticket via the MCP tool
2. Verifies the content includes `## Testing`
3. Verifies the section includes the expected placeholders:
   - "Existing tests to run"
   - "New tests to write"
   - "Verification command"

Also add a unit-level check in the template tests (if they exist) that
`TICKET_TEMPLATE` itself contains the `## Testing` section.

## Decisions

No open questions — the architecture review's recommendations have been
incorporated into this plan.
