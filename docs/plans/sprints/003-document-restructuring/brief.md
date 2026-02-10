---
status: draft
sprint: "003"
---

# Sprint 003 Brief

## Problem

The SE process has several rough edges identified through daily use:

1. **No place for ideas**: Stakeholders capture ideas in `docs/plans/todo/`
   informally but this directory is not part of the documented process. There
   is no defined format, lifecycle, or tooling.

2. **Too many documents per sprint**: Each sprint requires separate sprint.md,
   brief.md, usecases.md, and technical-plan.md. Sprint.md and brief.md overlap
   significantly, creating redundancy.

3. **Heavy project startup**: The process requires separate brief.md,
   usecases.md, and technical-plan.md at the project level before sprints begin.
   This front-loads detail that often changes. A lighter overview with details
   pushed into sprints is more practical.

4. **Missing guidance**: Technical plans lack diagram guidance. Sprint documents
   lack test strategy sections, making testing an afterthought.

5. **No per-language support**: Instructions are one-size-fits-all. There is no
   mechanism for language-specific coding conventions.

6. **No versioning scheme**: No defined approach to version numbering, no
   automated tagging on merge.

## Solution

1. Formalize the TODO directory with a lifecycle and a `clasi todo-split` CLI
   tool for splitting multi-topic files.
2. Merge sprint.md and brief.md into a single document. Add a test strategy
   section.
3. Replace three top-level planning docs with a single overview document.
4. Rename "use cases" to "scenarios" throughout.
5. Add Mermaid diagram guidance to technical plan instructions.
6. Implement `major.isodate.build` versioning with git tagging on merge.
7. Create per-language instruction files with MCP tool support.

## Success Criteria

- `docs/plans/todo/` is documented in SE instructions with clear lifecycle.
- `clasi todo-split` correctly splits multi-heading files.
- Sprint planning mines the TODO directory.
- Sprint template has a single document (no separate brief.md) with test
  strategy section.
- Single `docs/plans/overview.md` replaces three separate top-level docs.
- All instructions/templates/skills use "scenario" instead of "use case."
- Technical plan instructions include Mermaid diagram guidance.
- Versioning scheme documented and automated in close-sprint workflow.
- `instructions/languages/python.md` exists and is accessible via MCP.
