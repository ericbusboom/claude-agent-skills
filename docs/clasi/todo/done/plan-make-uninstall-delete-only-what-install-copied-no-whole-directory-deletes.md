---
status: done
sprint: '012'
tickets:
- 012-001
- 012-003
- 012-004
- 012-005
---

# Plan: Make uninstall delete only what install copied (no whole-directory deletes)

## Context

Right now both platform uninstallers have over-broad delete behavior
that can clobber user content. Two concrete spots:

1. **Claude `uninstall()`** does `shutil.rmtree(target_skill)` and
   `shutil.rmtree(target_agent)` for every plugin-known skill/agent
   subdirectory ([clasi/platforms/claude.py:359](clasi/platforms/claude.py#L359),
   [clasi/platforms/claude.py:373](clasi/platforms/claude.py#L373)).
   That removes the whole subdir even if the user dropped extra files
   into `.claude/skills/se/` (e.g., a `notes.md`) or
   `.claude/agents/team-lead/` (e.g., a custom `contract.yaml`).
   Install actually copies only specific files: `SKILL.md` per skill,
   and `*.md` files per agent ([claude.py:161-188](clasi/platforms/claude.py#L161-L188)).
2. **Codex `uninstall()`** cascades `rmdir` upward: removes
   `.agents/skills/` and then `.agents/` if empty
   ([codex.py:516-523](clasi/platforms/codex.py#L516-L523)). `.agents/`
   is the cross-tool standard root for skills/agents shared across
   Codex/Cursor/Gemini/Copilot/Windsurf — CLASI shouldn't delete it
   even when its skills happen to be the only resident.

The user's directive: uninstall must walk the install set and delete
only those specific files (and rmdir leaf dirs only if empty,
preserving any user-added content).

Other deletion paths in the codebase are already precise and need no
changes:
- Codex per-skill SKILL.md unlink + leaf rmdir-if-empty
  ([codex.py:510-513](clasi/platforms/codex.py#L510-L513))
- Codex `.codex/agents/<name>.toml` per-agent unlink
  ([codex.py:303-309](clasi/platforms/codex.py#L303-L309))
- Codex `.codex/agents/` rmdir-if-empty ([codex.py:312-314](clasi/platforms/codex.py#L312-L314))
- Claude rule files unlink ([claude.py:379-383](clasi/platforms/claude.py#L379-L383))
- All TOML/JSON key removals from settings.json, settings.local.json,
  .codex/config.toml, .codex/hooks.json
- AGENTS.md / CLAUDE.md marker-block strip (preserves all user content
  outside the marker block)

## Approach

Mirror the existing **codex skills** pattern (file-level delete + leaf
rmdir-if-empty) on the Claude side, and drop the cascading parent-dir
rmdir on the Codex side. No new manifest module — each uninstall walks
the same `plugin/<kind>/<name>/<files>` pattern that install walks, so
they stay symmetric by construction.

### Change 1 — Claude `uninstall()` skill section

Replace the `shutil.rmtree(target_skill)` block with a per-file delete:

```python
plugin_skills = _PLUGIN_DIR / "skills"
if plugin_skills.exists():
    for skill_dir in plugin_skills.iterdir():
        if not skill_dir.is_dir():
            continue
        target_skill = skills_dir / skill_dir.name
        if not target_skill.exists():
            continue
        # Install copies only SKILL.md per skill — mirror that.
        skill_md = target_skill / "SKILL.md"
        if skill_md.exists():
            skill_md.unlink()
        # rmdir leaf only if empty (user files preserved otherwise).
        if not any(target_skill.iterdir()):
            target_skill.rmdir()
            click.echo(f"  Removed: .claude/skills/{skill_dir.name}/")
        else:
            click.echo(
                f"  Partial: .claude/skills/{skill_dir.name}/ "
                f"(removed SKILL.md; user files preserved)"
            )
```

### Change 2 — Claude `uninstall()` agent section

Same pattern, but iterate `*.md` files (matches install at
[claude.py:181](clasi/platforms/claude.py#L181)):

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

Drop the `import shutil` from the function body — no longer needed.

### Change 3 — Codex `uninstall()` cascading parent rmdir

In [codex.py:516-523](clasi/platforms/codex.py#L516-L523), remove the
two cascading rmdirs of `.agents/skills/` and `.agents/`. Keep the
per-skill leaf rmdir-if-empty already in place at lines 510-513.
Result: empty `.agents/skills/` and `.agents/` directories may
remain after a clean uninstall — that's the right trade-off vs.
risking deletion of a directory shared with other tools.

### Change 4 — Tests

Add to [tests/unit/test_init_command.py](tests/unit/test_init_command.py):
- `test_uninstall_preserves_user_file_inside_skill_dir` — install,
  add `.claude/skills/se/notes.md`, uninstall, assert `notes.md`
  survives and `SKILL.md` is gone.
- `test_uninstall_preserves_user_file_inside_agent_dir` — install,
  add `.claude/agents/team-lead/custom.md`, uninstall, assert
  `custom.md` survives and CLASI `.md` files are gone.

Add to [tests/unit/test_platform_codex.py](tests/unit/test_platform_codex.py):
- `test_uninstall_does_not_delete_agents_root_dir` — install codex,
  add `.agents/other-tool-content.md`, uninstall, assert `.agents/`
  still exists with the user file intact.
- `test_uninstall_leaves_empty_agents_skills_dir` — install, uninstall
  cleanly, assert `.agents/skills/` may exist and be empty (or absent
  if the leaf-rmdir cascade stays gone).

## Files to modify

- `clasi/platforms/claude.py` (uninstall skill section + agent section)
- `clasi/platforms/codex.py` (drop two cascading rmdirs)
- `tests/unit/test_init_command.py` (two new tests)
- `tests/unit/test_platform_codex.py` (two new tests)

## Out of scope

- The single-source-of-truth refactor (install/uninstall sharing a
  manifest module) is appealing but separate. The code stays
  symmetric here by both sides walking the same `plugin/...`
  iterator. If/when the Claude and Codex installs diverge further,
  revisit. The codex-install rules-coverage TODO already proposes a
  shared `_rules.py` for the rule content; install/uninstall paths
  for skills+agents can join that module later if it pays off.
- The `.codex/agents/` rmdir-if-empty is already safe (the
  `if not any(iterdir())` guard preserves user files); keep it.
- Marker-block strip behavior on AGENTS.md/CLAUDE.md is already
  precise (only the CLASI block is removed, with file deletion only
  when content becomes empty); no changes.

## Verification

1. `python -m pytest --no-cov -q` — full suite must stay green.
2. The four new tests above must pass and explicitly demonstrate the
   user-file preservation.
3. Smoke: in a tmp dir, run `clasi init --claude --codex`, then
   `mkdir -p .claude/skills/se && echo notes > .claude/skills/se/notes.md`,
   then `clasi uninstall --claude --codex`. Verify `notes.md` survives
   and `.agents/` is not removed if non-empty.
