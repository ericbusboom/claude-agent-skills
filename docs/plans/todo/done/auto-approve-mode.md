---
status: done
sprint: '010'
consumed-by: sprint-010
---

# Auto-Approve Mode

## Problem

The process has multiple `AskUserQuestion` breakpoints (sprint close, sprint
plan approval, pre-execution confirmation, etc.). These are valuable for
oversight, but sometimes the stakeholder trusts the agent to run the full
flow without interruption. Currently there's no way to skip all breakpoints
at once.

## Proposed Solution

An "auto-approve" mode that, when active, causes the agent to select the
recommended option at every `AskUserQuestion` breakpoint and continue
without waiting for stakeholder input.

### Activation Methods (pick one or more)

1. **Verbal instruction**: Stakeholder says "auto-approve" or "run without
   asking" in conversation. Agent sets a session flag.
2. **Slash command**: `/auto-approve` toggles the mode on/off for the
   current session.
3. **Touch file**: Create `.claude/auto-approve` (or a frontmatter flag in
   the sprint document). Agent checks for this before each breakpoint.

### Behavior When Active

- At every `AskUserQuestion` breakpoint, the agent selects the first
  (recommended) option automatically.
- The agent logs that it auto-approved (so the stakeholder can see what
  was skipped in the conversation output).
- Mode persists until the stakeholder says "stop auto-approving" or the
  session/sprint ends.

### Safety Considerations

- Should auto-approve cover destructive actions (sprint close, merge, push)?
  Or should some breakpoints be exempt?
- Should auto-approve be sprint-scoped or session-scoped?
- Need clear visual indication that auto-approve is active so the
  stakeholder knows breakpoints are being skipped.
