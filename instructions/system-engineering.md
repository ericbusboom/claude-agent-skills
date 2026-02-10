---
name: system-engineering
description: Instructions for the system engineering process using brief, use cases, technical plan, and tickets
---

# System Engineering Process

This project follows a structured systems engineering workflow. All planning
artifacts live in `docs/plans/`.

## Artifacts

### 1. Brief (`docs/plans/brief.md`)

A one-page project description written first. Everything else derives from it.

Contents:
- Project name
- Problem statement (what problem, who has it)
- Proposed solution (high-level)
- Target users
- Key constraints (timeline, technology, budget)
- Success criteria (measurable outcomes)
- Out of scope

### 2. Use Cases (`docs/plans/usecases.md`)

Enumerated use cases derived from the brief. Each use case has:
- ID (UC-001, UC-002, ...)
- Title
- Actor
- Preconditions
- Main flow (numbered steps)
- Postconditions
- Acceptance criteria (checkboxes)

### 3. Technical Plan (`docs/plans/technical-plan.md`)

Architecture and design decisions. Must trace back to use cases.

Contents:
- Architecture overview
- Technology stack
- Component design (each component lists use cases it addresses)
- Data model
- API design
- Deployment strategy
- Security considerations
- Open questions

### 4. Tickets (`docs/plans/tickets/NNN-slug.md`)

Numbered implementation tickets broken out from the technical plan.

File naming: `001-setup-project-skeleton.md`, `002-add-auth-endpoints.md`, etc.

Each ticket has YAML frontmatter:
```yaml
---
id: "001"
title: Short title
status: todo | in-progress | done
use-cases: [UC-001, UC-002]
depends-on: []
---
```

Followed by: description, acceptance criteria (checkboxes), and implementation notes.

## Workflow

1. Draft the brief.
2. Derive use cases from the brief.
3. Write the technical plan referencing the use cases.
4. Break the technical plan into tickets.
5. Implement tickets in dependency order.
6. After each ticket, update the brief/plan if scope changed.

## Rules for AI Assistants

- When asked to plan work, produce or update these artifacts rather than
  jumping straight to code.
- When asked to implement, find the next unfinished ticket and work from it.
- When a ticket is completed, set its status to `done` in its frontmatter.
- Do not create new artifacts without updating the existing ones to stay
  consistent.
- If a change alters scope, update the brief and affected use cases first.
