---
id: "016"
title: Add error recovery patterns to SE instructions
status: done
use-cases: [UC-008]
depends-on: []
---

# 016: Add Error Recovery Patterns to SE Instructions

## Description

Add an error recovery section to `instructions/system-engineering.md`
covering what agents should do when things go wrong: test failures, plan
gaps discovered during implementation, tickets that are too large, and
unresolvable blockers requiring human escalation.

## Acceptance Criteria

- [x] SE instructions include an "Error Recovery" section
- [x] Covers test failure recovery (diagnose, fix, re-run)
- [x] Covers plan gap recovery (update plan, escalate if architectural)
- [x] Covers ticket splitting (when and how to split oversized tickets)
- [x] Covers escalation to human for unresolvable issues
