---
id: "002"
title: Fix clasi init for mcp.json
status: todo
use-cases: [SUC-001]
depends-on: []
---

# Fix clasi init for mcp.json

## Description

Change `init_command.py` to write MCP server config to `.mcp.json` at the
project root instead of `.claude/settings.json`.

### Implementation

1. Change MCP config writing to produce `.mcp.json` at `target_path`.
2. Format: `{"mcpServers": {"clasi": {"command": "clasi", "args": ["mcp"]}}}`.
3. Keep merge behavior (read existing, add/update clasi entry, write back).
4. Remove `.claude/settings.json` MCP writing.
5. Remove `--global-config` flag (not applicable for `.mcp.json`).
6. Update tests.

## Acceptance Criteria

- [ ] `clasi init` creates `.mcp.json` at project root
- [ ] Existing `.mcp.json` content is preserved (merge, not overwrite)
- [ ] No longer writes to `.claude/settings.json` for MCP config
- [ ] Command is idempotent
- [ ] Unit tests updated
