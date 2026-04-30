---
id: "013-006"
title: "New module copilot.py with install/uninstall skeleton"
status: done
sprint: "013"
use-cases:
  - SUC-005
  - SUC-006
  - SUC-007
depends-on:
  - "013-001"
todo:
  - add-github-copilot-platform-support.md
---

# 013-006: New module `copilot.py` with install/uninstall skeleton

## Description

Create `clasi/platforms/copilot.py` with the public interface (`install` / `uninstall`)
and all private helper stubs. This ticket establishes the module structure so that
tickets 007-011 can work in parallel on each subsection.

The skeleton installs nothing useful yet — it calls the stubs and emits "Not yet
implemented" echoes for each subsection. The module shape mirrors `claude.py` and
`codex.py` exactly.

Includes the `.github/skills/` directory symlink to `.agents/skills/` (this is a
single `link_or_copy` call and can be fully implemented here, not deferred to a
sub-ticket).

## Acceptance Criteria

- [x] `clasi/platforms/copilot.py` exists with:
  - `install(target: Path, mcp_config: dict, copy: bool = False) -> None`
  - `uninstall(target: Path) -> None`
  - Private stubs: `_install_global_instructions`, `_uninstall_global_instructions`,
    `_install_path_rules`, `_uninstall_path_rules`, `_install_agents`,
    `_uninstall_agents`, `_install_vscode_mcp`, `_uninstall_vscode_mcp`,
    `_print_cloud_mcp_notice`.
- [x] `install()` calls each stub in order and emits a section header for each (e.g.,
      "GitHub Copilot:").
- [x] `.github/skills/` → `.agents/skills/` symlink (or copy under `--copy`) is
      implemented and functional (not a stub) in this ticket.
  - Canonical `.agents/skills/` is written first (reuse the write loop from
    `_links.link_or_copy` with source from `plugin/skills/`).
  - Then `_links.link_or_copy(.agents/skills/, .github/skills/, copy=copy)` creates
    the directory-level symlink.
- [x] `uninstall()` calls each uninstall stub and also removes the `.github/skills/`
      symlink/directory via `_links.unlink_alias`.
- [x] The module imports `_rules`, `_markers`, and `_links` (even if only `_links` is
      used in this ticket).
- [x] A minimal test confirms `install()` runs without error against a `tmp_path` and
      produces `.github/skills/` (symlink) and does not crash on the stubs.
- [x] `python -m pytest --no-cov` green.

## Implementation Plan

### Approach

Copy the overall structure of `codex.py` as a starting point. Replace the content of
each private helper with a `click.echo("  [stub] <name>")` placeholder. Implement the
skills-symlink logic directly in `install()` before calling the stubs.

For the directory-level symlink:
```python
agents_skills = target / ".agents" / "skills"
github_skills = target / ".github" / "skills"
# First, ensure canonical content exists (write if not already there)
_ensure_canonical_skills(target)
# Then symlink the directory
result = _links.link_or_copy(agents_skills, github_skills, copy=copy)
click.echo(f"  {'Symlinked' if result == 'symlink' else 'Copied'}: .github/skills/ -> .agents/skills/")
```

`_ensure_canonical_skills` can be a private helper that writes plugin skills to
`.agents/skills/` if they don't already exist (idempotent write).

### Files to Create

- `clasi/platforms/copilot.py`
- `tests/unit/test_platform_copilot.py` (minimal, expanded in tickets 007-011)

### Testing Plan

Single integration-style test: `copilot.install(tmp_path, {})`, assert
`(tmp_path / ".github" / "skills").is_symlink()`, assert target is `.agents/skills/`.

### Documentation Updates

None at this stage.
