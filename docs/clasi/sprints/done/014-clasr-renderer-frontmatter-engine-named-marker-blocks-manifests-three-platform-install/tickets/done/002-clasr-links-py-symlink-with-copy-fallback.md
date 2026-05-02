---
id: '002'
title: "clasr/links.py \u2014 symlink-with-copy-fallback"
status: done
use-cases:
- SUC-003
- SUC-009
depends-on:
- '001'
github-issue: ''
todo: ''
completes_todo: false
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# clasr/links.py — symlink-with-copy-fallback

## Description

Create `clasr/links.py` — an independent implementation of the symlink-with-copy-fallback
primitive used by all `clasr` platform installers. This module is modeled on
`clasi/platforms/_links.py` but is a clean copy into the `clasr` package (Option B from
the architecture). It has no imports from `clasi` or any other `clasr` module.

## Acceptance Criteria

- [x] `clasr/links.py` exports `link_or_copy(canonical, alias, copy=False) -> str`
- [x] `link_or_copy` with `copy=False` calls `os.symlink`; on `OSError`, falls back to
      `shutil.copy2` and emits a `warnings.warn`; returns `"symlink"` or `"copy"`
- [x] `link_or_copy` with `copy=True` calls `shutil.copy2` directly (no symlink attempt);
      returns `"copy"`
- [x] `link_or_copy` creates the alias parent directory if it does not exist
- [x] `clasr/links.py` exports `unlink_alias(alias) -> bool`
- [x] `unlink_alias` removes the symlink or regular file at `alias`; returns `True` if
      removed, `False` if not found
- [x] Module has NO imports from `clasi` or any other `clasr` module
- [x] `tests/clasr/test_links.py` passes with: symlink path, copy path, OSError fallback,
      `--copy` forced mode, `unlink_alias` on symlink and regular file

## Implementation Plan

### Approach

Copy the logic from `clasi/platforms/_links.py`. The source module was analyzed and
confirmed to have no CLASI imports — it is a clean, portable module. Do NOT import from
`_links.py`; write it independently in `clasr/`. This maintains the one-way dependency.

### Files to Create

- `clasr/links.py`
- `tests/clasr/test_links.py`

### Testing Plan

`tests/clasr/test_links.py` with at least:
- `test_link_or_copy_creates_symlink`: create a real file, call `link_or_copy`; assert
  alias is a symlink pointing at canonical
- `test_link_or_copy_copy_mode`: `copy=True`; assert alias is a regular file with matching content
- `test_link_or_copy_oserror_fallback`: monkeypatch `os.symlink` to raise `OSError`;
  assert `shutil.copy2` is used and warning is emitted
- `test_link_or_copy_creates_parent_dirs`: alias under a nonexistent parent; assert parent
  is created
- `test_unlink_alias_symlink`: create a symlink, call `unlink_alias`; assert removed, returns True
- `test_unlink_alias_regular_file`: regular file; assert removed
- `test_unlink_alias_not_found`: nonexistent path; assert returns False
