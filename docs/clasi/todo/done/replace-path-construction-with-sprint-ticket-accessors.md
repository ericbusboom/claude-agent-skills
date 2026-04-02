---
status: done
sprint: '002'
tickets:
- 009
---

# Replace Path Construction With Sprint/Ticket Accessors

Audit all code that uses sprint and ticket objects and ensure no paths are being constructed manually via `.path()` or string concatenation. All well-known files (sprint.md, architecture-update.md, usecases.md, tickets/, tickets/done/, etc.) must be accessed through dedicated property accessors on the Sprint and Ticket classes.

This means:
- No `sprint.path / "sprint.md"` — use an accessor like `sprint.sprint_md`
- No `sprint.path / "tickets"` — use `sprint.tickets_dir`
- No ad-hoc path joins for known artifact files

Every well-known file should have a named accessor so the path structure is defined in one place.
