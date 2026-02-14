---
id: '005'
title: Add insert_sprint MCP tool to insert and renumber sprints
status: done
use-cases: []
depends-on: []
---

# Add insert_sprint MCP tool to insert and renumber sprints

## Description

Add an `insert_sprint` MCP tool that inserts a new sprint at a specified
position and renumbers all subsequent sprints to make room.

Currently `create_sprint` always appends (auto-assigns the next number).
Sometimes a stakeholder needs to insert a sprint between existing ones —
for example, inserting an urgent sprint between 012 and 013. The new tool
should:

1. Accept a position (e.g., "after sprint 012") and a title.
2. Create the new sprint at the next number (013).
3. Renumber all sprints that previously occupied 013+ by incrementing
   their IDs (013 becomes 014, 014 becomes 015, etc.).
4. Only sprints in `planning-docs` state (not yet committed to branches)
   should be renumbered. If a sprint that would need renumbering is in
   `active`, `executing`, or later phase, the tool should refuse and
   explain why.

Renumbering involves:
- Renaming the sprint directory (e.g., `013-foo` → `014-foo`)
- Updating the sprint ID in `sprint.md` frontmatter
- Updating sprint ID references in ticket frontmatter
- Updating any cross-references in use cases or technical plan docs

Since these sprints haven't been committed to branches yet, there are no
branch names or tags to update.

## Acceptance Criteria

- [ ] New `insert_sprint(after_sprint_id, title)` MCP tool registered
- [ ] Creates new sprint directory with correct ID and template docs
- [ ] Renumbers all subsequent sprints in `planning-docs` state
- [ ] Refuses to renumber sprints in `active` or later phases
- [ ] Updates sprint ID in frontmatter of renamed sprint docs
- [ ] Updates sprint_id references in tickets of renamed sprints
- [ ] Works correctly when inserting at the end (no renumbering needed)
- [ ] Works correctly when inserting in front of all planning sprints

## Testing

- **Existing tests to run**: `uv run pytest tests/unit/test_artifact_tools.py`
- **New tests to write**:
  - Insert between two planning sprints, verify renumbering
  - Insert when subsequent sprint is active (should refuse)
  - Insert at end (no renumbering, equivalent to create_sprint)
  - Verify ticket frontmatter updated in renumbered sprints
- **Verification command**: `uv run pytest`
