---
status: draft
---

# Sprint 009 Technical Plan

## Architecture Overview

This sprint redistributes breakpoint logic from `next.md` into the
individual skills that own the actions. All changes are content-only
markdown — no Python code changes.

Design principle: **each skill owns its own breakpoints**. `next.md` is
a thin dispatcher (assess state, invoke skill). If a skill is invoked
directly, its breakpoints still fire.

## Component Design

### Component: Simplify next.md

**Use Cases**: SUC-002

Remove the entire "Breakpoint check" step 3 added in sprint 008. The
skill becomes:

```markdown
1. Run the **project-status** skill to understand current state.
2. Based on the current stage, determine the next action:
   - No brief → Start requirements elicitation
   - Brief but no use cases → Continue requirements
   - Use cases but no technical plan → Start architecture
   - Technical plan, no sprint → Plan a sprint
   - Active sprint with todo tickets → Execute next ticket
   - All tickets done → Close the sprint
3. Begin executing the determined next action using the appropriate
   skill and agent.
```

Also remove the `IMPORTANT` note about no breakpoints between tickets
(that rule now lives in plan-sprint's step 15 note).

### Component: Add breakpoint to close-sprint.md

**Use Cases**: SUC-001

Insert a new step between current steps 2 and 3. The new step:

```markdown
3. **Confirm with stakeholder**: Present a summary of the sprint —
   list the completed tickets and key changes. Use `AskUserQuestion`:
   - "Close sprint and merge to main" (recommended)
   - "Review completed work first"

   If the stakeholder chooses to review, present the full sprint details
   and stop. Otherwise proceed with closing.
```

Renumber subsequent steps (old 3→4, 4→5, ... 10→11).

### Component: Add breakpoint to plan-sprint.md

**Use Cases**: SUC-003

Add a new step 15 after current step 14 (set sprint status):

```markdown
15. **Confirm before execution**: Present the list of tickets to the
    stakeholder. Use `AskUserQuestion`:
    - "Start executing tickets" (recommended)
    - "Review tickets first"

    If the stakeholder chooses to review, list the tickets and stop.
    Otherwise proceed. **Do NOT ask again between individual tickets** —
    once execution starts, tickets proceed without interruption.
```

### Component: Explicit AskUserQuestion in approval steps

**Use Cases**: SUC-004

Two existing approval steps use vague "wait for approval" wording instead of
specifying `AskUserQuestion`. Update both to match the explicit pattern used
elsewhere.

**plan-sprint.md step 10** — replace current text with:

```markdown
10. **Stakeholder review gate**: Present the sprint plan and architecture
    review to the stakeholder. Use `AskUserQuestion`:
    - "Approve sprint plan" (recommended)
    - "Request changes"

    If the stakeholder requests changes, revise and re-present. Only proceed
    when approved.
    - Call `record_gate_result` with gate `stakeholder_approval` and result
      `passed` or `failed`.
```

**project-initiation.md step 5** — replace current text with:

```markdown
5. **Stakeholder review**: Present the completed overview to the stakeholder.
   Use `AskUserQuestion`:
   - "Approve overview" (recommended)
   - "Request changes"

   If the stakeholder requests changes, revise and re-present. Only proceed
   when approved.
```

## Decisions

**"Before sprint planning" breakpoint (next.md step 3a) — intentionally
dropped, not redistributed.**

The architecture review flagged that `next.md` step 3a's "before sprint
planning" breakpoint has no target in the redistribution. This is
intentional:

1. Sprint planning is always triggered by explicit stakeholder intent —
   either via `/next` (where the user asked "what's next?") or by directly
   invoking `/plan-sprint`.
2. `plan-sprint.md` already has breakpoints at steps 8 (conditional, after
   architecture review) and 10 (stakeholder review gate) before any
   irreversible actions.
3. Adding "are you sure you want to plan?" at step 1 after the stakeholder
   just asked to plan is redundant and annoying.

The other two breakpoints (before sprint close, before first ticket
execution) ARE redistributed because they guard irreversible actions
(merge/push, bulk ticket execution) that happen without explicit
stakeholder trigger.
