---
status: pending
---

# Codex read-only filesystem error with MCP artifact tools

ChatGPT Codex runs in a sandboxed environment with a read-only
filesystem. When `create_sprint` (or any artifact-writing MCP tool)
tries to write to `/docs/plans/sprints/`, it fails with:

```
[Errno 30] Read-only file system: '/docs'
```

## Root Cause

The path resolves to `/docs` (not `<project>/docs`) because **Codex
runs MCP servers globally, not per-project**. Unlike Claude Code, which
starts the MCP server scoped to the current working directory, Codex
configures MCP servers at the top level and shares them across all
projects. There is a working-directory configuration for MCP servers in
Codex, but users set it globally rather than per-project.

This means `Path.cwd()` in `artifact_tools.py:_plans_dir()` resolves
to `/` instead of the project root, producing `/docs/plans/...` which
is read-only in the sandbox.

## Impact

- All artifact-writing MCP tools fail (`create_sprint`, `create_ticket`,
  `create_overview`, `update_ticket_status`, `move_ticket_to_done`,
  `close_sprint`, etc.)
- Read-only tools (`get_skill_definition`, `get_se_overview`,
  `list_agents`, etc.) still work because they read from the installed
  package, not from `cwd`

## Possible Approaches

- Detect read-only filesystem and return a helpful error message
- Accept an optional `project_root` parameter on artifact-writing tools
- Allow configuring a project root via environment variable
- Document that Codex's sandbox doesn't support artifact creation
  and recommend using Claude Code or another per-project MCP host
- Investigate whether Codex allows writing to specific directories
  (e.g., `/tmp` or a workspace mount)
