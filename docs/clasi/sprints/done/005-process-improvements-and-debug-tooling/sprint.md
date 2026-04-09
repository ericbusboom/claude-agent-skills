---
id: '005'
title: Process Improvements and Debug Tooling
status: done
branch: sprint/005-process-improvements-and-debug-tooling
use-cases:
- SUC-001
- SUC-002
- SUC-003
todos:
- plan-append-hook-payload-to-plan-to-todo-output-for-debugging.md
- plan-link-planning-to-todos-se-plan-command-and-instruction-updates.md
- plan-rebase-sprint-branch-before-merge-on-close.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 005: Process Improvements and Debug Tooling

## Goals

1. Surface hook payload data in TODO files to enable debugging the `plan-to-todo` file-targeting bug.
2. Make the two idea-capture paths (quick `/se todo` vs. discussed `/se plan`) explicit and discoverable.
3. Produce clean, linear git history on sprint close by rebasing the sprint branch before the `--no-ff` merge.

## Problem

Three small but real friction points accumulated after Sprint 004:

- The `plan-to-todo` hook picks the newest plan file from `~/.claude/plans/` without any project context, so it can steal plans from other projects. Before fixing this properly we need to see what data the hook payload actually contains.
- There is no explicit `/se plan` command and no guidance anywhere on when to use plan mode vs. the `todo` skill. The connection between ExitPlanMode and the TODO system is invisible to both the model and the developer.
- Sprint branches can diverge from master during planning (OOP fixes, version bumps). Closing the sprint produces a merge bubble whose commits are not rebased, cluttering git history.

## Solution

Three independent changes, all small and self-contained:

1. **Hook payload debug** — pass the PostToolUse hook payload through `handle_plan_to_todo` into `plan_to_todo()` and append it as a fenced `## Hook Debug Info` JSON block at the bottom of the created TODO file.
2. **`/se plan` command and instruction updates** — add `/se plan` to the SE skill table, add "when to use" guidance to the `todo` skill, and add a "Capture Ideas and Plans" scenario to the team-lead agent instructions. Mirror all changes to the live `.claude/` counterparts.
3. **Rebase before merge** — insert a `git rebase main_branch branch_name` step before the `--no-ff` merge in `Sprint.merge_branch()`, with abort-on-failure handling and an updated `merge_strategy` report string.

## Success Criteria

- After exiting plan mode, the created TODO file contains a `## Hook Debug Info` section with the raw payload JSON.
- `/se` (no args) shows a `/se plan` row. Invoking `/se plan` enters plan mode.
- `git log --oneline --graph` after sprint close shows sprint commits sitting linearly on top of master inside the merge bubble.
- `uv run pytest` passes for all three changes.

## Scope

### In Scope

- `clasi/hook_handlers.py` — pass payload to `plan_to_todo()`
- `clasi/plan_to_todo.py` — add `hook_payload` param, append debug block
- `clasi/plugin/skills/se/SKILL.md` — add `/se plan` row and guidance
- `clasi/plugin/skills/todo/SKILL.md` — add "when to use" note
- `clasi/plugin/agents/team-lead/agent.md` — add "Capture Ideas and Plans" scenario
- `.claude/skills/se/SKILL.md`, `.claude/skills/todo/SKILL.md`, `.claude/agents/team-lead/agent.md` — live copies updated
- `clasi/sprint.py` `merge_branch()` — rebase step before merge
- `clasi/tools/artifact_tools.py` — update `merge_strategy` string
- `tests/unit/test_sprint.py` — rebase tests

### Out of Scope

- The actual fix for the plan-file-targeting bug (deferred until we have payload data to inform the solution)
- Any changes to the MCP server, state DB, or sprint lifecycle tools
- UI or CLI changes beyond skill/agent markdown files

## Test Strategy

- TODO 1: no new tests needed (optional parameter, existing tests still pass)
- TODO 2: no tests needed (markdown only); manual verification via `/se` invocation
- TODO 3: new unit test in `test_sprint.py` simulating master advancing after branch point, verifying rebase occurred before merge

## Architecture Notes

All three changes are narrow augmentations to existing modules. No new modules, no new dependencies, no interface changes visible to callers. The `hook_payload` parameter on `plan_to_todo()` is optional with `None` default so all existing call sites remain valid. The rebase step is inserted before the checkout in `merge_branch()` and aborts cleanly if the rebase fails.

## GitHub Issues

None.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [x] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

| # | Title | Depends On | Group |
|---|-------|------------|-------|
| 001 | Hook Payload Debug in plan-to-todo | — | 1 |
| 002 | /se plan Command and Instruction Updates | — | 1 |
| 003 | Rebase Sprint Branch Before Merge on Close | — | 1 |

**Groups**: Tickets in the same group can execute in parallel.
Groups execute sequentially (1 before 2, etc.).
