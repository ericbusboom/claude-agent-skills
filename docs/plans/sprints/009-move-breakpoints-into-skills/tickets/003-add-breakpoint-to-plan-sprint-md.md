---
id: "003"
title: Add breakpoint to plan-sprint.md
status: todo
use-cases: [SUC-003]
depends-on: []
---

# Add breakpoint to plan-sprint.md

## Description

Add a new step 15 after current step 14 (set sprint status). This step
presents the list of tickets to the stakeholder and uses `AskUserQuestion`
to confirm before starting bulk ticket execution. Includes the rule that
once execution starts, no further breakpoints fire between individual
tickets.

## Acceptance Criteria

- [ ] New step 15 uses `AskUserQuestion` with "Start executing tickets" (recommended) and "Review tickets first"
- [ ] Step 15 presents the list of tickets
- [ ] If stakeholder chooses review, skill lists tickets and stops
- [ ] Includes note: "Do NOT ask again between individual tickets"
- [ ] 15 total steps in plan-sprint.md

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: None (content-only markdown change)
- **Verification command**: `uv run pytest`
