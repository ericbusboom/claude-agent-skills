---
id: "018"
title: Add git commit step to ticket lifecycle
status: done
use-cases: [UC-005]
depends-on: ["011"]
---

# 018: Add Git Commit Step to Ticket Lifecycle

## Description

Update `skills/execute-ticket.md` and `instructions/system-engineering.md`
to include a git commit step at ticket completion. The commit message should
follow the conventions defined in the git workflow instruction.

## Acceptance Criteria

- [x] `skills/execute-ticket.md` includes a git commit step before moving ticket to done
- [x] Commit message format references ticket ID
- [x] `instructions/system-engineering.md` "Completing a Ticket" section includes commit step
