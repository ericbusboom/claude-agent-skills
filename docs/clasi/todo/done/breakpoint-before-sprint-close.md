---
status: done
sprint: 009
---

# Breakpoints Belong in Skills, Not in next.md

## Design principle

`next.md` should be a thin dispatcher: assess the current state using
the process, then invoke the appropriate skill. It should NOT contain
breakpoint logic — that belongs in the skills themselves.

Each skill is responsible for pausing at the right moments. Skills must
be self-contained because they can be invoked directly (not via `/next`).

## What needs to change

### 1. Simplify `next.md`

Remove the entire "Breakpoint check" step (step 3) that was added in
sprint 008. The skill should just be:

1. Run project-status to assess current state
2. Determine the next action based on the process
3. Invoke the appropriate skill

No `AskUserQuestion` logic in `next.md` at all.

### 2. Add breakpoint to `close-sprint.md`

Between steps 2 (verify all tickets done) and 3 (advance to closing):

- Present a summary of completed tickets
- `AskUserQuestion`: "Close sprint and merge to main?" /
  "Review completed work first"

### 3. Add breakpoint to `plan-sprint.md` at start

The "before sprint planning" breakpoint currently in `next.md` step 3a
should move into `plan-sprint.md` as a new step 1 (or step 0):

- `AskUserQuestion`: "Plan a new sprint?" / "Review project status first"

Or this may already be covered by the stakeholder conversation that
triggers plan-sprint. Evaluate whether it's needed.

### 4. Evaluate execute-ticket breakpoint

The "before first ticket execution" breakpoint in `next.md` step 3b
needs a home. Options:

- Add it to `plan-sprint.md` after step 14 (set sprint status) — since
  plan-sprint is what transitions into execution
- Or keep it as a one-time check at the start of the first
  execute-ticket invocation

### 5. Audit plan-sprint.md

Already has breakpoints at steps 8 (conditional, after arch review) and
10 (stakeholder review gate). These are correct and stay.

## Skills to update

- `next.md` — remove breakpoint logic, make it a thin dispatcher
- `close-sprint.md` — add breakpoint between steps 2 and 3
- `plan-sprint.md` — possibly absorb the "before first execution" check
- `execute-ticket.md` — no changes needed (operates within approved scope)
