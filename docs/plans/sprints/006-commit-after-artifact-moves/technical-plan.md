---
status: draft
---

# Sprint 006 Technical Plan

## Architecture Overview

Three skill files need targeted edits to add commit instructions after
file-move operations. No Python code changes.

## Component Design

### Component: execute-ticket.md

**Use Cases**: SUC-001

Step 11 ("Complete the ticket") moves ticket and plan files to `tickets/done/`
but doesn't say to commit those moves. The preceding step 10 commits
implementation work, but the file moves in step 11 happen after that commit.

**Fix**: Add a step after the file moves in step 11 to commit the moved files.

### Component: close-sprint.md

**Use Cases**: SUC-001

Step 6 calls `close_sprint` which moves the entire sprint directory to
`sprints/done/` and bumps `pyproject.toml` version. Step 7 deletes the branch.
Neither step says to commit the moves.

**Fix**: Add a commit step between steps 6 and 7 (after close_sprint, before
branch delete).

### Component: plan-sprint.md

**Use Cases**: SUC-001

Step 2 ("Mine the TODO directory") says to move consumed TODOs to done/ but
doesn't mention committing. This happens early in the process before the sprint
branch even exists, so it may need to be committed on the current branch or
deferred.

**Fix**: Add a note to commit the TODO moves. Since TODOs are moved after the
sprint directory is created (step 3) and the sprint branch exists (step 4),
clarify that TODO moves happen on the sprint branch and should be committed.
