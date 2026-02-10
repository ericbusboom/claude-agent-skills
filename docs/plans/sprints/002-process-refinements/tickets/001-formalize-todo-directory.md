---
id: "001"
title: Formalize TODO directory in SE process
status: todo
use-cases: [SUC-001]
depends-on: []
---

# Formalize TODO Directory in SE Process

## Description

Add the `docs/plans/todo/` directory as a documented part of the SE
process. Currently the directory exists informally but is not mentioned
in the system engineering instructions.

The TODO directory is where stakeholders capture ideas when the AI agent
is busy with other work. Ideas are lightly structured markdown files.
The lifecycle is: capture -> mine during sprint planning -> move to done.

## Changes Required

1. Update `instructions/system-engineering.md`:
   - Add a "TODO Directory" section describing its purpose and lifecycle.
   - Define the file format: each level-1 heading is a separate idea.
     Files may contain multiple headings (to be split by the cleanup
     command).
   - Define the lifecycle: stakeholder creates a file, it lives in
     `todo/` until consumed by a sprint, then moves to `todo/done/`.
   - Update the directory layout diagram to include `todo/` and
     `todo/done/`.

2. Create `docs/plans/todo/done/` directory (with `.gitkeep` if needed).

## Acceptance Criteria

- [ ] `instructions/system-engineering.md` documents the TODO directory
- [ ] File format is defined (level-1 headings as ideas)
- [ ] Lifecycle is defined (capture -> mine -> done)
- [ ] Directory layout in instructions includes `todo/` and `todo/done/`
- [ ] `docs/plans/todo/done/` directory exists
