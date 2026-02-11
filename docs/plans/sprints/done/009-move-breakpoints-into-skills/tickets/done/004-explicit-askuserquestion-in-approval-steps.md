---
id: '004'
title: Explicit AskUserQuestion in approval steps
status: done
use-cases:
- SUC-004
depends-on: []
---

# Explicit AskUserQuestion in approval steps

## Description

Two existing approval steps say "wait for approval" without specifying the
`AskUserQuestion` mechanism. Update both to use explicit `AskUserQuestion`
with concrete options, matching the pattern used in other breakpoint steps.

## Acceptance Criteria

- [ ] `plan-sprint.md` step 10 uses `AskUserQuestion` with "Approve sprint plan" (recommended) and "Request changes"
- [ ] `project-initiation.md` step 5 uses `AskUserQuestion` with "Approve overview" (recommended) and "Request changes"
- [ ] Neither step uses vague "wait for approval" wording

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: None (content-only markdown change)
- **Verification command**: `uv run pytest`
