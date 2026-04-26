---
id: '005'
title: 'Codex uninstall: drop cascading rmdir of .agents/skills/ and .agents/'
status: done
use-cases:
- SUC-007
depends-on: []
github-issue: ''
todo: plan-make-uninstall-delete-only-what-install-copied-no-whole-directory-deletes.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Codex uninstall: drop cascading rmdir of .agents/skills/ and .agents/

## Description

The Codex uninstaller currently removes `.agents/skills/` and `.agents/` if they are
empty after skill removal (lines ~516-523 in `clasi/platforms/codex.py`). The `.agents/`
directory is the cross-tool standard root shared by Codex, Cursor, Gemini, Copilot, and
Windsurf. CLASI must not remove it even if its skills happen to be the only content.

The per-skill leaf `rmdir-if-empty` at lines ~510-513 is correct and must be preserved.
Only the two cascading parent rmdirs (`.agents/skills/` and `.agents/`) are removed.

## Acceptance Criteria

- [x] Lines ~516-523 in `codex.py` that cascade `rmdir` from `.agents/skills/` to
      `.agents/` are removed.
- [x] The per-skill leaf `rmdir-if-empty` (lines ~510-513) is preserved.
- [x] After a clean uninstall (no user files in `.agents/`), `.agents/skills/` and
      `.agents/` may remain as empty directories — this is acceptable.
- [x] New test passes: install Codex into a temp dir, add `.agents/other-tool.md`,
      run `codex.uninstall()`, assert `.agents/` still exists, assert
      `other-tool.md` still exists.
- [x] New test passes: install Codex into a temp dir (no extra user files), run
      `codex.uninstall()`, confirm no exception raised even if `.agents/skills/` or
      `.agents/` remain non-empty (empty dirs are OK remaining).
- [x] Existing test suite passes (`uv run pytest`).

## Implementation Plan

### Approach

Locate the cascading rmdir block in `codex.py`'s `uninstall()` function. The current
code looks like:

```python
        # Remove .agents/skills/ if now empty
        if skills_dir.exists() and not any(skills_dir.iterdir()):
            skills_dir.rmdir()
            click.echo("  Removed: .agents/skills/ (empty)")
        # Remove .agents/ if now empty
        agents_root = target / ".agents"
        if agents_root.exists() and not any(agents_root.iterdir()):
            agents_root.rmdir()
            click.echo("  Removed: .agents/ (empty)")
```

Delete these ~8 lines entirely. The per-skill loop above this block (which does
`skill_md.unlink()` + leaf `rmdir-if-empty`) stays untouched.

### Files to modify

- `clasi/platforms/codex.py` — remove the two cascading rmdir blocks after the per-skill
  loop in `uninstall()`

### Testing plan

Add to `tests/unit/test_platform_codex.py`:

```python
def test_uninstall_does_not_delete_agents_root_dir(tmp_path):
    """CLASI uninstall must not remove .agents/ even if it leaves it empty."""
    from clasi.platforms import codex
    codex.install(tmp_path, mcp_config={})

    # Simulate another tool using .agents/
    other_file = tmp_path / ".agents" / "other-tool.md"
    other_file.write_text("other tool content", encoding="utf-8")

    codex.uninstall(tmp_path)

    assert (tmp_path / ".agents").is_dir(), ".agents/ must survive CLASI uninstall"
    assert other_file.exists(), "other tool file must survive CLASI uninstall"


def test_uninstall_does_not_raise_when_agents_dir_becomes_empty(tmp_path):
    """Clean uninstall must not raise even if .agents/ remains as an empty dir."""
    from clasi.platforms import codex
    codex.install(tmp_path, mcp_config={})
    # No extra files — clean state
    codex.uninstall(tmp_path)
    # .agents/ or .agents/skills/ may or may not exist — just no exception
```

Run: `uv run pytest tests/unit/test_platform_codex.py -v -k uninstall`

### Documentation updates

None required.
