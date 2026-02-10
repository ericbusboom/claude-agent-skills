---
id: "004"
title: Execution locks
status: todo
use-cases:
  - SUC-003
depends-on:
  - "001"
---

# Execution locks

## Description

Add three execution lock functions to `state_db.py`:

- `acquire_lock(db_path, sprint_id)` -- Attempt to acquire the global execution
  lock for a sprint.
- `release_lock(db_path, sprint_id)` -- Release the execution lock held by a
  sprint.
- `get_lock_holder(db_path)` -- Query who currently holds the lock.

The `execution_locks` table is a singleton: it has a CHECK constraint
`(id = 1)` ensuring only one row can ever exist. This guarantees that at most
one sprint can be executing at any time, preventing concurrent sprint execution
which could lead to conflicting code changes.

### `acquire_lock(db_path, sprint_id)`

- Checks whether the lock is currently held (a row exists in `execution_locks`).
- If no row exists, inserts a row with the given sprint_id and current ISO 8601
  timestamp. Returns success.
- If a row exists for a different sprint, raises an error identifying which
  sprint holds the lock and when it was acquired.
- If the row exists for the same sprint (re-entrant), returns success without
  modifying the row.
- Validates that the sprint exists in the database.

### `release_lock(db_path, sprint_id)`

- Checks whether the lock is held by the given sprint.
- If yes, deletes the row and returns success.
- If the lock is held by a different sprint, raises an error (cannot release
  another sprint's lock).
- If no lock is held, raises an error (nothing to release).

### `get_lock_holder(db_path)`

- Returns a dict with `sprint_id` and `acquired_at` if the lock is held.
- Returns `None` if no lock is held.

## Acceptance Criteria

- [ ] `acquire_lock(db_path, sprint_id)` is added to `state_db.py`
- [ ] `release_lock(db_path, sprint_id)` is added to `state_db.py`
- [ ] `get_lock_holder(db_path)` is added to `state_db.py`
- [ ] Only one sprint can hold the lock at a time (singleton table constraint)
- [ ] `acquire_lock` fails with a clear error when another sprint holds the lock, including the holder's sprint ID and acquisition time
- [ ] `acquire_lock` is re-entrant: acquiring when already held by the same sprint succeeds
- [ ] `acquire_lock` validates that the sprint exists in the database
- [ ] `release_lock` fails if the lock is held by a different sprint
- [ ] `release_lock` fails if no lock is held
- [ ] `get_lock_holder` returns holder info or None
- [ ] Lock acquisition records an ISO 8601 timestamp
- [ ] Unit tests cover acquire, release, re-entrant acquire, and all error cases
