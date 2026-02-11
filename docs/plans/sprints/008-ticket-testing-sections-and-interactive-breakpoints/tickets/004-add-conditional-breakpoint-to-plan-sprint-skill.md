---
id: "004"
title: Add conditional breakpoint to plan-sprint skill
status: todo
use-cases: [SUC-004]
depends-on: []
---

# Add conditional breakpoint to plan-sprint skill

## Description

Update `claude_agent_skills/skills/plan-sprint.md` to add a conditional
`AskUserQuestion` breakpoint after architecture review passes (between
steps 7 and 8):

- If the technical plan has NO `## Open Questions` section (or it's empty),
  present an AskUserQuestion: "Architecture review passed. Proceed to
  stakeholder review?"
- If open questions DO exist, skip the breakpoint and proceed directly to
  step 8 (which already resolves them interactively via AskUserQuestion).

This avoids double-checking the stakeholder when open questions already
provide a natural pause point.

## Acceptance Criteria

- [ ] A new step (or sub-step) exists between current steps 7 and 8
- [ ] The breakpoint fires only when no open questions exist
- [ ] When open questions exist, the skill proceeds directly to step 8
- [ ] The AskUserQuestion offers "Continue to stakeholder review" and
      "Review architecture feedback first" options

## Testing

- **Existing tests to run**: `uv run pytest` (full suite)
- **New tests to write**: None (content-only markdown change)
- **Verification command**: `uv run pytest`
