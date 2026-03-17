---
id: "009"
title: Use case traceability
status: done
use-cases:
  - SUC-005
depends-on: []
---

# Use case traceability

## Description

Enable traceability between top-level project use cases (UC-NNN) and sprint-level
use cases (SUC-NNN) by adding a `Parent:` field to the sprint use case template
and providing a tool or enhancement to report coverage.

Currently, sprint use cases reference parent use cases informally. This ticket
formalizes the relationship so tooling can automatically determine which
top-level use cases are covered by completed sprints, which are in progress, and
which have not been addressed yet.

### Template changes

Update `SPRINT_USECASES_TEMPLATE` in `claude_agent_skills/templates.py` to
include a `Parent:` field in each use case section:

```markdown
## SUC-001: (Title)
Parent: UC-NNN

- **Actor**: (Who)
- **Preconditions**: (What must be true before)
...
```

The `Parent:` line appears immediately after the use case heading, before the
Actor field. It references the top-level use case ID that this sprint use case
implements or contributes to.

### Coverage reporting

Update the `project_status` tool in `process_tools.py` (or add a new
`get_use_case_coverage` tool) to:

1. Read top-level use cases from `docs/plans/usecases.md`.
2. Read each sprint's use cases from `docs/plans/sprints/*/usecases.md`.
3. Parse the `Parent:` field from each sprint use case.
4. Match sprint use cases to their parent top-level use cases.
5. Report coverage: which top-level use cases have been addressed by completed
   sprints, which are in active sprints, and which are unaddressed.

The output should be structured JSON that agents can use to advise stakeholders
on project progress.

## Acceptance Criteria

- [ ] `SPRINT_USECASES_TEMPLATE` in `templates.py` includes a `Parent: UC-NNN` field in the use case template
- [ ] The `Parent:` field appears after the section heading and before the Actor field
- [ ] Newly created sprints include the `Parent:` field in their `usecases.md`
- [ ] `project_status` or a new `get_use_case_coverage` tool reads top-level and sprint use cases
- [ ] The tool parses `Parent:` references from sprint use cases
- [ ] The tool reports which top-level use cases are covered (by done sprints), in-progress (by active sprints), or unaddressed
- [ ] Coverage report is returned as structured JSON
- [ ] Unit tests cover the parent parsing and coverage matching logic
