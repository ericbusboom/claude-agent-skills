---
id: "003"
title: Document Restructuring
status: planning
branch: sprint/003-document-restructuring
use-cases: [UC-004, UC-009]
---

# Sprint 003: Document Restructuring

## Goals

Simplify and improve the SE process document model based on lessons from
sprints 001 and 002. Reduce document redundancy, formalize the TODO directory,
add practical tooling (TODO cleanup, versioning), and introduce per-language
instruction support.

## Scope

### In Scope

1. **Formalize TODO directory**: Document `docs/plans/todo/` in SE instructions
   with a defined lifecycle (capture -> mine for sprint -> move to done). Define
   the file format (one idea per level-1 heading).

2. **TODO cleanup CLI command**: `clasi todo-split` command that splits
   multi-heading TODO files into individual files.

3. **TODO integration with sprint planning**: Update the plan-sprint skill to
   include mining the TODO directory. Consumed TODOs move to
   `docs/plans/todo/done/`.

4. **Merge sprint.md and brief.md**: Combine into a single sprint document. The
   brief content (problem, solution, success criteria) becomes part of sprint.md.
   No separate brief.md is created for new sprints.

5. **Add test strategy section**: Each sprint document includes a test strategy
   describing the overall testing approach for that sprint.

6. **Restructure project startup**: Replace separate top-level `brief.md`,
   `usecases.md`, `technical-plan.md` with a single `docs/plans/overview.md`.
   The overview covers project identity, high-level requirements, tech stack,
   and a rough sprint roadmap. All detailed planning lives inside sprints.

7. **Rename use cases to scenarios**: Throughout instructions, templates, and
   process docs. Less formal, better matches actual usage. Prefix changes from
   `UC-`/`SUC-` to `SC-`/`SSC-`.

8. **Mermaid diagram guidance**: Add guidance to instructions on when and how
   to include Mermaid diagrams in technical plans.

9. **Versioning scheme**: Implement `major.isodate.build` version numbering.
   Build number increments on sprint merge to main. Git tag `vX.Y.Z` on merge.

10. **Per-language instructions**: Create `instructions/languages/` with Python
    as the first language. Add MCP tools for listing and reading language
    instructions.

### Out of Scope

- Migrating existing completed sprints to new format (only affects new sprints)
- Per-framework instructions (e.g., Django, Flask) — only per-language
- Automated test generation
- Database/state tracking (that is sprint 002)

## Architecture Notes

- TODO cleanup uses the existing `click` CLI framework from sprint 001.
- Per-language MCP tools extend the SE Process Access tool group.
- Document restructuring is primarily changes to instructions, templates,
  and skills — minimal new Python modules.
- Template changes must handle backward compatibility: old sprints with
  separate brief.md still exist in `done/` and should not break.
- Versioning involves both pyproject.toml updates and git tagging in the
  close-sprint workflow.

## Source TODOs

- `docs/plans/todo/TODOs.md`
- `docs/plans/todo/New docs.md`
- `docs/plans/todo/Mermaid-all-sprint.md`
- `docs/plans/todo/language-instructions.md`
- `docs/plans/todo/Versioning.md`

## Tickets

(To be created after sprint approval.)
