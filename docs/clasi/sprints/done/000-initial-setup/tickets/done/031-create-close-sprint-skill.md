---
id: "031"
title: Create close-sprint skill
status: done
use-cases: [UC-013]
depends-on: ["028", "029"]
---

# Create Close Sprint Skill

Create `skills/close-sprint.md` — a skill for closing a completed sprint.

## Description

This skill covers sprint closure: verify all tickets are done, merge the
sprint branch, update the sprint document, and archive it.

## Acceptance Criteria

- [ ] `skills/close-sprint.md` exists with correct YAML frontmatter
- [ ] Skill verifies all sprint tickets satisfy Definition of Done
- [ ] Skill sets sprint status to `done`
- [ ] Skill merges sprint branch to main
- [ ] Skill moves sprint document to `docs/plans/sprints/done/`
- [ ] Skill reports sprint completion summary
