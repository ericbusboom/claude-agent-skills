---
status: done
sprint: '010'
consumed-by: sprint-010
---

# VSCode MCP Configuration

Install the CLASI MCP server configuration in `.vscode/mcp.json` so that
VSCode's Copilot agent mode can discover and use the CLASI MCP tools.

```json
{
	"servers": {
		"clasi": {
			"type": "stdio",
			"command": "clasi",
			"args": [
				"mcp"
			]
		}
	},
	"inputs": []
}
```

This parallels the existing `.claude/settings.local.json` MCP configuration
but targets VSCode's native MCP server discovery.
