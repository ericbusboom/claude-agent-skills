---
name: elicit-requirements
description: Runs the requirements elicitation workflow to produce a project brief and use cases from a stakeholder narrative
---

# Elicit Requirements Skill

This skill runs the requirements elicitation workflow to produce a brief and
use cases from a stakeholder narrative.

## Agent Used

**requirements-analyst**

## Inputs

- A stakeholder narrative describing the project (provided by the user or
  project-manager)

## Process

1. **Accept narrative**: Take the initial project description or
   conversation about what the project should do.
2. **Ask clarifying questions**: Ask about stakeholders, problem,
   components, requirements, constraints, success criteria, and out of scope.
3. **Write brief**: Produce `docs/plans/brief.md` — a one-page project
   description covering problem, solution, users, constraints, success
   criteria, and out of scope.
4. **Derive use cases**: Produce `docs/plans/usecases.md` — enumerated use
   cases with ID, title, actor, preconditions, main flow, postconditions,
   and acceptance criteria.
5. **Verify traceability**: Every use case must trace back to something in
   the brief. Acceptance criteria must be testable.

## Output

- `docs/plans/brief.md` (created or updated)
- `docs/plans/usecases.md` (created or updated)
