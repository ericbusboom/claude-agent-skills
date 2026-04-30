---
id: 013-004
title: Refactor claude.py CLAUDE.md write to symlink AGENTS.md
status: done
sprint: '013'
use-cases:
- SUC-002
- SUC-007
depends-on:
- 013-001
- 013-002
---

# 013-004: Refactor `claude.py` `CLAUDE.md` write to symlink `AGENTS.md`

## Description

Replace the direct `write_section(target / "CLAUDE.md", ...)` call in `claude.py` with
a two-step operation:

1. Write (or update) `AGENTS.md` with the CLASI entry-point block via `write_section`.
   `AGENTS.md` becomes the authoritative instruction file.
2. Create `CLAUDE.md` → `AGENTS.md` via `_links.link_or_copy(canonical=AGENTS.md,
   alias=CLAUDE.md, copy=copy)`.

Pre-install guard: if `CLAUDE.md` already exists as a regular file (not a symlink to
`AGENTS.md`), check content match:
- Content matches `AGENTS.md`: replace with symlink (or skip if `--copy` mode and
  content is already identical).
- Content does not match: error with "Use --migrate to convert" message.

Uninstall: call `_links.unlink_alias(CLAUDE.md)`. Also call `strip_section(AGENTS.md)`
if and only if the Codex installer is NOT also installed (guard: check for `.codex/`
presence in target). This prevents stripping Codex's entry-point block when only the
Claude platform is being uninstalled.

## Acceptance Criteria

- [x] After `clasi init --claude`, `CLAUDE.md` is a symlink to `AGENTS.md`.
- [x] After `clasi init --claude --copy`, `CLAUDE.md` is a regular file with content
      identical to `AGENTS.md`.
- [x] `clasi init --claude` without `--codex` writes `AGENTS.md` and creates the
      `CLAUDE.md` symlink. Both files exist.
- [x] `clasi uninstall --claude` removes `CLAUDE.md` (symlink or copy). `AGENTS.md`
      remains.
- [x] If `CLAUDE.md` exists as a regular file matching `AGENTS.md` content, re-running
      `clasi init --claude` converts it to a symlink (or leaves the identical copy in
      `--copy` mode).
- [x] If `CLAUDE.md` exists as a regular file NOT matching `AGENTS.md` content, install
      exits with a clear error message suggesting `--migrate`.
- [x] `clasi uninstall --claude` strips the Claude entry-point block from `AGENTS.md`
      only when Codex is not installed (`.codex/` absent).
- [x] All existing `CLAUDE.md`-related tests are updated and pass.
- [x] New tests cover: symlink creation, copy mode, conflict detection, uninstall
      (symlink removed, AGENTS.md preserved), mixed-platform uninstall (AGENTS.md
      block preserved when Codex still installed).
- [x] `python -m pytest --no-cov` green.

## Implementation Plan

### Approach

In `_write_claude_md` (or the equivalent section of `install`):
```python
agents_md = target / "AGENTS.md"
claude_md = target / "CLAUDE.md"

# Write/update AGENTS.md
write_section(agents_md, entry_point=body)

# Guard: check existing CLAUDE.md
if claude_md.exists() and not claude_md.is_symlink():
    if claude_md.read_bytes() != agents_md.read_bytes():
        click.echo("Error: CLAUDE.md exists with different content. Use --migrate.")
        return
    # else: content matches, fall through to create symlink (replaces file)

# Create alias
result = _links.link_or_copy(agents_md, claude_md, copy=copy)
click.echo(f"  {'Symlinked' if result == 'symlink' else 'Copied'}: CLAUDE.md -> AGENTS.md")
```

In uninstall:
```python
_links.unlink_alias(target / "CLAUDE.md")
codex_installed = (target / ".codex").exists()
if not codex_installed:
    strip_section(target / "AGENTS.md")
```

### Files to Modify

- `clasi/platforms/claude.py` — refactor `_write_claude_md` and the corresponding
  uninstall section.
- `tests/unit/test_platform_claude.py` — update and extend tests.

### Testing Plan

Use `tmp_path`. Test with pre-existing `CLAUDE.md` in various states (absent, symlink,
matching file, non-matching file). Test uninstall with and without `.codex/` present.

### Documentation Updates

None — README updated in ticket 012.
