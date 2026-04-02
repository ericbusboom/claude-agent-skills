---
id: "002"
title: "Task Lifecycle Hooks and Refactoring"
status: planning
branch: sprint/002-task-lifecycle-hooks-and-refactoring
use-cases: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 002: Task Lifecycle Hooks and Refactoring

## Goals

Implement TaskCreated and TaskCompleted hook handlers to log programmer task lifecycle, matching the existing SubagentStart/SubagentStop logging pattern.

## Problem

Programmer tasks produce no log output. SubagentStart/SubagentStop hooks log sprint-planner activity to `docs/clasi/log/`, but the TaskCreated/TaskCompleted handlers are stubs. No TaskCreated hook is registered in settings.json.

## Solution

1. Implement `_handle_task_created` to create a log file in `docs/clasi/log/` with task metadata.
2. Implement `_handle_task_completed` to append result/transcript to that log file.
3. Register `TaskCreated` hook in settings.json and init_command.py.

## Success Criteria

- TaskCreated creates a log file with task_id, task_subject, timestamp
- TaskCompleted appends result and transcript to the log file
- Both hooks registered in settings.json
- All existing tests pass, new tests cover the handlers

## Scope

### In Scope

- Task hook handler implementations in hook_handlers.py
- TaskCreated hook registration in settings.json and init_command.py
- Unit tests for the new handlers

### Out of Scope

- Validation logic (blocking tasks based on ticket state)
- Other TODOs (refactoring, path accessors, etc.)

## Test Strategy

Unit tests for _handle_task_created and _handle_task_completed verifying log file creation, content, and edge cases. Run full suite with `uv run pytest`.

## Architecture Notes

Task hook payloads include: task_id, task_subject, task_description, teammate_name, team_name, session_id, transcript_path, cwd, permission_mode, hook_event_name. Log files follow the same `NNN-type.md` pattern as subagent logs, using `.active/` markers to link created → completed.

## GitHub Issues

None.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
