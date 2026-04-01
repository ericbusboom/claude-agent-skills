---
id: "004"
title: Init command implementation
status: done
use-cases: [SUC-001]
depends-on: ["003"]
---

# Init Command Implementation

Implement `claude_agent_skills/init_command.py` — the `clasi init` command
that writes instruction files and configures the MCP server.

## Description

`clasi init` prepares a target repository for the CLASI SE process by:
1. Writing a single instruction file (`clasi-se-process.md`) to both
   `.claude/rules/` and `.github/copilot/instructions/`.
2. Adding the MCP server configuration to `.claude/settings.json`.
3. Optionally adding to global config with `--global`.

The instruction file content is a stable overview of the SE process with
a table mapping activities to MCP tool names.

## Acceptance Criteria

- [ ] `clasi init` creates `.claude/rules/clasi-se-process.md`
- [ ] `clasi init` creates `.github/copilot/instructions/clasi-se-process.md`
- [ ] Instruction file contains SE process overview and MCP tool reference
- [ ] `clasi init` adds MCP server config to `.claude/settings.json`
      (creates file if needed, merges into existing if present)
- [ ] `--global` flag also adds config to `~/.claude/settings.json`
- [ ] Re-running is idempotent (doesn't duplicate entries)
- [ ] `clasi init /some/path` works with a target directory argument
- [ ] Instruction file content is embedded in the Python module (not read
      from external files)
