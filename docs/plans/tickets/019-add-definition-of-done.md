---
id: "019"
title: Add definition of done to SE instructions
status: todo
use-cases: [UC-006, UC-007]
depends-on: ["011", "012", "015"]
---

# 019: Add Definition of Done to SE Instructions

## Description

Add a "Definition of Done" section to `instructions/system-engineering.md`
that consolidates all completion requirements: acceptance criteria met,
tests passing, code review passed, documentation updated, git committed,
no new warnings. This replaces the ad-hoc completion checks.

## Acceptance Criteria

- [ ] SE instructions include a "Definition of Done" section
- [ ] DoD lists all required gates (tests, review, docs, git, acceptance criteria)
- [ ] "Completing a Ticket" section references the DoD
- [ ] project-manager agent references the DoD when verifying completion
