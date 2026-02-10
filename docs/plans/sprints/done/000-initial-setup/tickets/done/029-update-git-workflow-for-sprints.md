---
id: "029"
title: Update git workflow for sprint branching
status: done
use-cases: [UC-014]
depends-on: []
---

# Update Git Workflow for Sprint Branching

Update `instructions/git-workflow.md` to add sprint-based branching as the
primary branch strategy.

## Description

The current git workflow offers two options (work on main, or feature
branches per ticket). With sprints, the strategy becomes: one branch per
sprint (`sprint/NNN-slug`), all ticket commits go to the sprint branch,
and the branch merges to main when the sprint closes.

## Acceptance Criteria

- [ ] Git workflow instruction adds a sprint branch section
- [ ] Branch naming convention documented: `sprint/NNN-slug`
- [ ] Branch created at sprint start, merged at sprint close
- [ ] Commit message format updated: `<type>: <summary> (#NNN, sprint NNN)`
- [ ] Existing Option A / Option B remain for projects not using sprints
- [ ] Sprint branching is positioned as the recommended approach
