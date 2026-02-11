---
id: '004'
title: Add TODO frontmatter and traceability to move_todo_to_done
status: done
use-cases:
- SUC-003
depends-on: []
---

# Add TODO frontmatter and traceability to move_todo_to_done

## Description

Enhance `move_todo_to_done` in `artifact_tools.py` to accept optional
`sprint_id` and `ticket_ids` parameters. When provided, write them into
the TODO's YAML frontmatter before moving the file. Update `skills/todo.md`
to add `status: pending` frontmatter when creating new TODOs.

`list_todos` already only scans active TODOs (not done/), so no filtering
change needed (stakeholder decision).

## Acceptance Criteria

- [ ] `move_todo_to_done` accepts optional `sprint_id: str` parameter
- [ ] `move_todo_to_done` accepts optional `ticket_ids: list[str]` parameter
- [ ] When sprint_id/ticket_ids provided, frontmatter is written before move
- [ ] Frontmatter includes `status: done`, `sprint`, and `tickets` fields
- [ ] `skills/todo.md` instructs adding `status: pending` frontmatter on creation
- [ ] Unit tests for new parameters
- [ ] All tests pass
