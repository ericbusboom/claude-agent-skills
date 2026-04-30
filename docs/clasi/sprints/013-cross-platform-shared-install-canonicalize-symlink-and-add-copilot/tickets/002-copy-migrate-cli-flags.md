---
id: "013-002"
title: "Add --copy and --migrate flags to clasi init and clasi uninstall CLI"
status: todo
sprint: "013"
use-cases:
  - SUC-003
depends-on: []
---

# 013-002: Add `--copy` and `--migrate` flags to `clasi init` and `clasi uninstall` CLI

## Description

Extend the `clasi init` and `clasi uninstall` commands with two new flags:

- `--copy` / `--no-copy`: when set, all alias operations use `shutil.copy2` instead of
  `os.symlink`. Default: `False` (symlink-first).
- `--migrate`: when set, the install pass calls `_links.migrate_to_symlink` on each
  existing alias path before installing. Converts legacy direct-copy installs to
  symlinks. Only applicable if `--copy` is not also set.

These flags are scaffolding — platform installers wired up in tickets 003, 004, 006+
will thread them through. This ticket adds the CLI surface and threads the flags as far
as the `install()` / `uninstall()` call sites in `init_command.py`.

## Acceptance Criteria

- [ ] `clasi init --copy` is accepted without error.
- [ ] `clasi init --migrate` is accepted without error.
- [ ] `clasi uninstall --copy` is accepted without error.
- [ ] The `copy` boolean is threaded to `claude.install(target, mcp_config, copy=copy)`,
      `codex.install(target, mcp_config, copy=copy)` (add the kwarg even if codex.py
      does not yet use it). Copilot wiring added in ticket 011.
- [ ] The `migrate` boolean is threaded to installer call sites (platform installers
      will read it in their own tickets; stubbing the parameter is sufficient here).
- [ ] The interactive platform prompt is updated to note that Copilot is available as
      a platform option (even if the `--copilot` wiring is completed in ticket 011);
      this is a placeholder update to avoid a double-touch of the prompt logic.
- [ ] Existing behavior with no new flags is unchanged (all existing tests pass).
- [ ] `python -m pytest --no-cov` green.

## Implementation Plan

### Approach

Add Click options in `clasi/cli.py` (or `init_command.py` and `uninstall_command.py`
depending on where flags live — check existing pattern). Thread the `copy` kwarg through
to `claude.install` and `codex.install` signatures as a no-op defaulting to `False` in
those modules (the actual behavior change comes in tickets 003 and 004).

### Files to Modify

- `clasi/init_command.py` — add `--copy` / `--migrate` options; thread to installer calls.
- `clasi/uninstall_command.py` — add `--copy` option; thread to uninstaller calls.
- `clasi/cli.py` — add options at the command decorator level if flags are defined there.
- `clasi/platforms/claude.py` — add `copy: bool = False` and `migrate: bool = False`
  kwargs to `install()` and `uninstall()` signatures (no behavior change yet).
- `clasi/platforms/codex.py` — same kwargs (no behavior change yet).

### Testing Plan

Extend existing CLI tests in `tests/unit/test_init_command.py` and
`tests/unit/test_uninstall_command.py` to invoke with `--copy` and assert no error.
No new behavioral tests yet (behavior comes in tickets 003/004).

### Documentation Updates

None at this stage.
