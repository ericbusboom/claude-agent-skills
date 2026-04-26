---
id: '003'
title: 'Claude uninstall: replace shutil.rmtree for skills with file-level deletion'
status: todo
use-cases:
  - SUC-005
depends-on: []
github-issue: ''
todo: plan-make-uninstall-delete-only-what-install-copied-no-whole-directory-deletes.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Claude uninstall: replace shutil.rmtree for skills with file-level deletion

## Description

In `clasi/platforms/claude.py`, the `uninstall()` function currently removes each
plugin-known skill subdirectory with `shutil.rmtree(target_skill)`. This deletes the
entire directory tree, including any user-added files (e.g., `notes.md`) placed inside
`.claude/skills/se/`.

The install logic copies only `SKILL.md` per skill. Uninstall should mirror this exactly:
remove only `SKILL.md`, then `rmdir` the leaf directory if and only if it is empty.

## Acceptance Criteria

- [ ] `shutil.rmtree(target_skill)` is removed from `claude.py` uninstall.
- [ ] For each plugin skill, uninstall removes only `target_skill / "SKILL.md"` if it
      exists.
- [ ] After removing `SKILL.md`, if `target_skill` is empty, it is removed with `rmdir`.
      If non-empty, it is left in place and a "Partial" message is emitted.
- [ ] `import shutil` is removed from the `uninstall` function body if no longer needed
      elsewhere in the function. (Check first — the agent section currently also imports
      shutil; once ticket 004 is done, the import can be removed from the module level
      if the function-level import was the last reference.)
- [ ] New test passes: install Claude platform into a temp dir, add
      `.claude/skills/se/notes.md`, run `claude.uninstall()`, assert `notes.md` exists,
      assert `.claude/skills/se/SKILL.md` does not exist, assert `.claude/skills/se/`
      directory still exists (non-empty).
- [ ] Existing test suite passes (`uv run pytest`).

## Implementation Plan

### Approach

Replace the `shutil.rmtree` block for skills (approximately lines 350-360 in
`claude.py`) with the per-file pattern from the TODO proposal:

```python
plugin_skills = _PLUGIN_DIR / "skills"
if plugin_skills.exists():
    for skill_dir in plugin_skills.iterdir():
        if not skill_dir.is_dir():
            continue
        target_skill = skills_dir / skill_dir.name
        if not target_skill.exists():
            continue
        skill_md = target_skill / "SKILL.md"
        if skill_md.exists():
            skill_md.unlink()
        if not any(target_skill.iterdir()):
            target_skill.rmdir()
            click.echo(f"  Removed: .claude/skills/{skill_dir.name}/")
        else:
            click.echo(
                f"  Partial: .claude/skills/{skill_dir.name}/ "
                f"(removed SKILL.md; user files preserved)"
            )
```

The outer `if skills_dir.exists() and _PLUGIN_DIR.exists():` guard stays.

### Files to modify

- `clasi/platforms/claude.py` — skill uninstall section only

### Testing plan

Add to `tests/unit/test_init_command.py`:

```python
def test_uninstall_preserves_user_file_inside_skill_dir(tmp_path):
    """User-added notes.md in .claude/skills/se/ survives uninstall."""
    from clasi.platforms import claude
    claude.install(tmp_path, mcp_config={})

    # Simulate user dropping a file into the skill subdir
    user_file = tmp_path / ".claude" / "skills" / "se" / "notes.md"
    user_file.write_text("my notes", encoding="utf-8")

    claude.uninstall(tmp_path)

    assert user_file.exists(), "user notes.md must survive uninstall"
    assert not (tmp_path / ".claude" / "skills" / "se" / "SKILL.md").exists(), \
        "SKILL.md must be removed by uninstall"
    # Directory stays because it is non-empty
    assert (tmp_path / ".claude" / "skills" / "se").is_dir()
```

Run: `uv run pytest tests/unit/test_init_command.py -v -k uninstall`

### Documentation updates

None required.
