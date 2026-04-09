---
id: '001'
title: Hook Payload Debug in plan-to-todo
status: done
use-cases:
- SUC-001
depends-on: []
github-issue: ''
todo: plan-append-hook-payload-to-plan-to-todo-output-for-debugging.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Hook Payload Debug in plan-to-todo

## Description

The `plan-to-todo` hook has a latent bug: it picks the newest `.md` file from
`~/.claude/plans/` without any project context, so it can consume plan files from
other projects. Before fixing this, we need to know what data the PostToolUse hook
payload actually contains — session ID, project directory, or other fields that could
identify the correct file.

This ticket threads the raw payload from `handle_plan_to_todo()` into `plan_to_todo()`
and appends it as a `## Hook Debug Info` fenced JSON block at the bottom of each TODO
file the hook creates. Two files, one optional parameter, no test changes needed.

## Acceptance Criteria

- [ ] `handle_plan_to_todo(payload)` passes `hook_payload=payload` to `plan_to_todo()`
- [ ] `plan_to_todo()` accepts `hook_payload: Optional[dict] = None` as a third parameter
- [ ] When `hook_payload` is not None, a `## Hook Debug Info` fenced JSON block is appended to the TODO file after the plan body
- [ ] The JSON block includes: `hook_payload`, `env` snapshot (`TOOL_INPUT`, `TOOL_NAME`, `SESSION_ID`, `CLASI_AGENT_TIER`, `CLASI_AGENT_NAME`, `CLAUDE_PROJECT_DIR`, `PWD`, `CWD`), `plans_dir`, `plan_file`, `cwd`
- [ ] When `hook_payload` is None (default), TODO file content is identical to current behavior
- [ ] `uv run pytest` passes with no new failures

## Implementation Plan

### Approach

Add `hook_payload: Optional[dict] = None` to `plan_to_todo()`. Build a debug dict
before writing the output file and append it as a formatted fenced block. Add
`hook_payload=payload` to the call in `handle_plan_to_todo()`. Both changes are
contained within their respective files.

### Files to Modify

**`clasi/plan_to_todo.py`**

- Add `import json` and `import os` at module top if not already present
- Change function signature to include `hook_payload: Optional[dict] = None`
- Add `from typing import Optional` if not already imported
- Before the `out_path.write_text(...)` call, build `debug_block`:
  - If `hook_payload is None`, `debug_block = ""`
  - Otherwise build a dict with `hook_payload`, `env` (os.environ.get for the listed keys), `plans_dir`, `plan_file`, `cwd`
  - Serialize with `json.dumps(debug_info, indent=2)` and wrap in `"\n\n---\n\n## Hook Debug Info\n\n```json\n...\n```\n"`
- Append `debug_block` to the content written by `out_path.write_text(...)`

**`clasi/hook_handlers.py`**

- In `handle_plan_to_todo(payload: dict)`, add `hook_payload=payload` as a keyword argument to the `plan_to_todo()` call

### Testing Plan

No new tests required. The new parameter is optional and defaults to `None`, so all
existing `plan_to_todo()` tests pass unchanged and exercise the unchanged code path.

Manual verification after implementation:
1. Enter plan mode, write a brief plan, exit plan mode
2. Open the created TODO file and confirm a `## Hook Debug Info` section is present at the bottom
3. Inspect the JSON to see which payload fields (if any) identify the project or session

### Documentation Updates

None needed. The debug block is self-explanatory within the TODO file.
