---
id: '005'
title: Move state_db functions into StateDB class methods
status: done
use-cases: []
depends-on: []
github-issue: ''
todo: move-state-db-functions-to-class-methods.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Move state_db functions into StateDB class methods

## Description

Move the real logic from module-level functions in `state_db.py` into `StateDB` class methods in `state_db_class.py`. Keep `state_db.py` as thin wrappers for backward compatibility.

## Acceptance Criteria

- [x] All logic from `state_db.py` functions moved into `StateDB` class methods in `state_db_class.py`
- [x] `rename_sprint` method added to `StateDB` class (was missing)
- [x] `get_lock_holder` method added to `StateDB` class (was missing)
- [x] `state_db.py` functions replaced with thin wrappers that instantiate `StateDB` and call the method
- [x] All constants and private helpers (`PHASES`, `VALID_GATE_NAMES`, `VALID_GATE_RESULTS`, `_SCHEMA`, `_GATE_REQUIREMENTS`, `_RECOVERY_TTL`, `_now`, `_connect`) live in `state_db_class.py` and are re-exported from `state_db.py` for backward compatibility
- [x] All existing tests pass (`uv run pytest` — 803 tests)

## Testing

- **Existing tests to run**: `tests/unit/test_state_db.py`, `tests/unit/test_state_db_class.py`
- **New tests to write**: No new tests needed — existing tests fully cover the refactored code
- **Verification command**: `uv run pytest`
