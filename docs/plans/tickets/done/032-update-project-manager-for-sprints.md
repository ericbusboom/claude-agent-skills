---
id: "032"
title: Update project-manager for sprint coordination
status: done
use-cases: [UC-010, UC-013]
depends-on: ["026", "027", "028"]
---

# Update Project Manager for Sprint Coordination

Update `agents/project-manager.md` to add sprint coordination and reference
the new review agents.

## Description

The project-manager needs to know about sprints as the primary working mode
after initial setup. It should coordinate sprint lifecycle, delegate
architecture reviews to architecture-reviewer, delegate code reviews to
code-reviewer, and track sprint state.

## Acceptance Criteria

- [ ] project-manager delegation map includes architecture-reviewer and
      code-reviewer
- [ ] "How You Work" section includes sprint state detection (check for
      active sprints in `docs/plans/sprints/`)
- [ ] Sprint lifecycle is described: plan → execute → close
- [ ] PM delegates architecture review during sprint planning
- [ ] PM delegates code review during ticket execution
- [ ] "Phase" references are updated to "Stage" (from ticket 028)
- [ ] Sprint is positioned as the default working mode after initial setup
