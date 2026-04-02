---
id: '004'
title: Enforce ticket completion on leave-open
status: done
use-cases: []
depends-on: []
github-issue: ''
todo: enforce-ticket-completion-on-leave-open.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Enforce ticket completion on leave-open

## Description

(What needs to be done and why.)

## Acceptance Criteria

- [x] `### Ticket Completion Rule` section added to `.claude/agents/team-lead/agent.md` under Ticket Completion Rules
- [x] Same section added to `plugin/agents/team-lead/agent.md`
- [x] Ticket completion mandatory note added to `.claude/skills/execute-sprint/SKILL.md`
- [x] Same note added to `plugin/skills/execute-sprint/SKILL.md`
- [x] `uv run pytest` passes with no regressions

## Testing

- **Existing tests to run**: `uv run pytest` (agent instruction change — no new tests needed)
- **New tests to write**: None — this is a documentation/process change only
- **Verification command**: `uv run pytest`
