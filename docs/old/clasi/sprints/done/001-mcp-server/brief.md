---
status: draft
---

# Sprint 001 Brief

## Problem

The current approach distributes SE process content (agents, skills,
instructions) via symlinks into target repos. This has several limitations:

1. **Fragile**: Symlinks break when the source package is reinstalled,
   moved, or the path changes between machines.
2. **All-or-nothing**: Every repo gets every file, regardless of what it
   needs.
3. **No query interface**: LLMs have to discover and read files themselves.
   There's no way to ask "what agents are available?" or "what should I do
   for requirements analysis?" without scanning the filesystem.
4. **No artifact management**: Creating sprints, tickets, and other SE
   artifacts is entirely manual. No templates, no numbering enforcement,
   no status queries.
5. **No structure enforcement**: Frontmatter formats, directory layouts,
   and naming conventions rely on agent discipline rather than tooling.

## Solution

Replace symlinks with an MCP server (`clasi mcp`) that serves SE process
content on demand and provides artifact management tools. A lightweight
`clasi init` command writes stable instruction files that direct LLMs to
the MCP server.

## Key Changes from Current System

| Aspect | Before (symlinks) | After (MCP) |
|--------|-------------------|-------------|
| Distribution | Symlink dirs/files into each repo | MCP server serves content on demand |
| Setup | `link-claude-agents` creates symlinks | `clasi init` writes instructions + configures MCP |
| Discovery | LLM reads files from known paths | LLM calls MCP tools (list, get, query) |
| Artifact creation | Manual file creation | MCP tools create files with templates |
| Status queries | LLM scans frontmatter manually | MCP tools return structured status data |
| CLI name | `link-claude-agents` | `clasi` |

## Success Criteria

- `clasi init` configures a repo in under 5 seconds with no symlinks.
- LLMs can discover and use SE process content via MCP tools.
- Creating a sprint/ticket via MCP returns the correct path and template.
- All artifact management operations (create, list, status, close) work.
- The old symlink code is removed from the package.
