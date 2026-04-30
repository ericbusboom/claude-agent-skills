---
id: "013-010"
title: "Copilot: .vscode/mcp.json JSON-merge writer"
status: done
sprint: "013"
use-cases:
  - SUC-005
  - SUC-007
depends-on:
  - "013-006"
---

# 013-010: Copilot: `.vscode/mcp.json` JSON-merge writer

## Description

Implement `_install_vscode_mcp` and `_uninstall_vscode_mcp` in `copilot.py`.

`.vscode/mcp.json` is the workspace MCP configuration for VS Code / JetBrains / Visual
Studio with Copilot agent mode. The merge strategy mirrors `_update_mcp_json` in
`init_command.py` (for `.mcp.json`):

- If the file does not exist: create with `{"servers": {"clasi": <mcp_config>}}`.
- If it exists and parses as JSON: merge `servers.clasi` key, preserving all other
  keys.
- If it exists but does not parse (corrupt JSON): log an error and skip — never
  overwrite user content.

Uninstall: remove the `servers.clasi` key from `.vscode/mcp.json`. If the `servers`
object becomes empty, consider leaving the file intact (user may have other entries
added later). If the entire file only contained CLASI's entry, leave it with an empty
`servers` object (do not delete the file).

Note: Verify the exact JSON shape for VS Code MCP during implementation. The expected
shape based on VS Code docs is `{"servers": {"clasi": {"command": "clasi",
"args": ["mcp"]}}}` — confirm against current VS Code MCP documentation before writing.

## Acceptance Criteria

- [x] After `_install_vscode_mcp(target, mcp_config)` on a clean target, `.vscode/mcp.json`
      exists with `servers.clasi` set to `mcp_config`.
- [x] After `_install_vscode_mcp` on an existing `.vscode/mcp.json` with user content,
      the user content is preserved and `servers.clasi` is added/updated.
- [x] If `.vscode/mcp.json` is corrupt JSON, an error is printed and the file is not
      modified.
- [x] After `_uninstall_vscode_mcp(target)`, `servers.clasi` is removed from
      `.vscode/mcp.json`. Other keys in `servers` are preserved.
- [x] `.vscode/` directory is created if absent on install.
- [x] `.vscode/` directory is NOT deleted on uninstall (user may have other VS Code
      config there).
- [x] Tests: fresh install (file created), merge into existing (user keys preserved),
      corrupt-JSON guard (file unchanged), uninstall (key removed, other keys intact).
- [x] `python -m pytest --no-cov` green.

## Implementation Plan

### Approach

```python
def _install_vscode_mcp(target: Path, mcp_config: dict) -> None:
    vscode_dir = target / ".vscode"
    vscode_dir.mkdir(parents=True, exist_ok=True)
    mcp_path = vscode_dir / "mcp.json"
    if mcp_path.exists():
        try:
            data = json.loads(mcp_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            click.echo("  Error: .vscode/mcp.json is not valid JSON; skipping.")
            return
    else:
        data = {}
    servers = data.setdefault("servers", {})
    servers["clasi"] = mcp_config
    mcp_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    click.echo("  Wrote: .vscode/mcp.json")

def _uninstall_vscode_mcp(target: Path) -> None:
    mcp_path = target / ".vscode" / "mcp.json"
    if not mcp_path.exists():
        return
    try:
        data = json.loads(mcp_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        click.echo("  Error: .vscode/mcp.json is not valid JSON; skipping.")
        return
    servers = data.get("servers", {})
    if "clasi" in servers:
        del servers["clasi"]
        mcp_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        click.echo("  Removed clasi from .vscode/mcp.json")
```

### Files to Modify

- `clasi/platforms/copilot.py` — implement `_install_vscode_mcp`, `_uninstall_vscode_mcp`.
- `tests/unit/test_platform_copilot.py` — add vscode mcp tests.

### Testing Plan

Use `tmp_path`. Write a pre-existing `.vscode/mcp.json` with a user key. After install,
parse JSON and assert user key present + clasi key present. Write a corrupt JSON file;
assert it is unchanged after install. After uninstall, parse and assert clasi key absent
and user key present.

### Documentation Updates

None at this stage.
