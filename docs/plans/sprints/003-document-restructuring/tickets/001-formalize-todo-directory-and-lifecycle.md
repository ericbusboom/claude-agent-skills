---
id: '001'
title: Formalize TODO directory and lifecycle
status: in-progress
use-cases:
- SUC-001
depends-on: []
---

# Formalize TODO directory and lifecycle

## Description

Document the `docs/plans/todo/` directory in `instructions/system-engineering.md`
as an official part of the SE process. Define the file format (one idea per
level-1 heading, descriptive filename), the lifecycle (capture -> mine for
sprint -> move to `done/`), and create the `docs/plans/todo/done/` directory.

This is currently an informal convention that needs to be part of the
documented process so AI agents know how to use it.

## Acceptance Criteria

- [x] `instructions/system-engineering.md` has a "TODO Directory" section
- [x] File format documented (markdown, one idea per level-1 heading)
- [x] Lifecycle documented (capture -> mine -> done)
- [x] `docs/plans/todo/done/` directory exists (with .gitkeep)
- [x] Directory layout diagram in SE instructions updated to show todo/
