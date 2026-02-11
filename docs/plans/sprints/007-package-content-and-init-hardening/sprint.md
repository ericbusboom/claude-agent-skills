---
id: "007"
title: Package Content and Init Hardening
status: planning
branch: sprint/007-package-content-and-init-hardening
use-cases: [SUC-001, SUC-002, SUC-003]
---

# Sprint 007: Package Content and Init Hardening

## Goals

1. Fix the broken path resolution so CLASI works after pip/pipx install
2. Centralize all content path access through a single resolver function
3. Add MCP permission allowlist to `clasi init`
4. Add a smoke test that verifies MCP tools can actually read content

## Problem

When installed via pipx, `get_repo_root()` resolves to `site-packages/`
instead of the package directory, so the server can't find `agents/`,
`skills/`, or `instructions/`. Additionally, `clasi init` doesn't set up
MCP permissions, forcing users to approve every tool call.

## Solution

Move content directories (`agents/`, `skills/`, `instructions/`) inside the
`claude_agent_skills/` package. Replace `get_repo_root()` with a single
`content_path(relative)` function that resolves all content access. Add
MCP permission allowlist and smoke tests to `clasi init`.

## Success Criteria

- `uv run pytest` passes with content inside the package
- No code anywhere constructs a path to content files except through the
  resolver function
- `clasi init` creates `.claude/settings.local.json` with `mcp__clasi__*`
- Smoke test calls MCP tools and verifies they return real content

## Scope

### In Scope

- Move `agents/`, `skills/`, `instructions/` into `claude_agent_skills/`
- Update `pyproject.toml` package-data to include `*.md` files
- Replace `get_repo_root()` with `content_path()` resolver
- Update all 10 call sites in `process_tools.py`
- Update tests that reference `get_repo_root()`
- Add MCP permissions to `clasi init`
- Add smoke test for init + MCP content access

### Out of Scope

- Changing the MCP tool signatures or behavior
- Refactoring artifact_tools.py (it uses cwd, not content paths)

## Test Strategy

- Unit tests: verify `content_path()` resolves correctly
- System tests: verify MCP tools return content after the move
- Smoke test: verify `clasi init` + MCP tool calls work end-to-end

## Architecture Notes

- `content_path("agents/technical-lead.md")` → absolute Path
- No caller should ever construct `some_root / "agents"` directly
- Package data config ensures `*.md` files ship with the wheel

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
