---
id: '007'
title: 'Codex installer: expand docs/clasi/AGENTS.md and add docs/clasi/todo/AGENTS.md'
status: todo
use-cases:
  - SUC-002
  - SUC-003
  - SUC-004
depends-on:
  - '001'
github-issue: ''
todo: codex-install-rules-coverage-gap.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Codex installer: expand docs/clasi/AGENTS.md and add docs/clasi/todo/AGENTS.md

## Description

Two nested AGENTS.md gaps remain after sprint 011:

1. **`docs/clasi/AGENTS.md`** has a partial mirror of the `clasi-artifacts` rule.
   It is missing the active-sprint check and phase check. A Codex agent modifying
   sprint artifacts would skip these guards.

2. **`docs/clasi/todo/AGENTS.md`** does not exist. Agents working in `docs/clasi/todo/`
   get no instruction to use CLASI tooling for TODO operations.

This ticket updates `_install_rules(target)` in `codex.py` to:
- Update `_DOCS_CLASI_RULES` (or the equivalent constant/import) to the full
  `CLASI_ARTIFACTS_BODY` from `_rules.py`.
- Add a third write in `_install_rules(target)` for `docs/clasi/todo/AGENTS.md`
  using `TODO_DIR_BODY` from `_rules.py`.
- Update `_uninstall_rules(target)` to also remove `docs/clasi/todo/AGENTS.md`.

The `clasi/AGENTS.md` (source-code rule) was already covered in sprint 011; it is
aligned with `_rules.py` in ticket 001 (the constant update). No structural change
to how it is written.

## Acceptance Criteria

- [ ] `_DOCS_CLASI_RULES` in `codex.py` is replaced by the full `CLASI_ARTIFACTS_BODY`
      from `_rules.py` (adds the active-sprint check, phase check, and MCP-tools-only
      instruction that were missing).
- [ ] `_install_rules(target)` writes `docs/clasi/todo/AGENTS.md` using the
      `TODO_DIR_BODY` from `_rules.py`. The directory `docs/clasi/todo/` is created
      if absent (`mkdir(parents=True, exist_ok=True)`).
- [ ] `_uninstall_rules(target)` removes `docs/clasi/todo/AGENTS.md` if present.
- [ ] After `codex.install()`:
      - `docs/clasi/AGENTS.md` exists and contains text about active-sprint check
        and phase check (from the full `clasi-artifacts` rule).
      - `docs/clasi/todo/AGENTS.md` exists and contains text about using the
        `todo` skill or `move_todo_to_done` MCP tool.
      - `clasi/AGENTS.md` exists (unchanged from sprint 011).
- [ ] After `codex.uninstall()`:
      - `docs/clasi/AGENTS.md` is removed.
      - `docs/clasi/todo/AGENTS.md` is removed.
      - `clasi/AGENTS.md` is removed.
- [ ] Existing test suite passes (`uv run pytest`).

## Implementation Plan

### Approach

In `codex.py`:

1. Remove (or replace) the `_DOCS_CLASI_RULES` string constant. Instead, build the
   content inline from `_rules.py`:

```python
def _build_docs_clasi_content() -> str:
    from clasi.platforms._rules import CLASI_ARTIFACTS_BODY
    return f"# CLASI SE Process Rules\n\n{CLASI_ARTIFACTS_BODY}\n"

def _build_todo_dir_content() -> str:
    from clasi.platforms._rules import TODO_DIR_BODY
    return f"# CLASI TODO Rules\n\n{TODO_DIR_BODY}\n"
```

2. In `_install_rules(target)`:

```python
def _install_rules(target: Path) -> None:
    docs_clasi = target / "docs" / "clasi"
    docs_clasi.mkdir(parents=True, exist_ok=True)
    (docs_clasi / "AGENTS.md").write_text(_build_docs_clasi_content(), encoding="utf-8")
    click.echo("  Wrote: docs/clasi/AGENTS.md")

    docs_clasi_todo = target / "docs" / "clasi" / "todo"
    docs_clasi_todo.mkdir(parents=True, exist_ok=True)
    (docs_clasi_todo / "AGENTS.md").write_text(_build_todo_dir_content(), encoding="utf-8")
    click.echo("  Wrote: docs/clasi/todo/AGENTS.md")

    clasi_src = target / "clasi"
    clasi_src.mkdir(parents=True, exist_ok=True)
    (clasi_src / "AGENTS.md").write_text(_build_clasi_src_content(), encoding="utf-8")
    click.echo("  Wrote: clasi/AGENTS.md")
```

3. In `_uninstall_rules(target)`, add removal of `docs/clasi/todo/AGENTS.md`.

### Files to modify

- `clasi/platforms/codex.py` — update `_DOCS_CLASI_RULES` / `_install_rules` /
  `_uninstall_rules`

### Testing plan

Add to `tests/unit/test_platform_codex.py`:

```python
def test_docs_clasi_agents_md_has_full_clasi_artifacts_content(tmp_path):
    """docs/clasi/AGENTS.md must contain the active-sprint check and phase check."""
    from clasi.platforms import codex
    codex.install(tmp_path, mcp_config={})

    content = (tmp_path / "docs" / "clasi" / "AGENTS.md").read_text(encoding="utf-8")
    # The full clasi-artifacts rule includes these concepts
    assert "active sprint" in content.lower() or "list_sprints" in content
    assert "phase" in content.lower() or "ticketing" in content.lower()
    assert "MCP" in content or "mcp" in content.lower()

def test_docs_clasi_todo_agents_md_created(tmp_path):
    """docs/clasi/todo/AGENTS.md must be written by codex install."""
    from clasi.platforms import codex
    codex.install(tmp_path, mcp_config={})

    todo_agents = tmp_path / "docs" / "clasi" / "todo" / "AGENTS.md"
    assert todo_agents.exists()
    content = todo_agents.read_text(encoding="utf-8")
    assert "todo" in content.lower() or "move_todo_to_done" in content

def test_docs_clasi_todo_agents_md_removed_on_uninstall(tmp_path):
    """docs/clasi/todo/AGENTS.md must be removed on uninstall."""
    from clasi.platforms import codex
    codex.install(tmp_path, mcp_config={})
    codex.uninstall(tmp_path)
    assert not (tmp_path / "docs" / "clasi" / "todo" / "AGENTS.md").exists()
```

Run: `uv run pytest tests/unit/test_platform_codex.py -v -k agents_md`

### Documentation updates

None required.
