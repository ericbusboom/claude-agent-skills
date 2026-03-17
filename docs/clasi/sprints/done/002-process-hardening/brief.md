---
status: draft
sprint: "002"
---

# Sprint 002 Brief

## Problem

The SE process defines a sprint lifecycle with review gates (architecture
review, stakeholder approval) but nothing enforces them. When an AI agent is
asked to plan a sprint, it generates all artifacts — planning documents and
tickets — in a single batch, skipping the gates entirely. This was demonstrated
in the original sprint 002 attempt, which had:

- No git branch created despite declaring one
- No architecture review performed
- No stakeholder approval before ticket creation
- Unresolved open questions in the technical plan
- All 10 tickets generated before any review

The root cause is that the process is expressed as narrative instructions with
no programmatic enforcement. The instructions say "wait for approval" but
nothing prevents the agent from continuing.

Additionally, there is no coordination mechanism for multiple simultaneous
sprints. Two sprints could be in progress (one planning, one executing) with
no way to communicate state between the AI sessions working on each.

## Solution

Add a SQLite database managed by the CLASI MCP server that tracks:

1. **Sprint lifecycle phase** — finer than `planning | active | done`. Phases
   include: `planning-docs`, `architecture-review`, `stakeholder-review`,
   `ticketing`, `executing`, `closing`, `done`.

2. **Review gate results** — explicit records of whether the architecture
   review and stakeholder approval have passed, with timestamps and notes.

3. **Execution locks** — only one sprint can be executing (committing code)
   at a time in a single repository.

The AI interacts with this database exclusively through MCP tools. The tools
enforce the lifecycle: you cannot create tickets until the review gates pass,
you cannot execute until you hold the lock.

Also add a Definition of Ready checklist to the sprint.md template and
explicit parent traceability from sprint use cases to top-level use cases.

## Success Criteria

- Sprint state database exists and is managed by the MCP server.
- MCP tools enforce phase transitions (cannot skip gates).
- `create_ticket` refuses to create tickets if the sprint has not passed
  stakeholder review.
- Execution lock prevents concurrent sprint execution.
- Sprint use cases have a `parent` field linking to top-level use cases.
- project-status tool reports use case coverage across sprints.
