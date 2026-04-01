---
id: '031'
title: Refactor dispatch_to_sprint_planner
status: planning_docs
branch: sprint/031-refactor-dispatch-to-sprint-planner
use-cases:
  - SUC-031-01
  - SUC-031-02
  - SUC-031-03
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 031: Refactor dispatch_to_sprint_planner

## Goals

Simplify the `dispatch_to_sprint_planner` API by removing the redundant
`sprint_directory` parameter, making `sprint_id` optional (so the tool
can create sprints internally), and adding an "extend" mode that lets
the team-lead add TODOs to an already-executing sprint without full
planning ceremony.

## Problem

The current `dispatch_to_sprint_planner` signature requires both
`sprint_id` and `sprint_directory`, but `sprint_directory` is always
derivable from `sprint_id`. The team-lead must also call `create_sprint`
as a separate step before dispatching to sprint-planner, adding
unnecessary orchestration complexity. Additionally, there is no formal
mode for adding new work to an in-flight sprint -- the team-lead uses
an informal `mode="add_to_sprint"` that lacks contract definition,
template support, or documentation.

## Solution

1. Remove `sprint_directory` from the dispatch function signature and
   derive it internally from `sprint_id` via `project.get_sprint()`.
2. Make `sprint_id` optional -- when `None`, the tool creates the
   sprint internally (requires a `title` parameter).
3. Add a formal `"extend"` mode that dispatches to sprint-planner with
   an abbreviated workflow: read existing plan, dispatch to
   technical-lead for new tickets only, skip architecture review and
   stakeholder approval.
4. Update all sprint-planner agent documents (agent.md, plan-sprint.md,
   dispatch-template.md.j2, contract.yaml) and team-lead agent.md to
   reflect the new API.

## Success Criteria

- `dispatch_to_sprint_planner` no longer accepts `sprint_directory`
- Calling with `sprint_id=None, title="..."` creates a sprint internally
- Calling with `mode="extend", sprint_id="031"` adds tickets without
  full ceremony
- All existing tests pass; new tests cover the new signature and error
  paths
- Agent documentation and contracts are consistent with the new API

## Scope

### In Scope

- Refactor `dispatch_to_sprint_planner` signature and body in
  `clasi/tools/dispatch_tools.py`
- Update sprint-planner agent docs: `agent.md`, `plan-sprint.md`,
  `dispatch-template.md.j2`, `contract.yaml`
- Update team-lead `agent.md` workflows
- Update and add unit tests for the new signature

### Out of Scope

- Removing `sprint_directory` from other dispatch tools
  (`dispatch_to_sprint_executor`, `dispatch_to_sprint_reviewer`, etc.)
  -- deferred to a separate TODO
- Changes to the sprint lifecycle state machine or phase transitions
- Changes to the architect, architecture-reviewer, or technical-lead
  agents

## Test Strategy

- **Unit tests**: Update existing `test_dispatch_tools.py` tests for
  the new signature. Add `TestSprintPlannerNewSignature` class with
  `inspect.signature` checks and error-path tests.
- **Regression**: Full `uv run pytest` after each ticket to catch
  breakage from signature changes.
- **Manual verification**: Grep for removed references to
  `sprint_directory` in agent docs.

## Architecture Notes

- `project.get_sprint(sprint_id)` already returns sprint metadata
  including directory path -- reuse this.
- The `_check_delegation_edge` guard remains unchanged.
- Extend mode skips architecture review and stakeholder approval gates
  because the sprint's architecture is already approved.
- The dispatch template needs a new Jinja2 branch for extend mode.

## GitHub Issues

None.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan

## Tickets

| ID | Title | Depends On |
|----|-------|------------|
| 031-001 | Refactor dispatch_to_sprint_planner tool signature | -- |
| 031-002 | Update sprint-planner agent documents for extend mode | 001 |
| 031-003 | Update team-lead agent to remove create_sprint steps and use extend mode | 001, 002 |
| 031-004 | Update tests for new dispatch_to_sprint_planner signature | 001, 002, 003 |
