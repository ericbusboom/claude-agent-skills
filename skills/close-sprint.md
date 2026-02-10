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

- Active sprint document in `docs/plans/sprints/NNN-slug.md`
- All tickets for this sprint should be `done`

## Process

1. **Identify the sprint**: Read the active sprint document from
   `docs/plans/sprints/`. If multiple sprints are active, confirm with
   the stakeholder which one to close.

2. **Verify all tickets are done**: Read each ticket listed in the sprint
   document. Every ticket must:
   - Have status `done` in its YAML frontmatter
   - Be located in `docs/plans/tickets/done/`
   - Satisfy the Definition of Done (see SE instructions)

   If any ticket is not done, report which tickets remain and stop.

3. **Run final validation**: Ensure tests pass, no uncommitted changes
   exist on the sprint branch.

4. **Merge sprint branch**: Merge `sprint/NNN-slug` into main:
   ```
   git checkout main
   git merge sprint/NNN-slug
   ```
   If there are merge conflicts, resolve them or escalate to the
   stakeholder.

5. **Update sprint document**: Set the sprint status to `done`.

6. **Archive sprint**: Move the sprint document to
   `docs/plans/sprints/done/NNN-slug.md`.

7. **Report completion**: Summarize what was accomplished in the sprint —
   list of completed tickets, key changes, any notes for follow-up.

## Output

- Sprint branch merged to main
- Sprint document moved to `docs/plans/sprints/done/`
- Sprint completion summary reported to stakeholder
