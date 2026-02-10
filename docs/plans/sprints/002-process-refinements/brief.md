---
status: draft
---

# Sprint 002 Brief

## Problem

The SE process has several rough edges identified through use:

1. **No place for ideas**: When stakeholders have ideas during a busy
   session, there is no formalized place to capture them for later.
   The `docs/plans/todo/` directory exists informally but is not part of
   the documented process.

2. **Too many documents per sprint**: Each sprint currently requires
   separate sprint.md, brief.md, usecases.md, and technical-plan.md files.
   The sprint.md and brief.md overlap significantly, creating redundancy.

3. **Rigid project startup**: The current process requires separate
   brief.md, usecases.md, and technical-plan.md at the project level before
   any sprint work begins. This front-loads detail that often changes once
   sprints begin. A lighter top-level overview with details pushed into
   sprints is more practical.

4. **Missing guidance**: Technical plans lack guidance on when and how to
   use diagrams. Sprint documents lack a test strategy section, making
   testing an afterthought.

5. **No per-language support**: Instructions are one-size-fits-all. There
   is no mechanism for language-specific coding standards or conventions
   (Python vs TypeScript vs Go).

## Solution

1. Formalize the TODO directory with a defined lifecycle and a CLI tool
   for splitting multi-topic TODO files into individual files.

2. Merge sprint.md and brief.md into a single sprint document. Add a test
   strategy section.

3. Replace the three top-level planning documents with a single overview
   document. Push all detailed architecture and scenarios into sprints.

4. Add Mermaid diagram guidance to the technical planning instructions.

5. Create a per-language instruction directory (`instructions/languages/`)
   with MCP tool support.

## Success Criteria

- `docs/plans/todo/` is documented in SE instructions with a clear
  lifecycle.
- `clasi todo-split` correctly splits multi-heading TODO files into
  individual files.
- Sprint planning workflow includes a step to mine the TODO directory.
- Sprint template has a single document (no separate brief.md) with a
  test strategy section.
- A single project overview document replaces the three separate top-level
  planning documents.
- Technical plan instructions include Mermaid diagram guidance.
- `instructions/languages/python.md` exists and is accessible via MCP.
