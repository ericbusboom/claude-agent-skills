---
id: '004'
title: VSCode MCP configuration
status: done
use-cases:
- SUC-004
depends-on: []
---

# VSCode MCP configuration

## Description

Create `.vscode/mcp.json` with the CLASI MCP server configuration so
VSCode's Copilot agent mode can discover and use CLASI tools.

## Acceptance Criteria

- [ ] `.vscode/mcp.json` exists
- [ ] Config has `"type": "stdio"`, `"command": "clasi"`, `"args": ["mcp"]`
- [ ] `"inputs": []` is included

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: None (static config file)
- **Verification command**: `uv run pytest`
