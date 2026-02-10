---
id: "005"
title: MCP server skeleton
status: done
use-cases: [SUC-002]
depends-on: ["003"]
---

# MCP Server Skeleton

Create `claude_agent_skills/mcp_server.py` — the stdio MCP server that
registers tools and handles the MCP protocol.

## Description

Set up the MCP server using the `mcp` Python SDK. The server runs via
`clasi mcp` (stdio mode). This ticket creates the server infrastructure
and wires it to the CLI. Actual tools are added in subsequent tickets.

The server needs to locate the source repo (agents, skills, instructions)
using the package path, similar to the current `get_repo_root()`.

## Acceptance Criteria

- [ ] `claude_agent_skills/mcp_server.py` exists with an MCP server class
- [ ] Server uses stdio transport (standard MCP protocol)
- [ ] `clasi mcp` starts the server and responds to MCP protocol messages
- [ ] Server locates the source repo root (agents/, skills/, instructions/)
- [ ] Server has a registration mechanism for adding tools from other modules
- [ ] Server handles graceful shutdown
- [ ] A minimal smoke test verifies the server starts without errors
