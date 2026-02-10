---
id: '003'
title: Integrate TODOs into sprint planning
status: in-progress
use-cases:
- SUC-003
depends-on:
- '001'
---

# Integrate TODOs into sprint planning

## Description

Update the `skills/plan-sprint.md` skill to include a TODO mining step.
During sprint planning, the project-manager agent should:

1. Scan `docs/plans/todo/` for relevant ideas
2. Discuss relevant TODOs with the stakeholder
3. Incorporate selected TODOs into the sprint scope
4. Move consumed TODO files to `docs/plans/todo/done/`

## Acceptance Criteria

- [x] `skills/plan-sprint.md` includes TODO mining step
- [x] Step describes scanning, discussing, incorporating, and archiving
- [x] Consumed TODO files move to `docs/plans/todo/done/`
