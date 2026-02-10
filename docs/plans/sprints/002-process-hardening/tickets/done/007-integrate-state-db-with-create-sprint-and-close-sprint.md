---
id: "007"
title: Integrate state DB with create_sprint and close_sprint
status: done
use-cases:
  - SUC-001
depends-on:
  - "005"
---

# Integrate state DB with create_sprint and close_sprint

## Description

Modify the existing `create_sprint` and `close_sprint` MCP tools in
`artifact_tools.py` to integrate with the state database, ensuring that every
sprint has a state record from the moment it is created and that sprint closure
properly updates the lifecycle state.

### Changes to `create_sprint`

After creating the sprint directory and template files (existing behavior),
`create_sprint` must call `register_sprint(db_path, sprint_id, slug, branch)` to
add the sprint to the state database. This registers the sprint in phase
`planning-docs` with the appropriate branch name.

The registration must use lazy initialization -- if the database does not exist
yet, `register_sprint` (which internally calls `init_db`) creates it. This means
no separate setup step is required; the database appears automatically when the
first sprint is created.

The `create_sprint` return value should include a `"phase"` field showing the
initial phase (`planning-docs`).

### Changes to `close_sprint`

Before moving the sprint directory to `done/`, `close_sprint` must:

1. Advance the sprint's phase to `done` in the state database (calling
   `advance_phase`).
2. Release any execution lock held by the sprint (calling `release_lock`).

Both operations should handle the case where the state database does not exist
or the sprint is not registered (graceful degradation for sprints created before
the state DB was introduced). In these cases, the existing close behavior
proceeds unchanged.

After successful closure, the sprint's phase in the database should be `done`
and any execution lock should be released.

## Acceptance Criteria

- [ ] `create_sprint` calls `register_sprint` after creating the directory structure
- [ ] The sprint is registered in phase `planning-docs` with the correct branch name
- [ ] `create_sprint` return value includes `"phase": "planning-docs"`
- [ ] The state database is lazily created on first `create_sprint` call
- [ ] `close_sprint` advances the sprint phase to `done` in the state database
- [ ] `close_sprint` releases any execution lock held by the sprint
- [ ] `close_sprint` handles missing state DB gracefully (no error if DB does not exist)
- [ ] `close_sprint` handles unregistered sprints gracefully (no error if sprint not in DB)
- [ ] The `.clasi.db` file is created at `docs/plans/.clasi.db`
- [ ] Unit tests cover creation with registration, closure with phase advance, and graceful degradation
