---
id: "002"
title: SE Process Refinements
status: planning
branch: sprint/002-process-refinements
use-cases: [UC-004, UC-009, UC-010]
---

# Sprint 002: SE Process Refinements

## Goals

Refine and evolve the SE process based on lessons learned from sprint 001
and stakeholder feedback. This sprint addresses four areas:

1. **TODO system**: Formalize the `docs/plans/todo/` directory as part of
   the SE process, with a lifecycle (capture, mine for sprints, move to
   done) and a cleanup CLI command.

2. **Document restructuring**: Simplify the document hierarchy by merging
   sprint.md and brief.md, and by replacing the separate top-level
   brief/usecases/technical-plan with a single overview document. All
   detailed planning moves into sprints.

3. **Process guidance**: Add Mermaid diagram guidance for technical plans
   and a test strategy section to sprint documents.

4. **Per-language instructions**: Create a per-language instruction
   subdirectory with MCP tools for discovery.

## Scope

### In Scope

1. **Formalize TODO directory**: Document the TODO directory in SE
   instructions. Define file format (one idea per level-1 heading) and
   lifecycle (create -> mine for sprint -> move to done).

2. **TODO cleanup command**: `clasi todo-split` CLI command that breaks
   multi-heading TODO files into individual files.

3. **TODO integration with sprint planning**: Update the plan-sprint
   workflow to include mining the TODO directory. Consumed TODOs move to
   `docs/plans/todo/done/`.

4. **Merge sprint.md and brief.md**: Combine these into a single sprint
   document. The brief content (problem, solution, success criteria)
   becomes part of the sprint document rather than a separate file.

5. **Restructure project startup**: Replace separate top-level
   `brief.md`, `usecases.md`, and `technical-plan.md` with a single
   general overview document (`docs/plans/overview.md`). The overview
   covers project identity, high-level requirements, technology choices,
   and a rough sprint roadmap. All detailed architecture and scenarios
   live inside sprint directories.

6. **Rename "use cases" to "scenarios"**: Throughout instructions,
   templates, and process documentation. Scenarios are less formal and
   better match how the process is actually used.

7. **Mermaid diagram guidance**: Add guidance to instructions on when and
   how to include Mermaid diagrams in technical plans. Focus on subsystem
   interaction and module dependency diagrams.

8. **Test strategy section**: Add a test plan/strategy section to the
   sprint document template.

9. **Per-language instruction files**: Create `instructions/languages/`
   with Python as the first language. Add MCP tools for listing and
   reading language-specific instructions.

### Out of Scope

- Migrating existing documents to the new format (this sprint defines the
  new format; migration happens incrementally as sprints are created)
- Per-framework instructions (e.g., Django, Flask) — only per-language
- Automated test generation or test framework selection

## Architecture Notes

- TODO cleanup uses the existing CLI framework (`click` from sprint 001)
- Per-language MCP tools extend the SE Process Access tool group
- Document restructuring is primarily changes to instructions, templates,
  and skills (no new Python modules)
- Template changes in `templates.py` must stay backward-compatible with
  any sprint 001 templates already in use

## Tickets

| ID  | Title | Depends On |
|-----|-------|-----------|
| 001 | Formalize TODO directory in SE process | — |
| 002 | Implement TODO cleanup CLI command | 001 |
| 003 | Integrate TODOs into sprint planning workflow | 001 |
| 004 | Merge sprint.md and brief.md | — |
| 005 | Add test strategy section to sprint template | 004 |
| 006 | Add Mermaid diagram guidance | — |
| 007 | Restructure project startup to single overview | 004 |
| 008 | Rename use cases to scenarios | 007 |
| 009 | Create per-language instruction directory | — |
| 010 | Add MCP tools for per-language instructions | 009 |

Independent starting points: 001, 004, 006, 009

Critical path: 004 -> 007 -> 008

## Source TODOs

This sprint was mined from the following TODO files:

- `docs/plans/todo/TODOs.md` -> tickets 001, 002, 003
- `docs/plans/todo/New docs.md` -> tickets 004, 005
- `docs/plans/todo/Mermaid-all-sprint.md` -> tickets 006, 007, 008
- `docs/plans/todo/language-instructions.md` -> tickets 009, 010
