---
id: "008"
title: Sprint template Definition of Ready
status: done
use-cases:
  - SUC-001
depends-on: []
---

# Sprint template Definition of Ready

## Description

Add a "Definition of Ready" checklist section to the `SPRINT_TEMPLATE` in
`claude_agent_skills/templates.py`. This checklist documents the prerequisites
that must be satisfied before a sprint can proceed to ticket creation. While the
actual enforcement comes from the state database (tickets 001-007), the
checklist makes the requirements visible in the sprint planning document itself.

### Template changes

Add the following section to `SPRINT_TEMPLATE` between the "Architecture Notes"
and "Tickets" sections:

```markdown
## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (brief, use cases, technical plan)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan
```

### Instruction updates

Update `instructions/system-engineering.md` to reference the Definition of Ready
concept. Add a brief explanation that sprints must pass through review gates
before ticket creation is allowed, and that the Definition of Ready checklist in
the sprint document tracks this. This ensures agents loading the system
engineering instructions understand the gating process.

## Acceptance Criteria

- [ ] `SPRINT_TEMPLATE` in `templates.py` includes a "Definition of Ready" section
- [ ] The section contains three checkboxes: planning docs complete, architecture review passed, stakeholder approved
- [ ] The section is placed between "Architecture Notes" and "Tickets"
- [ ] `instructions/system-engineering.md` references the Definition of Ready and explains the gating process
- [ ] Newly created sprints (via `create_sprint`) include the Definition of Ready section in their `sprint.md`
- [ ] Existing sprint documents are not affected (template change is forward-only)
