---
id: '002'
title: Add breakpoint to close-sprint.md
status: done
use-cases:
- SUC-001
depends-on: []
---

# Add breakpoint to close-sprint.md

## Description

Insert a new step 3 between current steps 2 (verify tickets done) and 3
(advance to closing phase). The new step presents a summary of completed
tickets and uses `AskUserQuestion` to confirm before proceeding with
irreversible merge/archive/push actions. Renumber subsequent steps (old
3→4, 4→5, ... 10→11).

## Acceptance Criteria

- [ ] New step 3 uses `AskUserQuestion` with "Close sprint and merge to main" (recommended) and "Review completed work first"
- [ ] Step 3 presents a summary of completed tickets
- [ ] If stakeholder chooses review, skill presents details and stops
- [ ] Subsequent steps renumbered (11 total steps)

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: None (content-only markdown change)
- **Verification command**: `uv run pytest`
