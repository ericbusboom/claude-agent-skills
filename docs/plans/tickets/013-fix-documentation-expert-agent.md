---
id: "013"
title: Fix documentation-expert agent tools and SE grounding
status: done
use-cases: [UC-007]
depends-on: []
---

# 013: Fix Documentation-Expert Agent

## Description

Fix the documentation-expert agent: add missing `Write` and `Edit` tools,
and ground it in the SE process so it knows about tickets, ticket plans,
and project instructions.

## Acceptance Criteria

- [ ] `agents/documentation-expert.md` tools include Write and Edit
- [ ] Agent description references the SE process (tickets, ticket plans)
- [ ] Agent knows to read testing and coding standards instructions
- [ ] Agent knows where to find SE artifacts (`docs/plans/`)
