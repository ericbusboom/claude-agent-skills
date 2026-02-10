---
name: project-status
description: Analyzes current project state by reading SE artifacts and reports phase, progress, and next actions
---

# Project Status Skill

This skill scans the SE artifacts and tickets to determine where a project
stands and what should happen next.

## Agent Used

**project-manager** (or can be invoked standalone)

## Process

1. **Check artifacts**: Verify which SE documents exist:
   - `docs/plans/brief.md`
   - `docs/plans/usecases.md`
   - `docs/plans/technical-plan.md`
2. **Scan tickets**: Read all ticket files in `docs/plans/tickets/` and
   `docs/plans/tickets/done/`. Extract frontmatter status for each.
3. **Determine phase**:
   - No brief → Phase 1 (Requirements) not started
   - Brief but no use cases → Phase 1 in progress
   - Use cases but no technical plan → Phase 1b (Architecture) needed
   - Technical plan but no tickets → Phase 2 (Ticketing) needed
   - Tickets exist with `todo` items → Phase 3 (Implementation)
   - All tickets `done` → Phase 4 (Maintenance)
4. **Report progress**:
   - Artifacts: which exist, their status
   - Tickets: count by status (todo, in-progress, done)
   - Next action: what should be done next
5. **Identify blockers**: Missing dependencies, in-progress tickets without
   plans, tickets with unmet depends-on.

## Output

A structured status report showing current phase, artifact status, ticket
progress, and recommended next action.
