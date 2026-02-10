---
name: execute-ticket
description: Executes a single implementation ticket through the full lifecycle — plan, implement, test, document, complete
---

# Execute Ticket Skill

This skill takes a ticket through its full lifecycle from planning to
completion, coordinating multiple agents.

## Agents Used

- **systems-engineer** — creates the ticket plan
- **python-expert** (or appropriate dev agent) — implements the code
- **code-reviewer** — reviews the implementation
- **documentation-expert** — updates documentation

## Inputs

- A ticket ID, or picks the next `todo` ticket whose dependencies are all
  `done`

## Process

1. **Select ticket**: Find the next `todo` ticket in `docs/plans/tickets/`
   whose `depends-on` entries are all `done`. Read its description and
   acceptance criteria.
2. **Create ticket plan**: Write `docs/plans/tickets/NNN-<slug>-plan.md`
   containing:
   - Approach and key design decisions
   - Files to create or modify
   - Testing plan (test type, verification strategy)
   - Documentation updates needed
3. **Set in-progress**: Update the ticket's `status` to `in-progress`.
4. **Implement**: Write the code following the plan. Use the appropriate
   development agent (python-expert for Python work, etc.).
5. **Write tests**: Create tests as specified in the plan. Follow the
   testing instructions (unit tests in `tests/unit/`, system tests in
   `tests/system/`, dev tests in `tests/dev/`).
6. **Run tests**: Verify all tests pass.
7. **Code review** (agent: **code-reviewer**): Delegate review to the
   code-reviewer agent, which checks:
   - Coding standards (`instructions/coding-standards.md`)
   - Security (no injection, no secrets, safe input handling)
   - Test coverage (every acceptance criterion has a corresponding test)
   - Acceptance criteria (does the code actually satisfy them?)
   The reviewer produces a PASS or FAIL verdict. If FAIL, fix the critical
   findings and request re-review. Do not proceed until the review passes.
8. **Update documentation** (skill: **generate-documentation**): Update any
   docs specified in the plan. Delegate to documentation-expert.
9. **Verify acceptance criteria**: Check every criterion in the ticket.
   All must be met.
10. **Git commit**: Commit all changes from this ticket following the
    conventions in `instructions/git-workflow.md`. The commit message must
    reference the ticket ID and sprint number if working within a sprint
    (e.g., `feat: add auth endpoint (#003, sprint 001)`).
11. **Complete the ticket**:
   - Set `status` to `done` in the ticket's YAML frontmatter.
   - Check off all acceptance criteria (`- [x]`).
   - Move the ticket file to `docs/plans/tickets/done/`.
   - Move the ticket plan file to `docs/plans/tickets/done/`.

## Output

- Implemented code with passing tests
- Updated documentation
- Ticket and plan moved to `docs/plans/tickets/done/`
