---
id: '006'
title: 'Codex installer: write global-rules block on root AGENTS.md'
status: done
use-cases:
  - SUC-001
  - SUC-008
depends-on:
  - '001'
  - '002'
github-issue: ''
todo: codex-install-rules-coverage-gap.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Codex installer: write global-rules block on root AGENTS.md

## Description

The root `AGENTS.md` already carries the CLASI entry-point block (written by
`_write_agents_md`). Codex agents working anywhere in the project should also see the
two global-scope rules: `mcp-required` and `git-commits`. These rules need a home at
the project root because their effective scope in Claude is `paths: ["**"]` (or near-
global). In Codex, root AGENTS.md is the equivalent.

This ticket adds `_install_global_rules(target)` and `_uninstall_global_rules(target)`
to `codex.py`. Both use the new `write_named_section`/`strip_named_section` API from
ticket 002 with `block_name="RULES"`. Content is sourced from `_rules.py` (ticket 001).

Note on scope: `git-commits.md` in `claude.py` has `paths: ["**/*.py", "**/*.md"]`
rather than a pure `**`. For Codex purposes, root AGENTS.md is the correct home — it
applies broadly to project-root agents which is close enough to the intent.

## Acceptance Criteria

- [x] `codex.py` has `_install_global_rules(target: Path)` that calls
      `_markers.write_named_section(target / "AGENTS.md", "RULES", global_content)`
      where `global_content` is the concatenated `MCP_REQUIRED_BODY` and
      `GIT_COMMITS_BODY` from `_rules.py` (with a heading per rule).
- [x] `codex.py` has `_uninstall_global_rules(target: Path)` that calls
      `_markers.strip_named_section(target / "AGENTS.md", "RULES")`.
- [x] `codex.install()` calls `_install_global_rules(target)`.
- [x] `codex.uninstall()` calls `_uninstall_global_rules(target)`.
- [x] After `codex.install()`, root `AGENTS.md` contains:
      - The original CLASI entry-point block (`<!-- CLASI:START -->...<!-- CLASI:END -->`).
      - The new rules block (`<!-- CLASI:RULES:START -->...<!-- CLASI:RULES:END -->`).
      - The `mcp-required` body inside the rules block.
      - The `git-commits` body inside the rules block.
- [x] After `codex.uninstall()`, only the rules block is stripped. The entry-point block
      survives (or is stripped separately by its own code path — it must not be damaged
      by `_uninstall_global_rules`).
- [x] Round-trip test: install, uninstall, re-install — root AGENTS.md ends up with both
      blocks each time with no duplication.
- [x] Existing test suite passes (`uv run pytest`).

## Implementation Plan

### Approach

1. In `_rules.py` (from ticket 001), constants `MCP_REQUIRED_BODY` and `GIT_COMMITS_BODY`
   are already available.

2. Add to `codex.py`:

```python
def _build_global_rules_content() -> str:
    """Build the content for the global-scope rules block on root AGENTS.md."""
    from clasi.platforms._rules import MCP_REQUIRED_BODY, GIT_COMMITS_BODY
    return (
        "# Global CLASI Rules\n\n"
        "## MCP Server Required\n\n"
        f"{MCP_REQUIRED_BODY}\n\n"
        "## Git Commits\n\n"
        f"{GIT_COMMITS_BODY}\n"
    )

def _install_global_rules(target: Path) -> None:
    from clasi.platforms._markers import write_named_section
    content = _build_global_rules_content()
    write_named_section(target / "AGENTS.md", "RULES", content)
    click.echo("  Wrote: AGENTS.md (global rules block)")

def _uninstall_global_rules(target: Path) -> None:
    from clasi.platforms._markers import strip_named_section
    strip_named_section(target / "AGENTS.md", "RULES")
```

3. In `codex.install()`, call `_install_global_rules(target)` after the existing
   `_write_agents_md(target)` call (so the entry-point block is written first).

4. In `codex.uninstall()`, call `_uninstall_global_rules(target)` after the existing
   `strip_section(target / "AGENTS.md")` call.

### Files to modify

- `clasi/platforms/codex.py` — add `_install_global_rules`, `_uninstall_global_rules`,
  `_build_global_rules_content`; wire into `install()` and `uninstall()`

### Testing plan

Add to `tests/unit/test_platform_codex.py`:

```python
def test_global_rules_block_present_after_install(tmp_path):
    """Root AGENTS.md must contain both the entry-point block and the rules block."""
    from clasi.platforms import codex
    codex.install(tmp_path, mcp_config={})

    content = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "<!-- CLASI:START -->" in content
    assert "<!-- CLASI:RULES:START -->" in content
    assert "<!-- CLASI:RULES:END -->" in content
    # Check rule content is present
    assert "MCP server" in content or "get_version" in content
    assert "git" in content.lower() or "commit" in content.lower()

def test_global_rules_block_stripped_on_uninstall(tmp_path):
    """Uninstall removes only the rules block; entry-point block must survive if present."""
    from clasi.platforms import codex
    codex.install(tmp_path, mcp_config={})
    codex.uninstall(tmp_path)

    # After uninstall, AGENTS.md may be deleted (if it only had CLASI content)
    # or may still exist with only user content. In any case:
    agents_md = tmp_path / "AGENTS.md"
    if agents_md.exists():
        content = agents_md.read_text(encoding="utf-8")
        assert "<!-- CLASI:RULES:START -->" not in content
```

Run: `uv run pytest tests/unit/test_platform_codex.py -v -k global_rules`

### Documentation updates

None required — the rules content is self-documenting inside the installed AGENTS.md.
