---
id: "020"
title: Add decision heuristics to project-manager agent
status: done
use-cases: [UC-008, UC-009]
depends-on: ["016", "017"]
---

# 020: Add Decision Heuristics to Project-Manager Agent

## Description

Update `agents/project-manager.md` with decision-making guidance: how to
prioritize parallel-ready tickets, what to do when blocked, how to handle
scope creep, and when to escalate to the human.

## Acceptance Criteria

- [x] project-manager agent includes ticket prioritization heuristics
- [x] Includes blocker handling guidance
- [x] Includes scope creep handling (new ticket vs. absorb)
- [x] Includes escalation criteria (when to ask the human)
