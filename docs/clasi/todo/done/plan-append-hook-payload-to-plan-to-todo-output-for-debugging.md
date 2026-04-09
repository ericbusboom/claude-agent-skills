---
status: done
sprint: '005'
tickets:
- 005-001
---

# Plan: Append hook payload to plan-to-todo output for debugging

## Context

The `plan-to-todo` hook has a bug: it grabs the newest `.md` from
`~/.claude/plans/` regardless of which project or session created it.
Running it multiple times eats plans from other projects.

To fix this properly we need to know what data the PostToolUse hook
receives — the payload might contain the plan file path, session ID,
or project context that would let us target the correct file. But
`handle_plan_to_todo` currently ignores the payload entirely.

**This plan**: Append the raw hook payload JSON (and relevant env
vars) as a fenced block at the bottom of each TODO the hook creates.
This lets us inspect what data is available and design the real fix.

## Changes

### `clasi/hook_handlers.py` — `handle_plan_to_todo()`

Pass the payload dict through to `plan_to_todo()` so it can be
appended to the TODO content.

```python
def handle_plan_to_todo(payload: dict) -> None:
    from clasi.plan_to_todo import plan_to_todo

    result = plan_to_todo(
        Path.home() / ".claude" / "plans",
        Path("docs/clasi/todo"),
        hook_payload=payload,
    )
    ...
```

### `clasi/plan_to_todo.py` — `plan_to_todo()`

Add `hook_payload` parameter. Collect env vars of interest. Append
a debug section to the TODO content before writing.

```python
def plan_to_todo(
    plans_dir: Path,
    todo_dir: Path,
    hook_payload: Optional[dict] = None,
) -> Optional[Path]:
    ...
    # Build debug info
    import os
    debug_info = {
        "hook_payload": hook_payload or {},
        "env": {
            k: os.environ.get(k, "")
            for k in [
                "TOOL_INPUT", "TOOL_NAME", "SESSION_ID",
                "CLASI_AGENT_TIER", "CLASI_AGENT_NAME",
                "CLAUDE_PROJECT_DIR", "PWD", "CWD",
            ]
        },
        "plans_dir": str(plans_dir),
        "plan_file": str(plan_file),
        "cwd": os.getcwd(),
    }

    debug_block = (
        "\n\n---\n\n"
        "## Hook Debug Info\n\n"
        "```json\n"
        + json.dumps(debug_info, indent=2)
        + "\n```\n"
    )

    out_path.write_text(
        f"---\nstatus: pending\n---\n\n{body}\n{debug_block}",
        encoding="utf-8",
    )
    ...
```

### Files to modify

| File | Change |
|------|--------|
| `clasi/hook_handlers.py` | Pass `payload` to `plan_to_todo()` as `hook_payload` |
| `clasi/plan_to_todo.py` | Add `hook_payload` param, append debug JSON block |

### No test changes needed

This is a debugging aid. Existing tests still pass since the new
parameter is optional with a default of `None`.

## Verification

1. Enter plan mode, write a plan, exit plan mode
2. Check the created TODO file — it should have a `## Hook Debug Info`
   section at the bottom with the JSON payload and env vars
3. Inspect the JSON to understand what data is available
4. `uv run pytest` passes
