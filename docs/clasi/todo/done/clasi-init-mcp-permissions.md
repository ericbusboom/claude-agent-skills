---
status: pending
---
# Add MCP Permission Allowlist to clasi init

The `clasi init` command should set up `.claude/settings.local.json` in the
target repo so that all CLASI MCP tools are pre-approved and never prompt for
permissions.

Add something like this to the `permissions.allow` list:

```json
{
  "permissions": {
    "allow": [
      "mcp__clasi__*"
    ]
  }
}
```

This should be created (or merged into existing) by `run_init()` alongside
the other files it already sets up (`.mcp.json`, instruction rules, skill
stubs).
