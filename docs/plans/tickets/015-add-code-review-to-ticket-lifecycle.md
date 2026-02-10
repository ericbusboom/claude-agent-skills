---
id: "015"
title: Add code review gate to ticket lifecycle
status: todo
use-cases: [UC-006]
depends-on: ["012"]
---

# 015: Add Code Review Gate to Ticket Lifecycle

## Description

Update `skills/execute-ticket.md` and `instructions/system-engineering.md`
to include a code review step between testing and documentation. The review
checks for coding standards compliance, security, test coverage, and
acceptance criteria. Issues must be resolved before completion.

## Acceptance Criteria

- [ ] `skills/execute-ticket.md` includes a review step after testing
- [ ] Review checks are defined (standards, security, test coverage, acceptance criteria)
- [ ] Review findings must be resolved before ticket completion
- [ ] `instructions/system-engineering.md` Phase 3 references code review step
