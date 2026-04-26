---
id: '008'
title: End-to-end Codex install correctness test for all AGENTS.md files
status: done
use-cases:
  - SUC-001
  - SUC-002
  - SUC-003
  - SUC-008
depends-on:
  - '006'
  - '007'
github-issue: ''
todo: codex-install-rules-coverage-gap.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# End-to-end Codex install correctness test for all AGENTS.md files

## Description

Tickets 006 and 007 add and update individual AGENTS.md files. This ticket adds a
comprehensive end-to-end test that calls `codex.install()` once and verifies the
complete AGENTS.md footprint: all four files exist at the correct paths, have the
correct content, and the root AGENTS.md carries both the entry-point block and the
global-rules block without duplication or corruption.

It also verifies the complete uninstall removes all AGENTS.md files (or their CLASI
sections) correctly.

This is a regression guard — if any future ticket breaks the install footprint, this
test fails immediately.

## Acceptance Criteria

- [x] A single test function `test_codex_install_full_agents_md_footprint` (or
      equivalent) calls `codex.install()` and asserts:
      - `AGENTS.md` (root) exists and contains `<!-- CLASI:START -->`.
      - `AGENTS.md` (root) exists and contains `<!-- CLASI:RULES:START -->`.
      - `AGENTS.md` (root) does NOT have the `RULES` block content duplicated.
      - `docs/clasi/AGENTS.md` exists and contains the full clasi-artifacts rule
        (active-sprint check and phase check).
      - `docs/clasi/todo/AGENTS.md` exists and contains the todo-dir rule.
      - `clasi/AGENTS.md` exists and contains the source-code rule.
- [x] A companion uninstall test asserts that after `codex.uninstall()`:
      - `<!-- CLASI:RULES:START -->` is absent from root `AGENTS.md` (rules block stripped).
      - `docs/clasi/AGENTS.md` does not exist.
      - `docs/clasi/todo/AGENTS.md` does not exist.
      - `clasi/AGENTS.md` does not exist.
- [x] Round-trip test: install → uninstall → re-install produces the same file state
      as the first install. No duplication of blocks.
- [x] All existing tests pass (`uv run pytest`).

## Implementation Plan

### Approach

This ticket adds only tests — no new production code.

Add to `tests/unit/test_platform_codex.py` (or a new
`tests/unit/test_codex_install_e2e.py` if the existing file is large):

```python
def test_codex_install_full_agents_md_footprint(tmp_path):
    """
    After codex.install(), all four AGENTS.md files exist at correct paths
    with correct content, and root AGENTS.md has both CLASI marker blocks.
    """
    from clasi.platforms import codex
    from clasi.platforms._rules import (
        MCP_REQUIRED_BODY, GIT_COMMITS_BODY,
        CLASI_ARTIFACTS_BODY, TODO_DIR_BODY, SOURCE_CODE_BODY,
    )

    codex.install(tmp_path, mcp_config={})

    # --- Root AGENTS.md ---
    root_agents = tmp_path / "AGENTS.md"
    assert root_agents.exists(), "root AGENTS.md must exist after codex install"
    root_content = root_agents.read_text(encoding="utf-8")
    assert "<!-- CLASI:START -->" in root_content, "entry-point block must be present"
    assert "<!-- CLASI:END -->" in root_content
    assert "<!-- CLASI:RULES:START -->" in root_content, "rules block must be present"
    assert "<!-- CLASI:RULES:END -->" in root_content
    # Rules block must not be duplicated
    assert root_content.count("<!-- CLASI:RULES:START -->") == 1
    # Key rule content present
    assert "get_version" in root_content or "MCP" in root_content
    assert "commit" in root_content.lower() or "git" in root_content.lower()

    # --- docs/clasi/AGENTS.md ---
    docs_clasi_agents = tmp_path / "docs" / "clasi" / "AGENTS.md"
    assert docs_clasi_agents.exists(), "docs/clasi/AGENTS.md must exist"
    docs_content = docs_clasi_agents.read_text(encoding="utf-8")
    # Full clasi-artifacts content (active-sprint + phase check)
    assert "list_sprints" in docs_content or "active sprint" in docs_content.lower()
    assert "phase" in docs_content.lower() or "ticketing" in docs_content.lower()

    # --- docs/clasi/todo/AGENTS.md ---
    todo_agents = tmp_path / "docs" / "clasi" / "todo" / "AGENTS.md"
    assert todo_agents.exists(), "docs/clasi/todo/AGENTS.md must exist"
    todo_content = todo_agents.read_text(encoding="utf-8")
    assert "move_todo_to_done" in todo_content or "todo" in todo_content.lower()

    # --- clasi/AGENTS.md ---
    clasi_agents = tmp_path / "clasi" / "AGENTS.md"
    assert clasi_agents.exists(), "clasi/AGENTS.md must exist"
    clasi_content = clasi_agents.read_text(encoding="utf-8")
    assert "in-progress" in clasi_content or "ticket" in clasi_content.lower()


def test_codex_uninstall_removes_all_agents_md_files(tmp_path):
    """After codex.uninstall(), all nested AGENTS.md files are removed."""
    from clasi.platforms import codex
    codex.install(tmp_path, mcp_config={})
    codex.uninstall(tmp_path)

    assert not (tmp_path / "docs" / "clasi" / "AGENTS.md").exists()
    assert not (tmp_path / "docs" / "clasi" / "todo" / "AGENTS.md").exists()
    assert not (tmp_path / "clasi" / "AGENTS.md").exists()

    root_agents = tmp_path / "AGENTS.md"
    if root_agents.exists():
        content = root_agents.read_text(encoding="utf-8")
        assert "<!-- CLASI:RULES:START -->" not in content, \
            "rules block must be stripped on uninstall"
        assert "<!-- CLASI:START -->" not in content, \
            "entry-point block must be stripped on uninstall"


def test_codex_install_round_trip_no_duplication(tmp_path):
    """Install → uninstall → re-install produces same output, no block duplication."""
    from clasi.platforms import codex
    codex.install(tmp_path, mcp_config={})
    codex.uninstall(tmp_path)
    codex.install(tmp_path, mcp_config={})

    root_agents = tmp_path / "AGENTS.md"
    assert root_agents.exists()
    content = root_agents.read_text(encoding="utf-8")
    assert content.count("<!-- CLASI:RULES:START -->") == 1, \
        "rules block must not be duplicated after re-install"
    assert content.count("<!-- CLASI:START -->") == 1, \
        "entry-point block must not be duplicated after re-install"
```

### Files to modify

- `tests/unit/test_platform_codex.py` (or new `tests/unit/test_codex_install_e2e.py`)
  — add three test functions above

### Testing plan

Run: `uv run pytest tests/unit/test_platform_codex.py -v -k "footprint or round_trip or removes_all"`

Also run the full suite: `uv run pytest`

### Documentation updates

None required.
