---
name: plan-sprint
description: Creates a new sprint from a stakeholder conversation — sprint document, branch, architecture review, and ticket creation
---

# Plan Sprint Skill

This skill creates a new sprint: capture goals, create the sprint document,
set up the branch, get architecture review, get stakeholder approval, and
create tickets.

## Agent Used

**project-manager** (orchestrates), **architecture-reviewer** (reviews plan),
**systems-engineer** (creates tickets)

## Inputs

- Stakeholder conversation describing the work to be done
- `docs/plans/brief.md` (must exist)
- `docs/plans/usecases.md` (must exist)
- `docs/plans/technical-plan.md` (must exist)

## Process

1. **Determine sprint number**: Check `docs/plans/sprints/` and
   `docs/plans/sprints/done/` for existing sprints. The new sprint gets the
   next sequential number (NNN format: 001, 002, ...).

2. **Create sprint directory**: Create `docs/plans/sprints/NNN-slug/` with:
   - `sprint.md` — Sprint goals, scope, architecture notes, ticket list.
     Frontmatter: id, title, status: planning, branch, use-cases.
   - `brief.md` — Sprint-level brief (problem, solution, success criteria).
   - `usecases.md` — Sprint-level use cases (SUC-NNN).
   - `technical-plan.md` — Sprint-level architecture and component design.
   - `tickets/` — Empty directory for tickets (with `done/` subdirectory).

3. **Create sprint branch**: Run `git checkout -b sprint/NNN-slug` from main.

4. **Architecture review**: Delegate to the architecture-reviewer agent.
   The reviewer reads the sprint plan, technical plan, and relevant existing
   code, then produces a review (APPROVE / APPROVE WITH CHANGES / REVISE).
   - If REVISE: update the sprint document and re-review.
   - If APPROVE WITH CHANGES: note the changes for ticket creation.

5. **Stakeholder review gate**: Present the sprint plan and architecture
   review to the stakeholder. Wait for approval. If changes are requested,
   revise and re-present.

6. **Create tickets**: Delegate to the systems-engineer to create tickets
   for this sprint. Tickets are created in the sprint's `tickets/` directory
   with per-sprint numbering (001, 002, ...). Update the sprint document's
   Tickets section with the list of created tickets.

7. **Set sprint status**: Update the sprint document status to `active`.

## Output

- Sprint directory `docs/plans/sprints/NNN-slug/` with planning documents
- Sprint `sprint.md` status set to `active`
- Sprint branch `sprint/NNN-slug` created
- Tickets in the sprint's `tickets/` directory ready for execution
