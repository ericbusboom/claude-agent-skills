---
id: "030"
title: Create plan-sprint skill
status: done
use-cases: [UC-010, UC-011]
depends-on: ["027", "028"]
---

# Create Plan Sprint Skill

Create `skills/plan-sprint.md` — a skill for creating a sprint from a
stakeholder conversation.

## Description

This skill covers the sprint planning workflow: capture stakeholder goals,
create the sprint document, create the sprint branch, get architecture
review, get stakeholder approval, then delegate ticket creation.

## Acceptance Criteria

- [ ] `skills/plan-sprint.md` exists with correct YAML frontmatter
- [ ] Skill defines the sprint document format (YAML frontmatter + content)
- [ ] Skill includes steps: create document, create branch, architecture
      review, stakeholder approval, create tickets
- [ ] Skill references architecture-reviewer agent for plan review
- [ ] Skill references systems-engineer for ticket creation
- [ ] Sprint numbering convention is defined (NNN, sequential)
