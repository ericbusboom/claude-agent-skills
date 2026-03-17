---
id: '001'
title: Replace symlinks with MCP server
status: done
branch: sprint/001-mcp-server
use-cases:
- UC-001
- UC-003
- UC-004
- UC-010
---

# Sprint 001: Replace Symlinks with MCP Server

## Goals

Replace the symlink-based distribution of agents, skills, and instructions
with an MCP (Model Context Protocol) server. Instead of symlinking files
into every repo, the SE process content is served on-demand via MCP tools.
A lightweight `clasi init` command writes minimal instructions into the
target repo and configures the MCP server.

## Scope

### In Scope

1. **Rename CLI** from `link-claude-agents` to `clasi` (Claude Agent Skills
   Instructions).

2. **`clasi init` command**: Initialize a target repo:
   - Write instruction files into `.claude/rules/` and
     `.github/copilot/instructions/` that give an overview of the SE process
     and direct the LLM to MCP tools for each activity.
   - Configure the MCP server in `.claude/settings.json` (local workspace).
   - `--global` flag to also add to global Claude config.
   - Idempotent: safe to re-run; doesn't overwrite if already configured.
   - Instructions are stable — the MCP server content can evolve without
     re-running init.

3. **`clasi mcp` command**: Run a single stdio MCP server with two tool
   groups:

   **SE Process Access tools** — serve the SE process content:
   - Get SE process overview
   - Get a specific agent definition by name
   - Get a specific skill definition by name
   - Get a specific instruction by name
   - List all agents / skills / instructions
   - Get activity-specific guidance that combines relevant agents, skills,
     and instructions into a single curated response (requirements,
     architecture, ticketing, implementation, testing, code-review,
     sprint-planning, sprint-closing)

   **Artifact Management tools** — CRUD for SE artifacts:
   - Create sprint (assigns number, creates directory with template files,
     returns path and template content)
   - Create ticket within a sprint (assigns number, creates file with
     template, returns path)
   - Create top-level brief / technical plan / use cases (with templates)
   - List sprints (filterable by status)
   - List tickets (filterable by sprint and status)
   - Get sprint/ticket status summary
   - Update artifact frontmatter (status changes)
   - Move ticket to done
   - Close sprint (move to done/)

4. **Sprint directory structure**: Each sprint is a directory:
   ```
   docs/plans/sprints/NNN-slug/
   ├── sprint.md
   ├── brief.md
   ├── usecases.md
   ├── technical-plan.md
   └── tickets/
       ├── 001-some-ticket.md
       ├── 001-some-ticket-plan.md
       └── done/
   ```

5. **Remove symlink functionality**: The old `link-claude-agents` /
   `link_agents.py` code is replaced. No more directory or file symlinks.

6. **Migrate old tickets to sprint 000**: Move `docs/plans/tickets/done/`
   (tickets 001-034) into a retroactive `docs/plans/sprints/done/000-initial-setup/`
   to unify everything under the sprint-directory model.

### Out of Scope

- Remote/network MCP server (stdio only for now)
- Authentication or multi-user support
- CI/CD integration
- Migration tooling for repos already using symlinks (manual re-init)

## Architecture Notes

- MCP server implemented in Python using the `mcp` SDK
- Server reads agent/skill/instruction files from the installed package
  path (same approach as current `get_repo_root()`)
- Artifact management tools operate on `docs/plans/` relative to cwd
- Templates for artifacts are embedded in the Python package
- Frontmatter parsing/editing via `pyyaml` or a lightweight YAML parser
- The instruction files written by `init` are small and stable — they
  describe the SE process at a high level and list the MCP tools to use
  for each activity, so the MCP server content can change without re-running
  init

## Tickets

| ID  | Title | Depends On |
|-----|-------|-----------|
| 001 | Frontmatter parser module | — |
| 002 | Templates module | — |
| 003 | Restructure CLI and pyproject.toml | — |
| 004 | Init command implementation | 003 |
| 005 | MCP server skeleton | 003 |
| 006 | SE Process Access tools | 005 |
| 007 | Activity guide tool | 006 |
| 008 | Artifact Management tools — create | 001, 002, 005 |
| 009 | Artifact Management tools — query and status | 001, 005 |
| 010 | Artifact Management tools — update and close | 001, 005 |
| 011 | Migrate old tickets to sprint 000 | — |
| 012 | Remove symlink code | 003 |
| 013 | Update SE instructions for sprint-as-directory | — |

Independent starting points: 001, 002, 003, 011, 013

Critical path: 003 → 005 → 006 → 007
