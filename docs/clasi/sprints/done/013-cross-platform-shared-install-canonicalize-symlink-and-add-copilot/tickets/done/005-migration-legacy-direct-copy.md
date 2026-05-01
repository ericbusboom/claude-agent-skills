---
id: 013-005
title: Migration logic for existing direct-copy installs (--migrate flag)
status: done
sprint: '013'
use-cases:
- SUC-001
- SUC-002
depends-on:
- 013-001
---

# 013-005: Migration logic for existing direct-copy installs (`--migrate` flag)

## Description

Implement the full `--migrate` behavior that converts legacy direct-copy CLASI installs
to symlinks. The core `migrate_to_symlink` function is already in `_links.py` (ticket
001). This ticket wires it into the Claude installer (and verifies Codex has no legacy
migration need — Codex already writes canonical `.agents/skills/`).

Migration scope:
- `.claude/skills/<n>/SKILL.md` → detect if regular file matching canonical, convert.
- `CLAUDE.md` → detect if regular file matching `AGENTS.md`, convert.

The migration pass runs as part of `clasi init --migrate --claude` (before the standard
install logic). It is non-destructive: conflicts are reported but do not abort the rest
of the migration.

## Acceptance Criteria

- [x] `clasi init --claude --migrate` converts all `.claude/skills/<n>/SKILL.md`
      regular files that match their canonical to symlinks. Reports each conversion.
- [x] `clasi init --claude --migrate` converts `CLAUDE.md` if it is a regular file
      matching `AGENTS.md`. Reports the conversion.
- [x] `clasi init --claude --migrate` reports a conflict (path + message) for any file
      that cannot be converted (content mismatch) without aborting migration of other
      files.
- [x] Already-symlinked paths are skipped silently (no error, no spurious "migrated"
      message).
- [x] Non-existent paths are skipped silently.
- [x] A summary line is printed: "Migration complete: N converted, M conflicts, P skipped."
- [x] `clasi init --migrate` without `--claude` has no effect (migration is
      platform-scoped).
- [x] Unit tests cover all four `migrate_to_symlink` return values in the context of the
      Claude installer's migration pass.
- [x] `python -m pytest --no-cov` green.

## Implementation Plan

### Approach

Add a `_migrate_claude(target: Path)` private function in `claude.py` that iterates
over the expected alias paths and calls `_links.migrate_to_symlink` on each, collecting
results. Called from `install()` when `migrate=True` before the main install loop.

The function returns a summary dict `{migrated: int, conflict: int, skipped: int}` and
prints per-item messages via `click.echo`.

### Files to Modify

- `clasi/platforms/claude.py` — add `_migrate_claude` and call it when `migrate=True`.
- `tests/unit/test_platform_claude.py` — add migration scenario tests.

### Testing Plan

Set up a `tmp_path` with a legacy direct-copy `.claude/skills/` structure (regular
files, content matching the plugin source). Run `install(target, mcp_config,
migrate=True, copy=False)`. Assert symlinks exist post-migration.

Set up a conflicting file (modified content). Assert conflict is reported without
aborting other conversions.

### Documentation Updates

None — README updated in ticket 012.
