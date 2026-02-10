# clasi init command

## Summary

Add a `clasi init` subcommand that bootstraps the CLASI MCP integration for
a project. Running `clasi init` should:

1. Create (or update) `.mcp.json` at the project root with the clasi MCP
   server configuration
2. Prompt the user for confirmation before writing
3. Optionally create the `.claude/` rules directory with the SE process
   instructions

## Motivation

Currently, setting up the CLASI MCP server for Claude Code requires manually
running `claude mcp add --transport stdio --scope project clasi -- clasi mcp`
or hand-editing `.mcp.json`. A dedicated `clasi init` command makes onboarding
a single step:

```
pipx install clasi   # or: uv tool install clasi
clasi init
```

## Acceptance Criteria

- [ ] `clasi init` creates `.mcp.json` with the correct stdio configuration
- [ ] User is prompted before any files are written
- [ ] Existing `.mcp.json` is merged, not overwritten
- [ ] Command is idempotent (safe to run multiple times)
- [ ] Help text documents what the command does
