---
id: '004'
title: Add tests for complex artifact operations (close_sprint, insert_sprint, move_ticket_to_done)
status: done
use-cases:
- SUC-005
depends-on:
- '001'
---

# Add tests for complex artifact operations

## Description

The three most complex state-mutating operations in artifact_tools.py
need additional edge case coverage. The existing test_artifact_tools.py
is strong for happy paths but doesn't exercise multi-step failure
scenarios or complex state transitions.

## Tasks

### close_sprint tests
1. Test full closure: sprint moves to done/, state DB advanced, execution
   lock released
2. Test closure with versioning: mock git tag, verify version file updated,
   verify tag name in response
3. Test closure when sprint has no version file (graceful skip)
4. Test closure with state DB errors (graceful degradation)

### insert_sprint tests
1. Test inserting between 3 existing sprints: verify all IDs renumbered
   correctly in directories, frontmatter, and state DB
2. Test inserting at the end (after last sprint)
3. Test insert blocked when target sprints are past planning-docs phase
4. Test that ticket frontmatter sprint_id is updated during renumbering

### move_ticket_to_done tests
1. Test moving ticket that has an associated plan file (ticket_id-plan.md):
   verify both files moved
2. Test moving ticket with no plan file: only ticket moved
3. Test moving ticket already in done/ path (no-op or error)
4. Test that ticket status frontmatter is preserved after move

## Acceptance Criteria

- [ ] >= 4 new close_sprint tests
- [ ] >= 4 new insert_sprint tests
- [ ] >= 3 new move_ticket_to_done tests
- [ ] All tests use real filesystem (tmp_path), mock only git/subprocess
- [ ] All tests pass: `uv run pytest tests/system/test_artifact_tools.py`

## Testing

- **Existing tests to run**: `uv run pytest tests/system/test_artifact_tools.py`
- **New tests to write**: Added to existing test_artifact_tools.py
- **Verification command**: `uv run pytest -v tests/system/test_artifact_tools.py`
