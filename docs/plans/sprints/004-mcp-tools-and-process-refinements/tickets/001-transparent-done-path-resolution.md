---
id: "001"
title: Transparent done path resolution
status: todo
use-cases: [SUC-005]
depends-on: []
---

# Transparent done path resolution

## Description

Create a `resolve_artifact_path(path)` function in `artifact_tools.py`
that finds files whether they're in their original location or have been
moved to a `done/` subdirectory. Integrate it into existing MCP tools
that accept file paths.

### Implementation

1. Add `resolve_artifact_path(path: str) -> Path` to `artifact_tools.py`.
   - Check given path first.
   - If not found, try inserting `done/` before the filename.
   - If not found, try removing `done/` from the path.
   - Raise `FileNotFoundError` with clear message if neither works.
2. Wire into `update_ticket_status` and `move_ticket_to_done`.

## Acceptance Criteria

- [ ] `resolve_artifact_path` finds files in their original location
- [ ] `resolve_artifact_path` finds files after move to `done/`
- [ ] `resolve_artifact_path` handles paths already containing `done/`
- [ ] `update_ticket_status` uses the resolver
- [ ] `move_ticket_to_done` uses the resolver
- [ ] Unit tests for `resolve_artifact_path`
