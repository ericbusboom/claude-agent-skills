---
id: '002'
title: Update sprint-planner agent documents for extend mode
status: todo
use-cases:
  - SUC-031-02
  - SUC-031-03
depends-on:
  - '001'
github-issue: ''
todo: ''
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Update sprint-planner agent documents for extend mode

## Description

Update the four sprint-planner documents to reflect the new `extend` mode and
the simplified signature. These changes make the sprint-planner's contract
explicit and give it the workflow instructions it needs to handle extend-mode
dispatches.

Files to update:

| File | Change |
|------|--------|
| `clasi/agents/domain-controllers/sprint-planner/agent.md` | Add extend mode workflow: read existing sprint plan/tickets, dispatch to technical-lead for new tickets only |
| `clasi/agents/domain-controllers/sprint-planner/plan-sprint.md` | Add extend mode section (abbreviated flow: no architect, no reviewer, no stakeholder gate). Update detail-mode step 1 to handle both sprint-id-provided and sprint-created-by-tool cases. |
| `clasi/agents/domain-controllers/sprint-planner/dispatch-template.md.j2` | Add template branch for extend mode (provides existing sprint context). Update detail/roadmap branch to omit `sprint_directory` from rendered output. |
| `clasi/agents/domain-controllers/sprint-planner/contract.yaml` | Add extend mode inputs (`sprint_id` required, `todo_ids`, `goals`) and outputs (`{status, summary, ticket_ids, files_created}`). Add `sprint_id` and `sprint_directory` as required fields to detail-mode output schema. |

## Acceptance Criteria

- [ ] `agent.md` documents the extend mode workflow: read existing plan/tickets, dispatch to technical-lead
- [ ] `plan-sprint.md` has an extend mode section with the abbreviated flow (no architecture review, no stakeholder approval)
- [ ] `plan-sprint.md` detail-mode step 1 handles both "sprint_id provided" and "sprint created by dispatch tool" cases
- [ ] `dispatch-template.md.j2` has a template branch for `mode="extend"` that provides existing sprint context
- [ ] `contract.yaml` includes extend mode inputs and outputs
- [ ] `contract.yaml` detail-mode output schema includes `sprint_id` and `sprint_directory`
- [ ] No reference to `sprint_directory` remains as a dispatch *input* in any of these files (it is now derived internally)

## Implementation Notes

- The extend mode contract output `{status, summary, ticket_ids, files_created}`
  matches the technical-lead's existing return format — reuse that schema.
- The dispatch-template extend branch should include: existing sprint summary,
  list of current tickets (with IDs/titles), and the new TODO(s) to be added.
- `goals` in extend mode is "description of the work being added" — a brief
  statement about the new TODO(s), not a restatement of original sprint goals.

## Testing

- **Existing tests to run**: `uv run pytest tests/unit/test_dispatch_tools.py tests/unit/test_mcp_server.py`
- **New tests to write**: Contract YAML validation tests in ticket 004
- **Verification command**: `uv run pytest`
