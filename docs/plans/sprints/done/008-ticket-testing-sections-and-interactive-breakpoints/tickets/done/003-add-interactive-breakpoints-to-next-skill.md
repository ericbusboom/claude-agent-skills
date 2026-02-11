---
id: '003'
title: Add interactive breakpoints to next skill
status: done
use-cases:
- SUC-003
- SUC-004
depends-on: []
---

# Add interactive breakpoints to next skill

## Description

Update `claude_agent_skills/skills/next.md` to add `AskUserQuestion`
breakpoints at two natural phase boundaries:

1. **Before sprint planning**: When the determined action is "Plan a sprint"
   (technical plan exists, no active sprint), ask the stakeholder before
   proceeding.
2. **Before first ticket execution**: When the determined action is "Execute
   next ticket" and no tickets are in-progress or done yet (all are todo),
   ask the stakeholder before starting bulk execution.

Critically, do NOT add breakpoints between individual tickets. Once
execution starts, tickets proceed without interruption.

## Acceptance Criteria

- [ ] The skill includes a breakpoint step before "Plan a sprint"
- [ ] The skill includes a breakpoint step before first ticket execution
      (when all tickets are todo)
- [ ] The skill explicitly states no breakpoints between individual tickets
- [ ] Mid-execution (some tickets done/in-progress) proceeds without asking
- [ ] Sprint closing proceeds without asking

## Testing

- **Existing tests to run**: `uv run pytest` (full suite)
- **New tests to write**: None (content-only markdown change)
- **Verification command**: `uv run pytest`
