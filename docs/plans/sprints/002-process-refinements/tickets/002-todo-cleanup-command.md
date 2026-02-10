---
id: "002"
title: Implement TODO cleanup CLI command
status: todo
use-cases: [SUC-002]
depends-on: ["001"]
---

# Implement TODO Cleanup CLI Command

## Description

Add a `clasi todo-split` CLI command that normalizes the TODO directory
by splitting files with multiple level-1 headings into individual files.

This addresses the common pattern where a stakeholder dumps several ideas
into a single file. The cleanup command makes each idea a separate file,
which is easier to manage during sprint planning.

## Implementation

Create `claude_agent_skills/todo_split.py`:

1. Scan `docs/plans/todo/` for `.md` files (exclude `done/` subdir).
2. For each file, parse for level-1 headings (`# Heading`).
3. If 0 or 1 headings, skip.
4. If 2+ headings, extract each section (heading + content until next
   heading or EOF).
5. Create new files named from heading text (slugified: lowercase, spaces
   to hyphens, strip special characters, `.md` extension).
6. Delete the original file.
7. Print a summary of actions.

Register as a `click` command in `cli.py`.

**Edge cases**:
- Content before the first heading: prepend to the first section.
- Heading text collisions: append a number suffix (`-2`, `-3`).
- Empty sections (heading with no body): create file with heading only.

## Acceptance Criteria

- [ ] `clasi todo-split` command exists and runs
- [ ] Files with 2+ level-1 headings are split into individual files
- [ ] New files are named from heading text (slugified)
- [ ] Original file is deleted after successful split
- [ ] Files with 0 or 1 headings are left unchanged
- [ ] Content before the first heading is preserved
- [ ] Command reports what it did (files created, files deleted)
- [ ] Unit tests cover splitting, edge cases, and no-op scenarios
