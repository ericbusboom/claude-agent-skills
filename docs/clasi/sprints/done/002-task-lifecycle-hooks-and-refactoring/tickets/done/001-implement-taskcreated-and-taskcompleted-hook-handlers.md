---
id: '001'
title: Implement TaskCreated and TaskCompleted hook handlers
status: done
use-cases: []
depends-on: []
github-issue: ''
todo: implement-task-lifecycle-hooks.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Implement TaskCreated and TaskCompleted hook handlers

## Description

Implements `_handle_task_created` and `_handle_task_completed` in `clasi/hook_handlers.py`
to log programmer task lifecycle, following the SubagentStart/SubagentStop pattern.
Also adds the TaskCreated hook entry to `.claude/settings.json`.

## Acceptance Criteria

- [x] `_handle_task_created` creates a log file in `docs/clasi/log/` with frontmatter (task_id, task_subject, teammate_name, started_at)
- [x] `_handle_task_created` writes an `.active/task-{id}.json` marker
- [x] `_handle_task_completed` finds the marker, appends duration to frontmatter, extracts prompt from transcript, appends transcript content
- [x] Both handlers exit 0 gracefully when `docs/clasi/log` does not exist
- [x] TaskCreated hook entry added to `.claude/settings.json`
- [x] All existing tests pass (787 total)

## Testing

- **Existing tests to run**: `uv run pytest --no-cov`
- **New tests to write**: `tests/unit/test_hook_handlers.py` — 11 tests covering both handlers
- **Verification command**: `uv run pytest --no-cov`
