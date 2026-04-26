---
id: "009"
title: "Add codex-plan-to-todo hook handler and wire into CLI"
status: done
use-cases:
  - SUC-010
  - SUC-011
depends-on:
  - "008"
github-issue: ""
todo: ""
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Add codex-plan-to-todo hook handler and wire into CLI

## Description

Add `handle_codex_plan_to_todo` to `clasi/hook_handlers.py` and register it as
`"codex-plan-to-todo"` in the routing table. Add `"codex-plan-to-todo"` to the
`clasi hook` CLI choices.

The handler:
1. Reads `last_assistant_message` from the stdin JSON payload.
2. Extracts content between `<proposed_plan>` and `</proposed_plan>` tags.
3. If no plan found: exits 0 (no-op).
4. Calls `plan_to_todo_from_text(plan_text, todo_dir)` from ticket 008.
5. Always exits 0 (does not block — the Codex session has already ended).

This is the final integration point that makes the Codex plan-to-todo pipeline work
end-to-end. Depends on ticket 008.

## Acceptance Criteria

- [x] `clasi/hook_handlers.py` contains `handle_codex_plan_to_todo(payload: dict) -> None`.
- [x] `handle_codex_plan_to_todo` extracts `<proposed_plan>...</proposed_plan>` from
      `payload["last_assistant_message"]` using a regex.
- [x] If no `<proposed_plan>` is found: exits 0, no TODO created.
- [x] If a `<proposed_plan>` is found: calls `plan_to_todo_from_text` with the extracted
      text and `Path("docs/clasi/todo")`. If a TODO is created, prints the path.
- [x] `handle_codex_plan_to_todo` always exits 0 (never exits 2).
- [x] The routing table includes `"codex-plan-to-todo": handle_codex_plan_to_todo`.
- [x] `clasi/cli.py` `hook` command choices include `"codex-plan-to-todo"`.
- [x] Existing `handle_plan_to_todo` (Claude) behavior is unchanged.
- [x] Tests in `tests/unit/test_hook_handlers.py` (extended) cover:
  - No `<proposed_plan>` in message: exits 0, no file created.
  - `<proposed_plan>` present: one TODO file created, exits 0.
  - Duplicate plan (same hash): second call creates no file, exits 0.
  - Existing `plan-to-todo` handler tests still pass.

## Implementation Plan

### Files to modify

- `clasi/hook_handlers.py` — add handler and routing entry
- `clasi/cli.py` — add `"codex-plan-to-todo"` to `hook` choices
- `tests/unit/test_hook_handlers.py` — extend with new tests

### Approach

**Handler**:

```python
def handle_codex_plan_to_todo(payload: dict) -> None:
    import re
    from clasi.plan_to_todo import plan_to_todo_from_text

    message = payload.get("last_assistant_message", "")
    match = re.search(
        r"<proposed_plan>(.*?)</proposed_plan>", message, re.DOTALL
    )
    if not match:
        sys.exit(0)

    plan_text = match.group(1).strip()
    todo_dir = Path("docs/clasi/todo")
    result = plan_to_todo_from_text(plan_text, todo_dir)
    if result:
        print(f"CLASI: Codex plan saved as TODO: {result}")
    sys.exit(0)
```

**Routing table update** in `handle_hook()`:

```python
"codex-plan-to-todo": handle_codex_plan_to_todo,
```

**`cli.py` hook choices** — add `"codex-plan-to-todo"` to the `click.Choice([...])` list.

### Testing plan

In `tests/unit/test_hook_handlers.py`, add tests using `monkeypatch` for stdin and
`tmp_path` for the TODO directory:

- `test_codex_hook_no_plan`: payload with no `<proposed_plan>` → sys.exit(0), no file.
- `test_codex_hook_with_plan`: payload with `<proposed_plan>Plan text</proposed_plan>`
  → one TODO file created, sys.exit(0).
- `test_codex_hook_dedup`: call handler twice with same plan text → only one file created.
- `test_codex_hook_never_exits_2`: assert sys.exit arg is always 0.

```
uv run pytest tests/unit/test_hook_handlers.py tests/unit/test_plan_to_todo.py -v
uv run pytest -x
```

### Documentation updates

Update the `clasi hook` command docstring in `cli.py` to list `codex-plan-to-todo` as
a valid event. No external documentation required.
