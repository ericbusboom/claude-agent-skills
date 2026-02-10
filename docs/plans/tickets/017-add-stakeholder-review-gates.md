---
id: "017"
title: Add stakeholder review gates between phases
status: todo
use-cases: [UC-009]
depends-on: []
---

# 017: Add Stakeholder Review Gates Between Phases

## Description

Update `instructions/system-engineering.md` and `agents/project-manager.md`
to require stakeholder approval between phases. The project-manager must
present each phase's output and wait for approval before advancing.

## Acceptance Criteria

- [ ] SE instructions define review gates after Phase 1a, 1b, and 2
- [ ] Each gate specifies what is presented and what approval means
- [ ] project-manager agent description includes pause-for-approval behavior
- [ ] Revision cycle is documented (stakeholder requests changes → agent revises → re-present)
