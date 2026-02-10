---
name: system-engineering
description: Instructions for the system engineering process using brief, use cases, technical plan, tickets, and ticket plans
---

# System Engineering Process

This project follows a structured systems engineering workflow. All planning
artifacts live in `docs/plans/`.

## Agents

Two specialized agents drive this process:

- **requirements-analyst** — Takes stakeholder narratives and produces the
  brief, use cases, and technical plan. Knows how to ask about stakeholders,
  components, requirements, and success criteria.
- **systems-engineer** — Takes the completed documents and breaks them into
  sequenced, numbered tickets. Creates ticket plans before implementation
  begins.

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
id: "NNN"
title: Short title
status: todo | in-progress | done
use-cases: [UC-001, UC-002]
depends-on: []
---
```

Followed by: description, acceptance criteria (checkboxes), and
implementation notes.

### 5. Ticket Plans (`docs/plans/tickets/NNN-slug-plan.md`)

Before starting work on a ticket, create a plan file with the same number
and slug, ending in `-plan`. For example, ticket `003-add-auth.md` gets a
plan file `003-add-auth-plan.md`.

Every ticket plan must include:
1. **Approach** — How the work will be done, key decisions.
2. **Files to create or modify** — What will be touched.
3. **Testing plan** — What tests will be written, what type (unit, system,
   dev), what verification strategy.
4. **Documentation updates** — What docs need updating when the ticket is
   complete.

A ticket plan without a testing section and a documentation section is
incomplete.

## Workflow

### Phase 1: Requirements (requirements-analyst)

1. Take the stakeholder's narrative about the project.
2. Ask clarifying questions about stakeholders, components, requirements,
   constraints, and success criteria.
3. Write the brief.
4. Derive use cases from the brief.
5. Write the technical plan referencing the use cases.

### Phase 2: Ticketing (systems-engineer)

6. Break the technical plan into numbered tickets in dependency order.
7. Ensure every use case is covered by at least one ticket.
8. Ensure every ticket traces to at least one use case.

### Phase 3: Implementation (per ticket)

9. Pick the next `todo` ticket whose dependencies are all `done`.
10. Create the ticket plan (`NNN-slug-plan.md`).
11. Set the ticket status to `in-progress` in its YAML frontmatter.
12. Implement the ticket following its plan.
13. Write tests as specified in the plan.
14. Update documentation as specified in the plan.
15. Verify all acceptance criteria are met and check them off (`[x]`).
16. Complete the ticket (see **Completing a Ticket** below).

#### Completing a Ticket

When a ticket's work is finished and all acceptance criteria are met:

1. Set the ticket's `status` to `done` in its YAML frontmatter.
2. Check off all acceptance criteria (`- [x]`).
3. Move the ticket file to `docs/plans/tickets/done/`.
4. Move the ticket plan file to `docs/plans/tickets/done/`.

Active tickets live in `docs/plans/tickets/`. Completed tickets live in
`docs/plans/tickets/done/`. This separation makes it easy to see at a glance
what work remains (active directory) versus what has been finished (done
directory).

### Phase 4: Maintenance

18. If a change alters scope, update the brief and affected use cases first.
19. If new work is needed, create new tickets following the numbering
    sequence.

## Directory Layout

```
docs/plans/
├── brief.md
├── usecases.md
├── technical-plan.md
└── tickets/
    ├── 003-add-auth.md          # Active ticket
    ├── 003-add-auth-plan.md     # Its plan
    ├── 004-add-api.md           # Next ticket
    └── done/                    # Completed tickets and plans
        ├── 001-setup.md
        ├── 001-setup-plan.md
        ├── 002-data-model.md
        └── 002-data-model-plan.md
```

## Rules for AI Assistants

- When asked to plan work, produce or update these artifacts rather than
  jumping straight to code.
- When asked to implement, find the next unfinished ticket and work from it.
- Always create a ticket plan before starting implementation.
- No ticket is done without tests. See the testing instructions.
- When a ticket is completed, update its frontmatter status to `done`,
  check off all acceptance criteria, and move the ticket and its plan to
  `docs/plans/tickets/done/`. Do this immediately — do not batch completions.
- Do not create new artifacts without updating the existing ones to stay
  consistent.
- If a change alters scope, update the brief and affected use cases first.
