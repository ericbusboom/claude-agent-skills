---
id: "008"
title: "Remove Dormant Claude SDK and Align Active Agent Model"
status: planning
branch: sprint/008-remove-dormant-claude-sdk-and-align-active-agent-model
use-cases: ["SUC-001", "SUC-002", "SUC-003", "SUC-004", "SUC-005"]
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 008: Remove Dormant Claude SDK and Align Active Agent Model

## Goals

- Remove the dormant Claude Agent SDK dispatch path (`dispatch_tools.py`, `Agent.dispatch()`, SDK import) from CLASI entirely.
- Stop exposing `clasi/plugin/agents/old/*` as active agents via `Project.get_agent()`.
- Refresh active agent contracts, instructions, and docs that still reference the old agent roster (`project-manager`, `architect`, `technical-lead`, `sprint-executor`, `code-reviewer`, `code-monkey`, `ad-hoc-executor`).

## Scope

### In Scope

- Delete `clasi/tools/dispatch_tools.py` and remove its registration from `mcp_server.py`.
- Remove `Agent.dispatch()` and its SDK-specific methods (`_build_role_guard_hooks`, `_build_retry_prompt`) from `clasi/agent.py`; retain only content-loading/rendering behavior (`render_prompt`, `definition`, `contract`, etc.).
- Remove `claude-agent-sdk` from `pyproject.toml` dependencies once no runtime imports remain.
- Remove `Project.get_agent()` fallback into `clasi/plugin/agents/old/`.
- Update active agent instructions/contracts that reference old agent names.
- Remove stale `pyproject.toml` package-data globs for top-level paths (`agents/**`, `skills/*.md`, `instructions/*.md`, `rules/*.md`) that no longer exist under `clasi/`.
- Update `tests/unit/test_dispatch_tools.py` and `test_agent.py` to reflect removal.
- Add a guard test verifying normal CLASI runtime paths do not import `claude_agent_sdk`.
- Update README to remove Copilot mirroring and old agent layout references.

### Out of Scope

- Codex or alternative sub-agent dispatch mechanism (future TODO).
- Changes to `clasi/plugin/agents/old/` directory contents (keep as archival; just stop loading them as active).
- Changes to the MCP state machine, sprint lifecycle, or ticket model.

## TODO References

Source TODO: `docs/clasi/todo/remove-dormant-sdk.md`

## Sequencing Note

Sprint 008 runs first to remove dead surface area (Claude SDK dispatch, old agent fallback, stale docs) so that sprint 010 (Codex support) does not need to navigate around or preserve obsolete infrastructure. Sprint 009 (multi-sprint TODO bug fix) is a small, independent bug fix that can land in any order relative to 008 but is sequenced here between the cleanup (008) and the larger feature (010) for clean separability.

## Tickets

| # | Title | Depends On | Group |
|---|-------|------------|-------|
| 001 | Delete dispatch_tools.py and remove its MCP registration | — | 1 |
| 004 | Remove Project.get_agent() fallback into agents/old/ | — | 1 |
| 002 | Strip Agent.dispatch() and SDK methods from agent.py | 001 | 2 |
| 005 | Refresh active agent contracts and instructions to current 3-agent roster | 004 | 2 |
| 003 | Remove claude-agent-sdk dependency and stale package-data globs from pyproject.toml | 001, 002 | 3 |
| 007 | Update README to remove Copilot references and old agent architecture description | 005 | 3 |
| 006 | Update tests: remove SDK tests, add no-SDK import guard test | 001, 002, 003, 004 | 4 |

**Groups**: Tickets in the same group can execute in parallel.
Groups execute sequentially (1 before 2, etc.).
