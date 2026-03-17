---
id: 009
title: Move Breakpoints Into Skills
status: done
branch: sprint/009-move-breakpoints-into-skills
use-cases:
- UC-009
---

# Sprint 009: Move Breakpoints Into Skills

## Goals

1. Remove breakpoint logic from `next.md` — make it a thin dispatcher.
2. Add a stakeholder confirmation breakpoint to `close-sprint.md` before
   irreversible actions (merge, archive, push).
3. Move the "before first ticket execution" breakpoint into
   `plan-sprint.md` at the end of the planning flow.
4. Make existing approval steps explicit — add `AskUserQuestion` to
   `plan-sprint.md` step 10 and `project-initiation.md` step 5.

## Problem

Sprint 008 added `AskUserQuestion` breakpoints to `next.md`, but this is
the wrong location. Skills can be invoked directly (not via `/next`), so
breakpoints in `next.md` get bypassed. Additionally, `close-sprint.md`
has no breakpoint at all — it proceeds from "verify tickets done" straight
through merge, archive, tag, and push without stakeholder confirmation.

## Solution

- Strip `next.md` back to a thin dispatcher: assess state, invoke skill.
- Add a breakpoint to `close-sprint.md` between steps 2 and 3.
- Move the "before first execution" breakpoint to `plan-sprint.md` after
  step 14 (the natural end of planning, right before execution begins).
- Make `plan-sprint.md` step 10 and `project-initiation.md` step 5 use
  explicit `AskUserQuestion` instead of vague "wait for approval" wording.
- Leave `execute-ticket.md` unchanged (operates within approved scope).

## Success Criteria

- `next.md` has no `AskUserQuestion` logic.
- `close-sprint.md` asks for confirmation before merging.
- `plan-sprint.md` asks before starting ticket execution.
- `plan-sprint.md` step 10 explicitly uses `AskUserQuestion`.
- `project-initiation.md` step 5 explicitly uses `AskUserQuestion`.
- All breakpoints are in the skills that own the actions.
- 171 tests still pass.

## Scope

### In Scope

- `next.md` — remove breakpoint step 3
- `close-sprint.md` — add breakpoint between steps 2 and 3
- `plan-sprint.md` — add breakpoint after step 14
- `plan-sprint.md` — make step 10 use explicit `AskUserQuestion`
- `project-initiation.md` — make step 5 use explicit `AskUserQuestion`

### Out of Scope

- Adding breakpoints to `execute-ticket.md` (not needed)
- Python code changes (all markdown content)
- New tests (content-only changes)

## Test Strategy

- All changes are content-only markdown. Run `uv run pytest` to verify
  no regressions. No new tests needed.

## Architecture Notes

- Design principle: each skill owns its own breakpoints. `next.md` is
  only responsible for state assessment and dispatch.
- `plan-sprint.md` already has breakpoints at steps 8 and 10. The new
  step 15 breakpoint covers the transition into execution.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, technical plan)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

- #001 Simplify next.md to thin dispatcher (SUC-002)
- #002 Add breakpoint to close-sprint.md (SUC-001)
- #003 Add breakpoint to plan-sprint.md (SUC-003)
- #004 Explicit AskUserQuestion in approval steps (SUC-004)
