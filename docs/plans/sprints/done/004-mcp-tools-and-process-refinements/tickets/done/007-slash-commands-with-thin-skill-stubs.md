---
id: '007'
title: Slash commands with thin skill stubs
status: done
use-cases:
- SUC-007
depends-on:
- '002'
- '003'
---

# Slash commands with thin skill stubs

## Description

Create MCP-served skill definitions and thin Claude Code skill stubs.
Stubs installed by `clasi init` point to the MCP server for instructions.

### Skill definitions (package `skills/`)

- `skills/todo.md` — Create a TODO file from user input
- `skills/next.md` — Determine and execute the next process step
- `skills/status.md` — Run project-status report

### Skill stubs (`.claude/skills/`)

Each stub tells the AI to call `get_skill_definition` for real instructions.

### clasi init changes

Update `init_command.py` to install stubs alongside instruction files.

## Acceptance Criteria

- [ ] `skills/todo.md` exists with TODO creation instructions
- [ ] `skills/next.md` exists with next-step instructions
- [ ] `skills/status.md` exists with status reporting instructions
- [ ] `clasi init` installs stubs to `.claude/skills/`
- [ ] Stubs reference `get_skill_definition` for real instructions
- [ ] Installation is idempotent
- [ ] Unit tests for stub installation
