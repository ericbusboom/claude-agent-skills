---
status: done
priority: high
sprint: '010'
consumed-by: sprint-010
---

# Scold Detection and Self-Reflection

## Problem

When the stakeholder corrects or scolds the agent for doing something wrong,
the feedback is valuable but ephemeral — it lives only in the conversation
context and is lost when the session ends. There is no mechanism to capture
what went wrong, why, and how to prevent it from happening again.

This is a project hygiene issue. When CLASI is used in other repos, these
reflections become a feedback loop for improving the process and skills.

## Proposed Solution

### Scold Detection

Add an instruction (high visibility — should appear in every context) that
tells the agent to recognize when the stakeholder is correcting its behavior.
Indicators include:

- Direct correction ("no, that's wrong", "you shouldn't have done that")
- Process critique ("why did you do X instead of Y?", "that's not how it works")
- Frustration signals ("I told you to...", "you keep doing...")

### Self-Reflection Skill

When a scold is detected, the agent should:

1. Acknowledge the correction
2. Produce a self-reflection document capturing:
   - What happened (the agent's action)
   - What should have happened (the correct behavior)
   - Root cause (why the agent went wrong — missing instruction? ambiguous
     skill? ignored existing instruction?)
   - Proposed fix (new instruction, skill update, or process change)
3. Save the reflection to a dedicated directory (e.g., `docs/plans/reflections/`
   rather than `docs/plans/todo/`) so reflections are distinct from feature work

### Visibility

This should be a high-priority instruction that loads in every context —
possibly as a CLAUDE.md rule or a top-level instruction file — so the agent
always has scold detection active regardless of which skill is running.

## Open Questions

1. Where should reflection documents live? `docs/plans/reflections/` vs
   `docs/plans/todo/` with a special tag?
2. Should reflections automatically generate TODOs for process fixes, or
   stay as standalone documents?
3. What level of detail should the reflection include? (minimal vs full
   conversation excerpt)
