---
sprint: "031"
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 031 Use Cases

## SUC-031-01: Create and Plan a New Sprint in One Dispatch

Parent: N/A (new capability)

- **Actor**: team-lead agent
- **Preconditions**: TODOs exist in `docs/clasi/todo/`. No sprint created yet.
- **Main Flow**:
  1. Team-lead calls `dispatch_to_sprint_planner(todo_ids=[...], goals="...",
     mode="detail", title="Sprint Title")` — no `sprint_id`, no
     `sprint_directory`.
  2. The dispatch tool creates the sprint internally via `create_sprint`,
     obtaining `sprint_id` and `sprint_directory`.
  3. The sprint planner receives the dispatch with the newly created
     `sprint_id` and proceeds with full detail planning.
  4. Sprint planner returns success with all planning artifacts.
- **Postconditions**: Sprint exists with `sprint.md`, `usecases.md`,
  `architecture-update.md`, and tickets — all created in a single dispatch
  without the team-lead needing to call `create_sprint` first.
- **Acceptance Criteria**:
  - [ ] `dispatch_to_sprint_planner` works without `sprint_id` when `title` is provided
  - [ ] Team-lead "Execute TODOs" workflow no longer includes `create_sprint` step
  - [ ] Team-lead "Sprint Planning Only" workflow no longer includes `create_sprint` step

## SUC-031-02: Extend an Executing Sprint with a New TODO

Parent: N/A (new capability)

- **Actor**: team-lead agent
- **Preconditions**: A sprint is currently executing (has execution lock,
  phase is `executing`). A new TODO needs to be added.
- **Main Flow**:
  1. Team-lead identifies the executing sprint via `list_sprints()` and
     `get_sprint_status()`.
  2. Team-lead calls `dispatch_to_sprint_planner(todo_ids=[<new_todo>],
     goals="Add TODO to sprint", mode="extend", sprint_id=<id>)`.
  3. The dispatch tool derives `sprint_directory` from `sprint_id`.
  4. The sprint planner receives the dispatch in extend mode.
  5. Sprint planner reads the existing sprint plan and tickets to understand
     the current structure.
  6. Sprint planner dispatches to the technical-lead to create new ticket(s)
     consistent with existing tickets.
  7. Sprint planner returns success with the new ticket file(s).
- **Postconditions**: New ticket(s) exist in the sprint's `tickets/`
  directory, numbered sequentially after existing tickets. No architecture
  review or stakeholder approval was triggered.
- **Acceptance Criteria**:
  - [ ] `mode="extend"` creates tickets without architecture review
  - [ ] `mode="extend"` requires `sprint_id` (errors without it)
  - [ ] Team-lead "Implement new TODO in existing sprint" uses `mode="extend"`

## SUC-031-03: Derive Sprint Directory from Sprint ID

Parent: N/A (simplification)

- **Actor**: `dispatch_to_sprint_planner` tool
- **Preconditions**: A sprint exists with a known `sprint_id`.
- **Main Flow**:
  1. Caller passes `sprint_id` to `dispatch_to_sprint_planner`.
  2. The tool calls `project.get_sprint(sprint_id)` to retrieve sprint
     metadata, including the directory path.
  3. The tool uses the derived directory for template rendering and agent dispatch.
- **Postconditions**: The correct sprint directory is used without the
  caller needing to know or pass it.
- **Acceptance Criteria**:
  - [ ] `sprint_directory` parameter removed from function signature
  - [ ] Directory derived correctly for all modes (roadmap, detail, extend)
  - [ ] All callers updated to omit `sprint_directory`
