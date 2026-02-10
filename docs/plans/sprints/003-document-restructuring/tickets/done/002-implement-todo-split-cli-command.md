---
id: '002'
title: Implement todo-split CLI command
status: done
use-cases:
- SUC-002
depends-on: []
---

# Implement todo-split CLI command

## Description

Create a `clasi todo-split` CLI command that normalizes the TODO directory by
splitting files with multiple level-1 headings into individual files.

Create `claude_agent_skills/todo_split.py` with the splitting logic and
register the command in `cli.py`.

### Algorithm

1. Scan `docs/plans/todo/` for `.md` files (exclude `done/` subdir).
2. For each file, parse for level-1 headings (`# Heading`).
3. If 0 or 1 headings, skip.
4. If 2+ headings, extract each section (heading + content until next heading
   or EOF).
5. Create new file named from heading (slugified).
6. Delete original file.
7. Report actions to stdout.

### Edge cases

- Content before first heading: prepend to first section.
- Heading collisions: append number suffix.
- Empty sections: still create file (heading only).

## Acceptance Criteria

- [x] `clasi todo-split` command exists and runs
- [x] Multi-heading files split into individual files
- [x] New file names derived from heading text (slugified, using existing `slugify`)
- [x] Original file deleted after successful split
- [x] Single-heading and no-heading files left alone
- [x] Content before first heading preserved
- [x] Heading name collisions handled with numeric suffix
- [x] Unit tests cover normal case, edge cases, and no-op scenario
