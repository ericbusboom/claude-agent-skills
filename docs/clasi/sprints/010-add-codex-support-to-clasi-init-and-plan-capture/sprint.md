---
id: "010"
title: "Add Codex Support to CLASI Init and Plan Capture"
status: active
branch: sprint/010-add-codex-support-to-clasi-init-and-plan-capture
use-cases:
  - SUC-001
  - SUC-002
  - SUC-003
  - SUC-004
  - SUC-005
  - SUC-006
  - SUC-007
  - SUC-008
  - SUC-009
  - SUC-010
  - SUC-011
  - SUC-012
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 010: Add Codex Support to CLASI Init and Plan Capture

## Goals

- Extend `clasi init` with opt-in `--codex` (and `--claude`) flags that install Codex-oriented project files alongside (or instead of) the existing Claude setup.
- Add a `clasi hook codex-plan-to-todo` Stop hook that captures `<proposed_plan>` output from Codex sessions and writes a pending TODO, mirroring the existing `ExitPlanMode` plan-to-todo behavior for Claude.
- Add `clasi uninstall` with platform selection (`--claude`, `--codex`, or both) that removes only CLASI-managed files/sections.

## Scope

### In Scope

- New CLI flags: `clasi init --claude`, `clasi init --codex`, `clasi init --claude --codex`.
- Platform detection (advisory only) and interactive prompt when no flag is supplied.
- Codex init outputs: `AGENTS.md` (CLASI section), `.codex/config.toml`, `.codex/hooks.json`, `.agents/skills/se/SKILL.md`.
- `clasi hook codex-plan-to-todo`: extract `<proposed_plan>`, write TODO, de-dupe by content hash.
- `clasi uninstall --claude`, `clasi uninstall --codex`, `clasi uninstall --claude --codex`.
- TOML read/write dependency (`tomli` + `tomli-w` for Python < 3.11).
- Tests for all new paths, idempotency, and backward compatibility.

### Out of Scope

- Alternative sub-agent dispatch backends (separate TODO if needed).
- Changes to the MCP state machine or sprint lifecycle.
- Anything in `docs/clasi/` planning artifacts (no sprint/ticket schema changes).

## TODO References

Source TODO: `docs/clasi/todo/add-codex-support-to-clasi-init-and-plan-capture.md`

## Sequencing Note

Sprint 010 is the largest sprint of the three and benefits from sprint 008 having removed the dormant SDK dispatch code first — init and hook logic is cleaner when there is no SDK entanglement to navigate around. Sprint 009 is independent and can land before or after 010 without conflict.

## Tickets

| # | Title | Depends On | Group |
|---|-------|------------|-------|
| 001 | Add tomli and tomli-w dependencies | — | 1 |
| 002 | Refactor init_command into clasi/platforms/claude.py | — | 1 |
| 003 | Add clasi/platforms/detect.py — advisory platform detection | — | 1 |
| 008 | Extend plan_to_todo.py with plan_to_todo_from_text and content hash dedup | — | 1 |
| 004 | Add clasi/platforms/codex.py — Codex installer and uninstaller | 001, 002 | 2 |
| 005 | Wire --claude / --codex flags and install synonym into cli.py and init_command | 002, 004 | 3 |
| 007 | Add clasi/uninstall_command.py and clasi uninstall CLI command | 002, 003, 004 | 3 |
| 009 | Add codex-plan-to-todo hook handler and wire into CLI | 008 | 3 |
| 006 | Add interactive platform prompt to clasi init | 003, 005 | 4 |

**Groups**: Tickets in the same group can execute in parallel.
Groups execute sequentially (1 before 2, etc.).

**Group 1** (parallel): 001, 002, 003, 008 — foundation work with no inter-dependencies.
**Group 2** (parallel): 004 — Codex installer, needs TOML deps (001) and platforms package (002).
**Group 3** (parallel): 005, 007, 009 — CLI wiring and hook; each depends on different group 1/2 outputs.
**Group 4**: 006 — interactive prompt; needs both detect (003) and flag wiring (005) in place.
