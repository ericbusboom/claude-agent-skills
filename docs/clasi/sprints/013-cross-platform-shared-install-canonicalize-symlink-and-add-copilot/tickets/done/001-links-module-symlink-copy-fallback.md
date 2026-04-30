---
id: "013-001"
title: "New module _links.py: symlink-with-copy-fallback helper"
status: done
sprint: "013"
use-cases:
  - SUC-001
  - SUC-002
  - SUC-003
  - SUC-007
depends-on: []
todo:
  - cross-platform-agent-config-canonicalize-and-symlink.md
---

# 013-001: New module `_links.py`: symlink-with-copy-fallback helper

## Description

Create `clasi/platforms/_links.py` — a new leaf-level shared module that provides
the "symlink-with-copy-fallback" primitive used by all three platform installers
(claude.py, codex.py, copilot.py). This is the foundation ticket for Track A.

The module has no CLASI imports and no platform knowledge. It is a pure filesystem
helper.

## Acceptance Criteria

- [x] `_links.py` exports `link_or_copy(canonical: Path, alias: Path, copy: bool = False) -> str`.
- [x] When `copy=False` (default): `os.symlink(canonical, alias)` is attempted; on
      `OSError` falls back to `shutil.copy2` and returns `"copy"`.
- [x] When `copy=True`: `shutil.copy2` is used directly; returns `"copy"`.
- [x] When symlink succeeds: returns `"symlink"`.
- [x] Alias parent directory is created (`parents=True, exist_ok=True`) if absent.
- [x] `_links.py` exports `unlink_alias(alias: Path) -> bool`.
  - Returns `True` if the alias existed and was removed (works for both symlinks and
    regular files).
  - Returns `False` if the alias did not exist.
  - Never touches the canonical path.
- [x] `_links.py` exports `migrate_to_symlink(canonical: Path, alias: Path) -> str`.
  - Returns `"already-symlink"` if `alias` is already a symlink pointing at `canonical`.
  - Returns `"migrated"` if `alias` was a content-matching regular file: removes it,
    creates symlink.
  - Returns `"conflict"` if `alias` is a regular file with content not matching `canonical`.
  - Returns `"not-found"` if `alias` does not exist.
- [x] `tests/unit/test_links.py` is created and covers:
  - `link_or_copy` symlink path (mock or real tmp dir).
  - `link_or_copy` copy path (via `copy=True`).
  - `link_or_copy` fallback path (force `OSError` on `os.symlink`).
  - `unlink_alias` removes symlink without touching canonical.
  - `unlink_alias` removes regular file without touching canonical.
  - `unlink_alias` returns `False` for non-existent path.
  - `migrate_to_symlink` all four return values.
- [x] Full test suite green (`python -m pytest --no-cov`).

## Implementation Plan

### Approach

Write the module from scratch. No external dependencies beyond stdlib (`os`, `pathlib`,
`shutil`). The fallback logic uses a try/except around `os.symlink`.

### Files to Create

- `clasi/platforms/_links.py` — new module.
- `tests/unit/test_links.py` — new test file.

### Files to Modify

None in this ticket. Platform installers consume `_links.py` in subsequent tickets.

### Testing Plan

Use `tmp_path` pytest fixture for real filesystem tests. For the fallback path, use
`monkeypatch` to raise `OSError` on `os.symlink`. Confirm symlink vs regular file with
`alias.is_symlink()` assertions.

### Documentation Updates

None required at this stage. README updated in ticket 012.
