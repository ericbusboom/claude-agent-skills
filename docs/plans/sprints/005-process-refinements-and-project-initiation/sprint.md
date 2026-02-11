---
id: "005"
title: Process Refinements and Project Initiation
status: planning
branch: sprint/005-process-refinements-and-project-initiation
use-cases: [SUC-001, SUC-002, SUC-003, SUC-004, SUC-005]
---

# Sprint 005: Process Refinements and Project Initiation

## Goals

Rename the SE process from "Systems Engineering" to "Software Engineering",
streamline project initiation into a single overview document with a guided
interview, add frontmatter traceability to TODOs, and surface open questions
during sprint planning reviews.

## Problem

1. The process is named "Systems Engineering" but should be "Software
   Engineering"; the agent is called `systems-engineer` but should be
   `technical-lead`.
2. Project initiation creates three separate documents (brief, technical plan,
   use cases) when a single overview document would be simpler and more
   accessible.
3. TODO files have no frontmatter — there's no traceability from a done TODO
   back to the sprint/tickets that addressed it.
4. Open questions in technical plans are passive text; they should be actively
   presented to the stakeholder during the review gate.
5. AI agents tried to create tickets during sprint initiation before the
   planning docs were even reviewed — the instructions need to be more
   forceful about the phase gate.

## Solution

- Global rename of "Systems Engineering" → "Software Engineering" and
  `systems-engineer.md` → `technical-lead.md` across all instructions, agents,
  skills, and embedded content.
- Create a product-manager agent and an initiation interview workflow that
  produces a single `overview.md`, linked into IDE instruction directories.
- Add YAML frontmatter to TODO files on creation and update it with sprint/ticket
  references on `move_todo_to_done`.
- Enhance the plan-sprint skill to parse open questions and present them via
  `AskUserQuestion` at the stakeholder review gate.

## Success Criteria

- No references to "Systems Engineering" or `systems-engineer` remain in the
  codebase
- `clasi init` scaffolds the overview-based initiation workflow
- A product-manager agent definition exists and is referenced by a
  project-initiation skill
- `move_todo_to_done` writes sprint/ticket traceability into frontmatter
- Open questions are presented interactively during stakeholder review
- Instructions clearly prohibit ticket creation before stakeholder approval

## Scope

### In Scope

- Rename process and agent across all files
- Product manager agent definition
- Project overview document template and `create_overview` workflow
- TODO frontmatter (status, sprint, tickets)
- Open questions interactive presentation in plan-sprint skill
- Updates to `clasi init` for overview-based flow
- Harden instructions to prevent premature ticket creation
- Retroactive frontmatter on the 4 TODOs already moved to done/
- Tests for all new/changed functionality

### Out of Scope

- Full CLAUDE.md generation (future sprint)
- MCP prompts/resources/apps (decided to wait and see)
- Rewriting existing sprint archives to match new naming

## Test Strategy

- Unit tests for any new/changed Python modules (frontmatter updates,
  rename verification)
- System tests for the init command with new overview workflow
- Grep-based verification that no old naming remains after rename

## Architecture Notes

- The rename is a codebase-wide find-and-replace plus file rename — no
  architectural changes needed.
- The overview document replaces three separate files. The old
  `create_brief`/`create_technical_plan`/`create_use_cases` MCP tools will
  be removed entirely (stakeholder decision).
- `create_overview` MCP tool already exists; it needs to be wired into the
  initiation workflow.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, technical plan)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
