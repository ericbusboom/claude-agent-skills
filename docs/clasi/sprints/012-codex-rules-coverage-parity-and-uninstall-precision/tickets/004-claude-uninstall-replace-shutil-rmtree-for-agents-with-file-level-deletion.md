---
id: '004'
title: 'Claude uninstall: replace shutil.rmtree for agents with file-level deletion'
status: todo
use-cases:
  - SUC-006
depends-on: []
github-issue: ''
todo: plan-make-uninstall-delete-only-what-install-copied-no-whole-directory-deletes.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Claude uninstall: replace shutil.rmtree for agents with file-level deletion

## Description

In `clasi/platforms/claude.py`, the `uninstall()` function currently removes each
plugin-known agent subdirectory with `shutil.rmtree(target_agent)`. This deletes the
entire directory tree, including any user-added files (e.g., `contract.yaml`) placed
inside `.claude/agents/team-lead/`.

The install logic copies only `*.md` files from each `plugin/agents/<name>/` directory.
Uninstall should mirror this exactly: iterate those same `*.md` files, remove each if
present, then `rmdir` the leaf directory only if empty.

## Acceptance Criteria

- [ ] `shutil.rmtree(target_agent)` is removed from `claude.py` uninstall.
- [ ] For each plugin agent dir, uninstall globs `plugin/agents/<name>/*.md` to identify
      which files were copied at install time, and removes them from `target_agent`.
- [ ] After the per-file deletions, if `target_agent` is empty, it is removed with
      `rmdir`. If non-empty, it is left in place with a "Partial" message.
- [ ] `import shutil` is fully removed from the `uninstall` function (and from the
      module-level import if it was only used in the uninstall context). Check ticket
      003 is done first; if ticket 003 already removed the only `import shutil`, this
      ticket confirms the module-level import is gone.
- [ ] New test passes: install Claude platform into a temp dir, add
      `.claude/agents/team-lead/custom.md`, run `claude.uninstall()`, assert `custom.md`
      exists, assert CLASI-installed `.md` files (e.g., `agent.md`) are gone, assert
      `.claude/agents/team-lead/` directory still exists.
- [ ] Existing test suite passes (`uv run pytest`).

## Implementation Plan

### Approach

Replace the `shutil.rmtree` block for agents (approximately lines 362-374 in
`claude.py`) with the per-file pattern from the TODO proposal:

```python
plugin_agents = _PLUGIN_DIR / "agents"
if plugin_agents.exists():
    for agent_dir in plugin_agents.iterdir():
        if not agent_dir.is_dir():
            continue
        target_agent = agents_dir / agent_dir.name
        if not target_agent.exists():
            continue
        # Install copies *.md from plugin/agents/<name>/ — mirror that.
        for plugin_md in agent_dir.glob("*.md"):
            target_md = target_agent / plugin_md.name
            if target_md.exists():
                target_md.unlink()
        if not any(target_agent.iterdir()):
            target_agent.rmdir()
            click.echo(f"  Removed: .claude/agents/{agent_dir.name}/")
        else:
            click.echo(
                f"  Partial: .claude/agents/{agent_dir.name}/ "
                f"(removed CLASI .md files; user files preserved)"
            )
```

### Files to modify

- `clasi/platforms/claude.py` — agent uninstall section; remove `import shutil` if
  ticket 003 has already removed the skills-section usage

### Testing plan

Add to `tests/unit/test_init_command.py`:

```python
def test_uninstall_preserves_user_file_inside_agent_dir(tmp_path):
    """User-added custom.md in .claude/agents/team-lead/ survives uninstall."""
    from clasi.platforms import claude
    claude.install(tmp_path, mcp_config={})

    # Simulate user dropping a file into the agent subdir
    user_file = tmp_path / ".claude" / "agents" / "team-lead" / "custom.md"
    user_file.write_text("my custom instructions", encoding="utf-8")

    claude.uninstall(tmp_path)

    assert user_file.exists(), "custom.md must survive uninstall"
    # CLASI-installed agent.md must be removed
    assert not (tmp_path / ".claude" / "agents" / "team-lead" / "agent.md").exists(), \
        "CLASI agent.md must be removed by uninstall"
    # Directory stays because it is non-empty
    assert (tmp_path / ".claude" / "agents" / "team-lead").is_dir()
```

Note: The user added `custom.md` which is a `.md` file. The install copies specific
named `.md` files from `plugin/agents/team-lead/` (e.g., `agent.md`, `contract.yaml`).
The uninstall globs `plugin/agents/team-lead/*.md` — it will see `agent.md` and any
other `.md` files from the plugin. It will NOT see `custom.md` in the plugin dir, so
`custom.md` in the target is not removed. This is the correct behavior.

If a cleaner test is preferred, use a non-`.md` user file (e.g., `contract.yaml`) to
make the distinction even more obvious — but the test above is valid because `custom.md`
is not in the plugin's agent dir.

Run: `uv run pytest tests/unit/test_init_command.py -v -k uninstall`

### Documentation updates

None required.
