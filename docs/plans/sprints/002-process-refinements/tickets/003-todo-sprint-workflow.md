---
id: "003"
title: Integrate TODOs into sprint planning workflow
status: todo
use-cases: [SUC-003]
depends-on: ["001"]
---

# Integrate TODOs into Sprint Planning Workflow

## Description

Update the plan-sprint skill and related process documentation so that
sprint planning includes mining the TODO directory for relevant ideas.
When a TODO is incorporated into a sprint, the TODO file moves to
`docs/plans/todo/done/`.

## Changes Required

1. Update `skills/plan-sprint.md`:
   - Add a step early in the workflow: "Scan `docs/plans/todo/` for
     files. Read each TODO and assess relevance to the sprint being
     planned."
   - Add a step: "Discuss relevant TODOs with the stakeholder. Confirm
     which should be included in the sprint scope."
   - Add a step at sprint finalization: "Move consumed TODO files to
     `docs/plans/todo/done/`."

2. Update `instructions/system-engineering.md`:
   - In the Sprint section, reference TODO mining as part of sprint
     planning.

3. Update the sprint template to include a "Source TODOs" section
   that lists which TODO files were consumed for traceability.

## Acceptance Criteria

- [ ] `skills/plan-sprint.md` includes TODO mining steps
- [ ] Sprint planning scans the TODO directory
- [ ] Stakeholder is consulted about which TODOs to include
- [ ] Consumed TODO files are moved to `docs/plans/todo/done/`
- [ ] Sprint document includes a "Source TODOs" section
