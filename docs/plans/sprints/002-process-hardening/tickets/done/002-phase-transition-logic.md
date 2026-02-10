---
id: "002"
title: Phase transition logic
status: done
use-cases:
  - SUC-001
depends-on:
  - "001"
---

# Phase transition logic

## Description

Add the `advance_phase(db_path, sprint_id)` function to `state_db.py`. This
function validates that the current phase's exit conditions are met before
advancing the sprint to the next phase. If conditions are not met, it raises
an error explaining exactly what is missing.

The sprint lifecycle has seven phases in strict order:

1. `planning-docs` -- sprint directory created, planning docs being written
2. `architecture-review` -- docs complete, architecture review in progress
3. `stakeholder-review` -- arch review passed, awaiting stakeholder approval
4. `ticketing` -- approved, tickets being created
5. `executing` -- tickets being implemented
6. `closing` -- all tickets done, closing the sprint
7. `done` -- sprint archived

### Transition rules

Each transition has specific gate conditions:

| From | To | Gate Condition |
|------|----|----------------|
| `planning-docs` | `architecture-review` | None (agent decides docs are ready) |
| `architecture-review` | `stakeholder-review` | `architecture_review` gate result = `passed` |
| `stakeholder-review` | `ticketing` | `stakeholder_approval` gate result = `passed` |
| `ticketing` | `executing` | At least one ticket exists AND execution lock acquired |
| `executing` | `closing` | All tickets in `done` status |
| `closing` | `done` | Sprint directory moved to `done/` (sprint archived) |

The function must:

- Look up the sprint's current phase in the database.
- Determine the next phase in the ordered list.
- Check whether the gate condition for the current-to-next transition is satisfied.
- If satisfied, update the sprint's `phase` and `updated_at` in the database.
- If not satisfied, raise a descriptive error listing what conditions are unmet.
- If the sprint is already in `done`, raise an error (cannot advance past done).

Skipping phases is not possible -- the function always advances exactly one step.

## Acceptance Criteria

- [ ] `advance_phase(db_path, sprint_id)` is added to `state_db.py`
- [ ] Phase order is enforced: `planning-docs` -> `architecture-review` -> `stakeholder-review` -> `ticketing` -> `executing` -> `closing` -> `done`
- [ ] `planning-docs` -> `architecture-review` succeeds with no gate check
- [ ] `architecture-review` -> `stakeholder-review` requires `architecture_review` gate = `passed`
- [ ] `stakeholder-review` -> `ticketing` requires `stakeholder_approval` gate = `passed`
- [ ] `ticketing` -> `executing` requires at least one ticket AND execution lock held by this sprint
- [ ] `executing` -> `closing` requires all tickets to have status `done`
- [ ] `closing` -> `done` requires the sprint to be archived (directory in `done/`)
- [ ] Attempting to advance past `done` raises a clear error
- [ ] Attempting to advance when conditions are unmet raises an error listing the unmet conditions
- [ ] The sprint's `updated_at` timestamp is updated on successful advance
- [ ] Skipping phases is not possible (always advances exactly one step)
- [ ] Unit tests cover each transition and each failure mode
