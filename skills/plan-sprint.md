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

2. **Mine the TODO directory**: Scan `docs/plans/todo/` for ideas relevant
   to the upcoming sprint. Discuss relevant TODOs with the stakeholder and
   incorporate selected items into the sprint scope. After the sprint
   directory is created (step 3), move consumed TODO files to
   `docs/plans/todo/done/`.

3. **Create sprint directory**: Use the `create_sprint` MCP tool. This
   creates the directory structure and registers the sprint in the state
   database at phase `planning-docs`:
   - `sprint.md` — Sprint goals, scope, architecture notes, ticket list.
     Frontmatter: id, title, status: planning, branch, use-cases.
   - `brief.md` — Sprint-level brief (problem, solution, success criteria).
   - `usecases.md` — Sprint-level use cases (SUC-NNN).
   - `technical-plan.md` — Sprint-level architecture and component design.
   - `tickets/` — Empty directory for tickets (with `done/` subdirectory).

4. **Create sprint branch**: Run `git checkout -b sprint/NNN-slug` from main.

5. **Advance to architecture-review**: Call `advance_sprint_phase` to move
   from `planning-docs` to `architecture-review`.

6. **Architecture review**: Delegate to the architecture-reviewer agent.
   The reviewer reads the sprint plan, technical plan, and relevant existing
   code, then produces a review (APPROVE / APPROVE WITH CHANGES / REVISE).
   - If REVISE: update the sprint document and re-review.
   - If APPROVE WITH CHANGES: note the changes for ticket creation.
   - Call `record_gate_result` with gate `architecture_review` and result
     `passed` or `failed`.

7. **Advance to stakeholder-review**: If architecture review passed, call
   `advance_sprint_phase` to move to `stakeholder-review`.

8. **Stakeholder review gate**: Present the sprint plan and architecture
   review to the stakeholder. Wait for approval. If changes are requested,
   revise and re-present.
   - Call `record_gate_result` with gate `stakeholder_approval` and result
     `passed` or `failed`.

9. **Advance to ticketing**: If stakeholder approved, call
   `advance_sprint_phase` to move to `ticketing`.

10. **Create tickets**: Delegate to the systems-engineer to create tickets
    for this sprint. Tickets are created in the sprint's `tickets/` directory
    with per-sprint numbering (001, 002, ...). Update the sprint document's
    Tickets section with the list of created tickets.

11. **Acquire execution lock and advance to executing**: Call
    `acquire_execution_lock` to claim the lock for this sprint, then call
    `advance_sprint_phase` to move to `executing`. Only one sprint can hold
    the execution lock at a time.

12. **Set sprint status**: Update the sprint document status to `active`.

## Output

- Sprint directory `docs/plans/sprints/NNN-slug/` with planning documents
- Sprint `sprint.md` status set to `active`
- Sprint branch `sprint/NNN-slug` created
- Sprint phase advanced to `executing` in the state database
- Execution lock acquired for this sprint
- Tickets in the sprint's `tickets/` directory ready for execution
