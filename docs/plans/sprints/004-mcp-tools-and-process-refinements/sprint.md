---
id: "004"
title: MCP Tools and Process Refinements
status: planning
branch: sprint/004-mcp-tools-and-process-refinements
use-cases: [UC-004, UC-009]
---

# Sprint 004: MCP Tools and Process Refinements

## Problem

The MCP tool layer has gaps that force AI agents to fall back on direct
file operations: no TODO management tools, no frontmatter read/write, and
paths break when artifacts move to `done/`. The `clasi init` command writes
to the wrong config file. Coding standards contain Python-specific content
that belongs in language instructions. And there are no slash commands for
common actions.

## Solution

Fill the MCP tool gaps (frontmatter, TODO management, done/ path
resolution), fix `clasi init` to produce `.mcp.json`, dissolve the
coding-standards instruction into language-specific files, add a versioning
system, and implement slash commands for `/todo`, `/next`, and other common
actions.

## Success Criteria

- All TODO directory operations possible through MCP tools
- Frontmatter readable and writable through MCP tools
- Artifact paths resolve transparently whether in active or done/ location
- `clasi init` creates `.mcp.json` correctly
- `coding-standards.md` dissolved into `languages/python.md`
- Version numbers auto-managed during sprint closure
- Slash commands work for common SE process actions

## Test Strategy

- Unit tests for each new MCP tool function (frontmatter, TODO mgmt, path
  resolution, versioning)
- Unit tests for `clasi init` `.mcp.json` output
- System tests verifying path resolution across move-to-done operations
- Manual verification of slash commands in Claude Code

## Scope

### In Scope

1. Fix `clasi init` to write `.mcp.json` instead of `.claude/settings.json`
2. Add `list_todos` and `move_todo_to_done` MCP tools
3. Dissolve `coding-standards.md` into language-specific instructions
4. Add `read_frontmatter` and `write_frontmatter` MCP tools
5. Implement transparent `done/` path resolution for all file-accepting MCP tools
6. Add versioning system (`<major>.<isodate>.<build>`) with git tagging
7. Add slash commands (`/todo`, `/next`, `/status`, and others)

### Out of Scope

- New language instruction files beyond Python
- Changes to the sprint lifecycle phases
- Changes to the state database schema

## Architecture Notes

- Path resolution should be a single shared function used by all
  file-accepting MCP tools — not duplicated per tool.
- Slash commands are Claude Code skills (`.claude/skills/` files), not
  MCP tools. They invoke MCP tools internally.
- The `/next` slash command needs to read sprint phase state to determine
  what "next" means.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, technical plan)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
