---
id: '010'
title: Process Hygiene and Tooling
status: active
branch: sprint/010-process-hygiene-and-tooling
use-cases:
- UC-010
---

# Sprint 010: Process Hygiene and Tooling

## Goals

1. Add scold detection and self-reflection — when the stakeholder corrects
   the agent, capture structured feedback in a reflections directory.
2. Add auto-approve mode — allow stakeholders to skip `AskUserQuestion`
   breakpoints when they trust the agent to proceed autonomously.
3. Multi-ecosystem version detection — extend `tag_version` to detect and
   update version files beyond `pyproject.toml` (package.json, etc.).
4. VSCode MCP configuration — add `.vscode/mcp.json` so Copilot agent mode
   can discover CLASI tools.

## Problem

Four independent process and tooling gaps identified during sprints 008-009:

- **Scold detection**: Stakeholder corrections are valuable feedback but
  disappear when the session ends. No mechanism to capture learnings.
- **Auto-approve**: The new breakpoint system (sprint 009) adds overhead
  when the stakeholder trusts the agent. No way to skip breakpoints.
- **Version detection**: `tag_version` is hardcoded to `pyproject.toml`.
  When CLASI is used in Node/Rust/Go projects, versioning breaks.
- **VSCode MCP**: The MCP server config only exists for Claude Code, not
  for VSCode's native MCP server discovery.

## Solution

- Create a self-reflection skill and always-on CLAUDE.md instruction for
  scold detection.
- Add an auto-approve mode toggled by verbal instruction, checked at each
  `AskUserQuestion` breakpoint.
- Refactor `versioning.py` to detect version files by ecosystem and update
  the appropriate one.
- Create `.vscode/mcp.json` with the CLASI server configuration.

## Success Criteria

- Agent produces a reflection document when corrected.
- `docs/plans/reflections/` directory is used for output.
- Auto-approve mode can be activated verbally and skips breakpoints.
- `tag_version` works with `package.json` (at minimum) in addition to
  `pyproject.toml`.
- `.vscode/mcp.json` exists with correct CLASI server config.
- All existing tests still pass; new tests cover version detection.

## Scope

### In Scope

- Self-reflection skill (`claude_agent_skills/skills/self-reflect.md`)
- Scold detection instruction (`.claude/rules/scold-detection.md`)
- Auto-approve instruction (`.claude/rules/auto-approve.md`)
- `versioning.py` — multi-ecosystem version file detection
- `.vscode/mcp.json` — static config file
- Tests for version detection changes

### Out of Scope

- Ecosystem-aware version formatting (e.g., semver for npm) — future sprint
- Reflection analytics or dashboards
- Auto-approve as a persistent config file (session-scoped only for now)
- Cargo.toml / go.mod support (future, package.json only for now)

## Test Strategy

- Unit tests for new version detection logic (detect_version_file,
  update_version for each ecosystem)
- Existing versioning tests must continue to pass
- Content-only changes (skills, instructions, config) verified by
  `uv run pytest` for no regressions

## Architecture Notes

- Scold detection is an always-on instruction, not a skill gate. The
  self-reflection skill is invoked reactively, not at fixed process points.
- Auto-approve is session-scoped state. The agent checks a conversational
  flag before each `AskUserQuestion`. No file-based persistence for now.
- Version detection uses a priority-ordered list of known version files.
  Falls back to git-tag-only if no file is found.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, technical plan)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

- #001 Scold detection and self-reflection (SUC-001)
- #002 Auto-approve mode instruction (SUC-002)
- #003 Multi-ecosystem version detection (SUC-003)
- #004 VSCode MCP configuration (SUC-004)
