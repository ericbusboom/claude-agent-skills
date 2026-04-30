---
id: "013-003"
title: "Refactor claude.py skills install to use _links.py (symlink to canonical)"
status: todo
sprint: "013"
use-cases:
  - SUC-001
  - SUC-007
depends-on:
  - "013-001"
  - "013-002"
---

# 013-003: Refactor `claude.py` skills install to use `_links.py`

## Description

Replace the direct `shutil.copy2` skill write in `claude.py` with a two-step operation:

1. Write canonical `SKILL.md` to `.agents/skills/<n>/SKILL.md` (via `_links.link_or_copy`
   with the canonical as both source and destination — effectively a write step using the
   source from `plugin/skills/`).
2. Create alias `.claude/skills/<n>/SKILL.md` → `.agents/skills/<n>/SKILL.md` via
   `_links.link_or_copy(canonical, alias, copy=copy)`.

Update the uninstall path to call `_links.unlink_alias` on the `.claude/skills/` alias
rather than removing the file directly. The canonical `.agents/skills/<n>/SKILL.md` is
not removed by the Claude uninstaller (it is canonical).

The `--copy` flag (wired in ticket 002) is threaded through `install(target, mcp_config,
copy=copy)` to all `link_or_copy` calls.

The `--migrate` flag triggers `_links.migrate_to_symlink` on each existing
`.claude/skills/<n>/SKILL.md` path before the standard install logic.

## Acceptance Criteria

- [ ] After `clasi init --claude`, `.agents/skills/<n>/SKILL.md` exists for every
      bundled skill.
- [ ] After `clasi init --claude`, `.claude/skills/<n>/SKILL.md` is a symlink to
      `.agents/skills/<n>/SKILL.md` (default mode).
- [ ] After `clasi init --claude --copy`, `.claude/skills/<n>/SKILL.md` is a regular
      file with content identical to `.agents/skills/<n>/SKILL.md`.
- [ ] `clasi init --claude` without `--codex` still produces `.agents/skills/` canonical.
- [ ] `clasi uninstall --claude` removes `.claude/skills/<n>/SKILL.md` (symlink or copy)
      but leaves `.agents/skills/<n>/SKILL.md` intact.
- [ ] `clasi init --claude --migrate` converts an existing direct-copy
      `.claude/skills/<n>/SKILL.md` to a symlink when content matches.
- [ ] `clasi init --claude --migrate` reports a conflict (does not silently overwrite)
      when the existing file's content differs from canonical.
- [ ] Existing unit tests for Claude skills install are updated and pass.
- [ ] New unit tests cover: canonical write, symlink alias, copy alias, uninstall
      precision (alias removed, canonical preserved), migrate happy path, migrate conflict.
- [ ] `python -m pytest --no-cov` green.

## Implementation Plan

### Approach

In `_install_content` (or the skills section of `install`), replace:
```python
shutil.copy2(skill_src / "SKILL.md", dest_dir / "SKILL.md")
```
with:
```python
canonical = target / ".agents" / "skills" / skill_dir.name / "SKILL.md"
alias = target / ".claude" / "skills" / skill_dir.name / "SKILL.md"
# Write canonical
canonical.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(skill_src / "SKILL.md", canonical)
# Create alias
result = _links.link_or_copy(canonical, alias, copy=copy)
click.echo(f"  {'Symlinked' if result == 'symlink' else 'Copied'}: .claude/skills/{skill_dir.name}/SKILL.md")
```

In uninstall skills loop, replace per-file delete with `_links.unlink_alias(alias)`.

### Files to Modify

- `clasi/platforms/claude.py` — refactor skills install and uninstall sections.
- `tests/unit/test_platform_claude.py` — update and extend tests.

### Testing Plan

Use `tmp_path`. Assert `alias.is_symlink()` in default mode. Assert
`alias.read_bytes() == canonical.read_bytes()` in copy mode. After uninstall, assert
`alias.exists() is False` and `canonical.exists() is True`.

### Documentation Updates

None — README updated in ticket 012.
