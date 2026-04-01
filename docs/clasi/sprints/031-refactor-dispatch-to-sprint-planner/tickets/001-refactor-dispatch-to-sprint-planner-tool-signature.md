---
id: '001'
title: Refactor dispatch_to_sprint_planner tool signature
status: todo
use-cases:
  - SUC-031-01
  - SUC-031-02
  - SUC-031-03
depends-on: []
github-issue: ''
todo: refactor-dispatch-to-sprint-planner.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Refactor dispatch_to_sprint_planner tool signature

## Description

Refactor `dispatch_to_sprint_planner` in `clasi/tools/dispatch_tools.py` to:

1. **Remove `sprint_directory`** — derive it internally from `sprint_id` via
   `project.get_sprint()` (SUC-031-03).
2. **Make `sprint_id` optional** — when `None` in roadmap/detail mode, call
   `create_sprint(title=<title>)` internally to obtain `sprint_id` and
   `sprint_directory` (SUC-031-01).
3. **Add `title` parameter** — required when `sprint_id` is `None`; passed to
   the internal `create_sprint` call.
4. **Add formal `extend` mode** — when `mode="extend"`, `sprint_id` is required;
   the tool derives `sprint_directory`, then dispatches directly to the
   sprint-planner without architecture review or stakeholder approval (SUC-031-02).

New signature:

```python
async def dispatch_to_sprint_planner(
    todo_ids: list[str],
    goals: str,
    mode: str = "detail",        # "roadmap", "detail", or "extend"
    sprint_id: str | None = None, # required for "extend", optional otherwise
    title: str | None = None,     # required when sprint_id is None
) -> str:
```

The return value for detail/roadmap mode must include `sprint_id` and
`sprint_directory` in the result JSON (needed by team-lead for subsequent calls
to `acquire_execution_lock` and `dispatch_to_sprint_executor`).

The return value for extend mode is `{status, summary, ticket_ids, files_created}`.

## Acceptance Criteria

- [ ] `sprint_directory` is no longer a parameter on `dispatch_to_sprint_planner`
- [ ] `sprint_id` is optional (defaults to `None`)
- [ ] `title` parameter added
- [ ] When `sprint_id=None` and `title` is provided, sprint is created internally via `create_sprint`
- [ ] When `sprint_id=None` and `title` is `None`, the function raises a `ValueError`
- [ ] `mode="extend"` with a valid `sprint_id` dispatches to sprint-planner without triggering architecture review
- [ ] `mode="extend"` without `sprint_id` raises a `ValueError`
- [ ] `sprint_directory` is derived correctly from `sprint_id` via `project.get_sprint()` for all modes
- [ ] Detail/roadmap mode return JSON includes `sprint_id` and `sprint_directory`
- [ ] Extend mode return JSON is `{status, summary, ticket_ids, files_created}`
- [ ] `dispatch_to_sprint_planner` docstring updated to reflect new signature and modes

## Implementation Notes

- `project.get_sprint(sprint_id)` already returns sprint metadata including directory.
- The internal `create_sprint` call follows the same pattern used by team-lead today.
- The `_check_delegation_edge` guard remains — only `team-lead` may call this.
- The `mode` value is passed through to the sprint-planner dispatch template so
  the agent knows which workflow to follow.
- Sprint-planner documents (agent.md, plan-sprint.md, dispatch-template.md.j2,
  contract.yaml) are updated in ticket 002.

## Testing

- **Existing tests to run**: `tests/unit/test_dispatch_tools.py` (class `TestSprintPlannerModeParameter`, delegation edge tests)
- **New tests to write**: See ticket 004
- **Verification command**: `uv run pytest tests/unit/test_dispatch_tools.py`
