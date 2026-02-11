---
id: 008
title: Ticket Testing Sections and Interactive Breakpoints
status: done
branch: sprint/008-ticket-testing-sections-and-interactive-breakpoints
use-cases:
- UC-007
- UC-009
---

# Sprint 008: Ticket Testing Sections and Interactive Breakpoints

## Goals

1. Add a `## Testing` section to the ticket template so every ticket
   documents what tests to run and write.
2. Update the `execute-ticket` skill to reference the ticket's testing
   section during implementation.
3. Add `AskUserQuestion` breakpoints to `next` and `plan-sprint` skills
   at natural phase boundaries — but never between individual tickets.

## Problem

Tickets currently have no standard place to describe testing expectations.
Implementers have to guess what tests to run and write. Additionally, the
`/next` skill barrels through the entire process without giving the
stakeholder a chance to intervene at natural breakpoints (e.g., before
starting ticket execution).

## Solution

- Extend `TICKET_TEMPLATE` in `templates.py` with a `## Testing` section.
- Update `execute-ticket.md` to reference the ticket's testing section in
  the "Write tests" and "Run tests" steps.
- Update `next.md` to use `AskUserQuestion` before starting ticket
  execution and before sprint planning.
- Update `plan-sprint.md` to add an explicit breakpoint after architecture
  review passes.

## Success Criteria

- Every new ticket created via `create_ticket` includes a Testing section.
- The execute-ticket skill instructs agents to follow the Testing section.
- The `/next` skill pauses for stakeholder input before starting bulk
  ticket execution and before sprint planning.
- No breakpoints are added between individual tickets.

## Scope

### In Scope

- `TICKET_TEMPLATE` in `templates.py` (add Testing section)
- `execute-ticket.md` skill (reference Testing section)
- `next.md` skill (add AskUserQuestion breakpoints)
- `plan-sprint.md` skill (add breakpoint after arch review)
- Tests for the updated template

### Out of Scope

- Retroactively adding Testing sections to existing done tickets
- Changes to the ticket MCP tool's Python logic (only the template changes)
- Breakpoints within ticket execution (explicitly excluded per TODO)

## Test Strategy

- Update existing `test_artifact_tools.py` tests to verify the new
  `## Testing` section appears in created tickets.
- Verify `TICKET_TEMPLATE` contains the expected Testing section content.
- Skill changes are content-only markdown and don't have automated tests.
- Run full test suite: `uv run pytest`

## Architecture Notes

- Both changes are largely content-only (markdown skill definitions).
- The only Python code change is adding lines to `TICKET_TEMPLATE`.
- No new modules, no new MCP tools, no schema changes.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, technical plan)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

- **001**: Add Testing section to ticket template (SUC-001)
- **002**: Update execute-ticket skill to reference Testing section (SUC-002, depends on 001)
- **003**: Add interactive breakpoints to next skill (SUC-003, SUC-004)
- **004**: Add conditional breakpoint to plan-sprint skill (SUC-004)
- **005**: Push version tags on sprint close (UC-013)
