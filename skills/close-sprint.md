---
name: close-sprint
description: Validates and closes a completed sprint — verifies tickets, merges branch, archives sprint document
---

# Close Sprint Skill

This skill closes a completed sprint: verify all tickets are done, merge
the sprint branch, and archive the sprint document.

## Agent Used

**project-manager**

## Inputs

- Active sprint directory in `docs/plans/sprints/NNN-slug/`
- All tickets for this sprint should be `done`

## Process

1. **Identify the sprint**: Read active sprint directories from
   `docs/plans/sprints/`. If multiple sprints are active, confirm with
   the stakeholder which one to close.

2. **Verify all tickets are done**: Read each ticket in the sprint's
   `tickets/` directory. Every ticket must:
   - Have status `done` in its YAML frontmatter
   - Be located in the sprint's `tickets/done/` directory
   - Satisfy the Definition of Done (see SE instructions)

   If any ticket is not done, report which tickets remain and stop.

3. **Advance to closing phase**: Call `advance_sprint_phase` to move
   from `executing` to `closing`.

4. **Run final validation**: Ensure tests pass, no uncommitted changes
   exist on the sprint branch.

5. **Merge sprint branch**: Merge `sprint/NNN-slug` into main:
   ```
   git checkout main
   git merge sprint/NNN-slug
   ```
   If there are merge conflicts, resolve them or escalate to the
   stakeholder.

6. **Close the sprint**: Call the `close_sprint` MCP tool. This
   atomically:
   - Updates the sprint document status to `done`
   - Moves the sprint directory to `docs/plans/sprints/done/NNN-slug/`
   - Advances the state database phase to `done`
   - Releases the execution lock

7. **Commit the archive**: The `close_sprint` tool moves files and bumps
   the version in `pyproject.toml` but does not commit. Run `git add` for
   the moved sprint directory and `pyproject.toml`, then commit with a
   message like `chore: close sprint NNN — archive to done, tag vX.Y.Z`.

8. **Delete sprint branch**: Run `git branch -d sprint/NNN-slug`.

9. **Report completion**: Summarize what was accomplished in the sprint —
   list of completed tickets, key changes, any notes for follow-up.

## Output

- Sprint branch merged to main and deleted
- Sprint document moved to `docs/plans/sprints/done/`
- State database phase set to `done`, execution lock released
- Sprint completion summary reported to stakeholder
