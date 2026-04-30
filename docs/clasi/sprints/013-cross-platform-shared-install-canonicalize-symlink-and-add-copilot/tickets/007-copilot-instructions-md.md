---
id: "013-007"
title: "Copilot: .github/copilot-instructions.md writer"
status: todo
sprint: "013"
use-cases:
  - SUC-005
  - SUC-008
depends-on:
  - "013-006"
---

# 013-007: Copilot: `.github/copilot-instructions.md` writer

## Description

Implement `_install_global_instructions` and `_uninstall_global_instructions` in
`copilot.py`.

The file `.github/copilot-instructions.md` is the primary Copilot instruction file
(legacy/secondary; still active for cloud + IDE). It is marker-managed via
`_markers.write_section`, preserving any user content outside the CLASI block.

Content of the CLASI block:
- Entry-point sentence pointing at `.github/agents/team-lead.agent.md` (analogous to
  the Codex entry-point pointing at `.codex/agents/team-lead.toml`).
- Global-scope rule bodies from `_rules.py`: `MCP_REQUIRED_BODY` and `GIT_COMMITS_BODY`.

Also implement `_print_cloud_mcp_notice` in this ticket (it is logically part of the
instructions footprint and has no dependencies on other subsections).

## Acceptance Criteria

- [ ] After `_install_global_instructions(target)`, `.github/copilot-instructions.md`
      exists with a CLASI marker block containing the entry-point sentence and global
      rules content.
- [ ] Re-running `_install_global_instructions` on an existing file preserves user
      content outside the marker block.
- [ ] The entry-point sentence references `.github/agents/team-lead.agent.md`.
- [ ] After `_uninstall_global_instructions(target)`, the CLASI marker block is stripped.
      User content outside the block is preserved. The file is not deleted.
- [ ] `_print_cloud_mcp_notice(mcp_config)` prints to stdout:
  - A header line: "Copilot Cloud Coding Agent MCP (manual step required):"
  - The GitHub Settings URL pattern for the repo.
  - The exact JSON snippet to paste.
- [ ] `install()` calls `_print_cloud_mcp_notice` after all install steps.
- [ ] Tests cover: file creation, marker block content, re-install idempotency (user
      content preserved), uninstall (block stripped, user content preserved), cloud
      notice output.
- [ ] `python -m pytest --no-cov` green.

## Implementation Plan

### Approach

Model `_install_global_instructions` on `codex.py`'s `_write_agents_md` / global-rules
block pattern:

```python
def _install_global_instructions(target: Path) -> None:
    path = target / ".github" / "copilot-instructions.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    body = (
        "Read `.github/agents/team-lead.agent.md` at session start "
        "and follow the team-lead role definition.\n\n"
        "## MCP Required\n\n" + MCP_REQUIRED_BODY + "\n\n"
        "## Git Commits\n\n" + GIT_COMMITS_BODY
    )
    write_section(path, entry_point=body)
    click.echo("  Wrote: .github/copilot-instructions.md")
```

For `_print_cloud_mcp_notice`, emit a `click.echo` block with the JSON snippet. The
exact JSON shape for the MCP server entry should mirror `.mcp.json` (verify during
implementation against GitHub Copilot docs for cloud MCP server format).

### Files to Modify

- `clasi/platforms/copilot.py` — implement `_install_global_instructions`,
  `_uninstall_global_instructions`, `_print_cloud_mcp_notice`.
- `tests/unit/test_platform_copilot.py` — add tests for these helpers.

### Testing Plan

Use `tmp_path`. Write a pre-existing `copilot-instructions.md` with user content;
confirm it survives re-install. Check strip leaves user content. Capture `click.echo`
output for cloud notice test.

### Documentation Updates

None at this stage.
