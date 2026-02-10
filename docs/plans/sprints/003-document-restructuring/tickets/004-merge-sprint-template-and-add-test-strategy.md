---
id: '004'
title: Merge sprint template and add test strategy
status: in-progress
use-cases:
- SUC-004
depends-on: []
---

# Merge sprint template and add test strategy

## Description

Update `SPRINT_TEMPLATE` in `templates.py` to include the brief content
(Problem, Solution, Success Criteria) directly, eliminating the need for a
separate `brief.md` per sprint. Also add a "Test Strategy" section.

Update `create_sprint` in `artifact_tools.py` to stop creating a separate
`brief.md` file.

Update `instructions/testing.md` to reference the sprint-level test strategy
section.

### Template structure after merge

```
sprint.md:
  - Goals
  - Scope (In Scope / Out of Scope)
  - Problem
  - Solution
  - Success Criteria
  - Test Strategy
  - Architecture Notes
  - Definition of Ready
  - Tickets
```

## Acceptance Criteria

- [x] `SPRINT_TEMPLATE` includes Problem, Solution, Success Criteria sections
- [x] `SPRINT_TEMPLATE` includes Test Strategy section
- [x] `SPRINT_BRIEF_TEMPLATE` still exists (for backward compat) but is not
      used by `create_sprint`
- [x] `create_sprint` no longer creates a separate `brief.md`
- [x] `instructions/testing.md` references sprint test strategy
- [x] Existing tests updated for new template output
- [x] New tests verify merged template content
