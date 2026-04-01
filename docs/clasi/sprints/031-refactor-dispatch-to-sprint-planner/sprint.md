---
id: "031"
title: "Refactor dispatch_to_sprint_planner"
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

1. Simplify the `dispatch_to_sprint_planner` API by removing the
   redundant `sprint_directory` parameter and making `sprint_id` optional.
2. Add a `title` parameter for creating new sprints internally.
3. Add an `extend` mode that allows adding TODOs to an already-executing
   sprint without full architecture review.
4. Update all consuming agents and artifacts (team-lead, sprint-planner,
   dispatch template, contract) to reflect the new signature and modes.

## Problem

The current `dispatch_to_sprint_planner` signature has several issues:

- **Redundant parameter**: `sprint_directory` is always derivable from
  `sprint_id` via `project.get_sprint()`, yet callers must pass both.
- **Unnecessary pre-step**: The team-lead must call `create_sprint`
  before dispatching to the sprint planner, adding complexity to the
  "Execute TODOs" and "Sprint Planning Only" workflows.
- **No extend mode**: When a sprint is already executing and a new TODO
  needs to be added, there is no lightweight path — the team-lead uses
  an ad-hoc `mode="add_to_sprint"` that isn't formally defined in the
  contract or dispatch template.

## Solution

Refactor the dispatch tool signature:

```python
async def dispatch_to_sprint_planner(
    todo_ids: list[str],
    goals: str,
    mode: str = "detail",        # "roadmap", "detail", or "extend"
    sprint_id: str | None = None, # required for "extend", optional otherwise
    title: str | None = None,     # required when creating a new sprint
) -> str:
```

- Derive `sprint_directory` internally from `sprint_id`.
- When `sprint_id` is `None` in roadmap/detail mode, create the sprint
  internally (requires `title`).
- Add formal `extend` mode: creates new ticket(s) for added TODO(s),
  consistent with the existing plan. No architecture review or
  stakeholder approval needed.

Update all consuming documents:
- team-lead agent.md: remove `create_sprint` steps, use new signature
- sprint-planner agent.md: document extend mode workflow
- plan-sprint.md: add extend mode section
- dispatch-template.md.j2: add extend template branch
- contract.yaml: add extend mode inputs/outputs

## Success Criteria

- `dispatch_to_sprint_planner` accepts the new signature and correctly
  handles all three modes (roadmap, detail, extend).
- `sprint_directory` is no longer a parameter; it is derived internally.
- `sprint_id` is optional for roadmap/detail (sprint created internally).
- `title` is required when `sprint_id` is None.
- Extend mode creates tickets without architecture review.
- Team-lead agent.md no longer references `create_sprint` in "Execute
  TODOs" or "Sprint Planning Only" workflows.
- Team-lead "Implement new TODO in existing sprint" uses `mode="extend"`.
- All existing tests continue to pass with the updated signature.

## Scope

### In Scope

- Refactor `dispatch_to_sprint_planner` in `clasi/tools/dispatch_tools.py`
- Update `clasi/agents/main-controller/team-lead/agent.md`
- Update `clasi/agents/domain-controllers/sprint-planner/agent.md`
- Update `clasi/agents/domain-controllers/sprint-planner/plan-sprint.md`
- Update `clasi/agents/domain-controllers/sprint-planner/dispatch-template.md.j2`
- Update `clasi/agents/domain-controllers/sprint-planner/contract.yaml`
- Update any tests that call `dispatch_to_sprint_planner`

### Out of Scope

- Removing `sprint_directory` from other dispatch tools (e.g.,
  `dispatch_to_sprint_executor`, `dispatch_to_sprint_reviewer`). This
  is noted in the TODO as a stretch goal / separate TODO.
- Changes to the sprint state machine or lifecycle phases.

## Test Strategy

- **Unit tests**: Update existing tests for `dispatch_to_sprint_planner`
  to use the new signature. Add tests for:
  - `sprint_id=None` with `title` creates a new sprint
  - `sprint_id=None` without `title` raises an error
  - `mode="extend"` with `sprint_id` works correctly
  - `mode="extend"` without `sprint_id` raises an error
  - `sprint_directory` derivation from `sprint_id`
- **Contract validation**: Verify contract.yaml covers extend mode
  inputs/outputs.
- **Integration**: Run full test suite to catch regressions.

## Architecture Notes

- The key design change is moving sprint creation responsibility from
  the team-lead into the sprint-planner (via the dispatch tool).
- `sprint_directory` derivation uses `project.get_sprint()` which
  already exists and returns sprint metadata including the directory.
- The extend mode skips architecture review and stakeholder approval
  gates, going directly to ticket creation via the technical-lead.

## GitHub Issues

(None.)

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
