---
id: '001'
title: Simplify next.md to thin dispatcher
status: done
use-cases:
- SUC-002
depends-on: []
---

# Simplify next.md to thin dispatcher

## Description

Remove the entire "Breakpoint check" step 3 and the `IMPORTANT` note added
in sprint 008. `next.md` becomes a 3-step thin dispatcher: assess state,
determine action, invoke skill. No `AskUserQuestion` logic remains.

## Acceptance Criteria

- [ ] `next.md` has exactly 3 steps
- [ ] No `AskUserQuestion` references in `next.md`
- [ ] No `IMPORTANT` note about breakpoints between tickets
- [ ] Step 1: run project-status
- [ ] Step 2: determine next action (6 conditions)
- [ ] Step 3: execute using appropriate skill and agent

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: None (content-only markdown change)
- **Verification command**: `uv run pytest`
