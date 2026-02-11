---
id: '002'
title: Auto-approve mode instruction
status: in-progress
use-cases:
- SUC-002
depends-on: []
---

# Auto-approve mode instruction

## Description

Create an always-on instruction at `.claude/rules/auto-approve.md` that
defines auto-approve mode behavior. When the stakeholder says "auto-approve"
or similar, the agent selects the recommended (first) option at every
`AskUserQuestion` breakpoint automatically, logging each auto-approval.

Session-scoped only — does not persist across conversations.

## Acceptance Criteria

- [ ] `.claude/rules/auto-approve.md` exists
- [ ] Instruction specifies activation phrases ("auto-approve", "run without asking")
- [ ] Instruction specifies deactivation ("stop auto-approving")
- [ ] Instruction says to select first (recommended) option
- [ ] Instruction says to log each auto-approval visibly

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: None (instruction-only change)
- **Verification command**: `uv run pytest`
