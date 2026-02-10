---
id: "016"
title: Add error recovery patterns to SE instructions
status: todo
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

- [ ] SE instructions include an "Error Recovery" section
- [ ] Covers test failure recovery (diagnose, fix, re-run)
- [ ] Covers plan gap recovery (update plan, escalate if architectural)
- [ ] Covers ticket splitting (when and how to split oversized tickets)
- [ ] Covers escalation to human for unresolvable issues
