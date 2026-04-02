---
status: done
sprint: '002'
tickets:
- '006'
---

# Move Todo Functions Into the Todo Class

The module-level functions in `todo.py` (and related tool code) should be moved into methods on the Todo class. Same pattern as the other domain model refactors — the Todo class should own its own logic for creation, status changes, moving to done, etc.
