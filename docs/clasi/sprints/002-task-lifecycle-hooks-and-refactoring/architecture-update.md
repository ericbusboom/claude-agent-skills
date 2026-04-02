---
sprint: "002"
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Architecture Update -- Sprint 002: Task Lifecycle Hooks and Refactoring

## What Changed

- Implemented `_handle_task_created` and `_handle_task_completed` in `clasi/hook_handlers.py` to create and append log files in `docs/clasi/log/`.
- Registered `TaskCreated` hook in settings.json template and init_command.py.
- Added corresponding hook script `.claude/hooks/task_created.py`.

## Why

Programmer tasks had no logging. Sprint-planner activity was logged via SubagentStart/SubagentStop, but task lifecycle was invisible. Addresses TODO `implement-task-lifecycle-hooks.md`.

## Impact on Existing Components

No breaking changes. Adds new log files alongside existing subagent logs. The `_handle_task_completed` stub is replaced with real logic but maintains the same exit-0 behavior (permissive).

## Migration Concerns

Projects initialized before this sprint won't have the `TaskCreated` hook registered. Running `clasi init` again will add it. Existing projects can manually add it to `.claude/settings.json`.
