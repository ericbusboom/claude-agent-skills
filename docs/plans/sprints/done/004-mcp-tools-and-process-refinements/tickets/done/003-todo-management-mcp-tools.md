---
id: '003'
title: TODO management MCP tools
status: done
use-cases:
- SUC-002
depends-on: []
---

# TODO management MCP tools

## Description

Add two MCP tools to `artifact_tools.py` for managing the TODO directory.

### Implementation

1. `list_todos()` — Scan `docs/plans/todo/*.md`, return JSON array of
   `{filename, title}` where title is the first `# ` heading.
2. `move_todo_to_done(filename)` — Move from `docs/plans/todo/` to
   `docs/plans/todo/done/`. Create `done/` if needed.

## Acceptance Criteria

- [ ] `list_todos` returns JSON array with filename and title
- [ ] `list_todos` excludes `done/` subdirectory files
- [ ] `move_todo_to_done` moves file to `done/`
- [ ] `move_todo_to_done` creates `done/` if needed
- [ ] Error on nonexistent filename
- [ ] Unit tests for both tools
