---
id: "014"
title: Ground python-expert agent in SE process
status: done
use-cases: [UC-007]
depends-on: []
---

# 014: Ground Python-Expert Agent in SE Process

## Description

Update the python-expert agent to be aware of the SE process: it should
know about the ticket it's working on, the ticket plan, testing instructions,
coding standards, and acceptance criteria. Replace the generic description
with one grounded in the workflow.

## Acceptance Criteria

- [x] `agents/python-expert.md` references tickets and ticket plans
- [x] Agent knows to read the ticket plan before implementing
- [x] Agent references testing instructions and coding standards
- [x] Agent knows to satisfy acceptance criteria from the ticket
- [x] Agent knows where to find SE artifacts (`docs/plans/`)
