---
status: done
sprint: '002'
tickets:
- '005'
---

# Move state_db Functions Into StateDB Class Methods

`state_db.py` has all the real logic as module-level functions taking `db_path` as the first arg. `state_db_class.py` wraps them in a `StateDB` class that just delegates every call. The logic should live directly in the class methods, eliminating the indirection.

Also: `rename_sprint` and `get_lock_holder` are only in the module functions, not exposed on the class.

After moving, `state_db.py` can either be removed or reduced to re-exports for backward compatibility (if callers use the module functions directly).
