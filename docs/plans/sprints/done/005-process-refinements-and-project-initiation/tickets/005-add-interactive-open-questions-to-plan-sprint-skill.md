---
id: "005"
title: Add interactive open questions to plan-sprint skill
status: todo
use-cases: [SUC-004]
depends-on: []
---

# Add interactive open questions to plan-sprint skill

## Description

Update `skills/plan-sprint.md` to add a step before stakeholder approval
that parses the `## Open Questions` section from the technical plan, presents
each question to the stakeholder via `AskUserQuestion`, and writes the answers
back into the technical plan as a `## Decisions` section.

This is a skill-only change — no Python code needed.

## Acceptance Criteria

- [ ] `plan-sprint.md` includes step to parse open questions from technical plan
- [ ] Step presents each question via `AskUserQuestion` with options
- [ ] Answers are recorded back into the technical plan
- [ ] Open Questions section is replaced with Decisions section
- [ ] Step occurs before stakeholder approval gate
