---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 031 Use Cases

## SUC-031-01: Team-lead dispatches sprint planning without pre-creating a sprint

- **Actor**: Team-lead agent
- **Preconditions**: TODOs exist; no sprint has been created yet
- **Main Flow**:
  1. Team-lead calls `dispatch_to_sprint_planner(todo_ids=[...],
     goals="...", mode="detail", title="Sprint title")` without
     providing `sprint_id` or `sprint_directory`.
  2. The dispatch tool internally calls `create_sprint(title=...)` to
     obtain `sprint_id` and `sprint_directory`.
  3. The dispatch tool renders the template and dispatches to the
     sprint-planner agent.
  4. Sprint-planner completes planning and returns result JSON
     containing `sprint_id` and `sprint_directory`.
  5. Team-lead uses the returned `sprint_id` for subsequent calls
     (`acquire_execution_lock`, `dispatch_to_sprint_executor`).
- **Postconditions**: Sprint exists with full planning artifacts;
  team-lead has `sprint_id` and `sprint_directory` from return JSON.
- **Acceptance Criteria**:
  - [ ] No `create_sprint` call needed before `dispatch_to_sprint_planner`
  - [ ] `sprint_id` and `sprint_directory` returned in result JSON
  - [ ] Calling without `title` when `sprint_id` is `None` raises `ValueError`

## SUC-031-02: Team-lead adds a TODO to an already-executing sprint

- **Actor**: Team-lead agent
- **Preconditions**: Sprint exists and is in `executing` phase; new
  TODO needs to be added to the sprint
- **Main Flow**:
  1. Team-lead calls `dispatch_to_sprint_planner(todo_ids=[new_todo],
     goals="description of new work", mode="extend",
     sprint_id="NNN")`.
  2. The dispatch tool derives `sprint_directory` from `sprint_id`.
  3. Sprint-planner reads existing sprint plan and tickets.
  4. Sprint-planner dispatches to technical-lead to create new
     ticket(s) consistent with the existing plan.
  5. Sprint-planner returns `{status, summary, ticket_ids,
     files_created}`.
  6. No architecture review or stakeholder approval is required.
- **Postconditions**: New ticket(s) added to the sprint's `tickets/`
  directory; existing tickets unchanged.
- **Acceptance Criteria**:
  - [ ] `mode="extend"` requires `sprint_id` (raises `ValueError` if `None`)
  - [ ] No architecture review or stakeholder approval triggered
  - [ ] New tickets are consistent with existing sprint scope
  - [ ] Return JSON includes new `ticket_ids`

## SUC-031-03: sprint_directory derived from sprint_id

- **Actor**: Any caller of `dispatch_to_sprint_planner`
- **Preconditions**: `sprint_id` is provided (or was just created
  internally)
- **Main Flow**:
  1. The dispatch tool calls `project.get_sprint(sprint_id)` to obtain
     sprint metadata including directory path.
  2. The directory path is used internally for template rendering and
     `cwd` in the dispatch call.
  3. The caller never provides `sprint_directory`.
- **Postconditions**: `sprint_directory` is correctly derived; no
  redundant parameter in the API.
- **Acceptance Criteria**:
  - [ ] `sprint_directory` is not a parameter on `dispatch_to_sprint_planner`
  - [ ] Directory is correctly derived via `project.get_sprint()`
  - [ ] Works for all three modes: roadmap, detail, extend
