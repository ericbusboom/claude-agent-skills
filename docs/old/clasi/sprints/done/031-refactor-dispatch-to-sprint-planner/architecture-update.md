---
sprint: '031'
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Architecture Update -- Sprint 031: Refactor dispatch_to_sprint_planner

## What Changed

### `clasi/tools/dispatch_tools.py`

- **`dispatch_to_sprint_planner` signature changed**: Removed
  `sprint_directory` parameter. Made `sprint_id` optional (default
  `None`). Added `title` parameter (default `None`). Added `"extend"`
  as a valid `mode` value.
- **Internal sprint creation**: When `sprint_id` is `None`, the
  function calls `create_sprint(title=title)` internally to obtain
  `sprint_id` and `sprint_directory`. Raises `ValueError` if `title`
  is also `None`.
- **Internal directory derivation**: When `sprint_id` is provided,
  calls `project.get_sprint(sprint_id)` to derive `sprint_directory`.
- **Extend mode validation**: `mode="extend"` requires `sprint_id`;
  raises `ValueError` if `None`.

### Sprint-planner agent documents

- **`agent.md`**: Added extend mode workflow section.
- **`plan-sprint.md`**: Added extend mode section (abbreviated flow:
  skip architect, reviewer, stakeholder gates; dispatch directly to
  technical-lead).
- **`dispatch-template.md.j2`**: Added `{% if mode == "extend" %}`
  template branch providing existing sprint context, current ticket
  list, and new TODO references. Removed `sprint_directory` as a
  template input variable.
- **`contract.yaml`**: Added extend mode inputs/outputs. Added
  `sprint_id` and `sprint_directory` to detail-mode return schema.

### Team-lead agent

- **`agent.md`**: Removed `create_sprint` pre-step from "Execute TODOs"
  and "Sprint Planning Only" workflows. Updated dispatch calls to new
  signature. "Implement new TODO in existing sprint" now uses formal
  `mode="extend"`.

## Why

The `sprint_directory` parameter was always derivable from `sprint_id`,
creating redundancy and requiring the team-lead to manage an extra
piece of state. The team-lead also had to call `create_sprint` as a
separate orchestration step before dispatching to sprint-planner,
which could be handled internally. The lack of a formal "extend" mode
meant adding work to in-flight sprints relied on undocumented behavior
without contract validation.

This refactoring simplifies the team-lead's orchestration logic,
reduces the API surface, and formalizes the extend workflow with proper
contract definition and template support.

## Impact on Existing Components

- **Team-lead agent**: Must update all `dispatch_to_sprint_planner`
  call sites to the new signature. This is a breaking change to the
  dispatch tool's API.
- **Sprint-planner agent**: Gains a new mode (`extend`) and no longer
  receives `sprint_directory` as a dispatch input -- it is available
  via the sprint context instead.
- **Other dispatch tools**: `dispatch_to_sprint_executor`,
  `dispatch_to_sprint_reviewer`, etc. still accept `sprint_directory`
  -- those are out of scope for this sprint.
- **Tests**: `test_dispatch_tools.py` must be updated for the new
  signature; existing parametrized tests will break until updated.

## Migration Concerns

- **Breaking change**: The `dispatch_to_sprint_planner` MCP tool
  signature changes. Any callers passing `sprint_directory` will fail.
  Since the only allowed caller is `team-lead` (enforced by delegation
  edge check), the migration scope is limited to the team-lead agent
  documentation.
- **No data migration**: No changes to SQLite schema, sprint
  lifecycle phases, or artifact formats.
- **Backward compatibility**: Not applicable -- the dispatch tools are
  internal to CLASI and not part of a public API.
