---
name: system-engineering
description: Instructions for the system engineering process using brief, use cases, technical plan, tickets, and ticket plans
---

# System Engineering Process

This project follows a structured systems engineering workflow. All planning
artifacts live in `docs/plans/`.

## Agents

Six specialized agents drive this process, orchestrated by the
project-manager:

- **project-manager** — Top-level orchestrator. Delegates to the other
  agents, tracks project state, and coordinates sprints and ticket execution.
  Does not implement code or write documents itself.
- **requirements-analyst** — Elicits requirements from stakeholder
  narratives. Produces the brief and use cases.
- **architect** — Designs system architecture. Takes the brief and use cases
  and produces the technical plan.
- **systems-engineer** — Breaks the technical plan into sequenced, numbered
  tickets. Creates ticket plans before implementation begins.
- **architecture-reviewer** — Reviews sprint plans against the existing
  codebase and technical plan. Produces architectural review verdicts.
- **code-reviewer** — Reviews code changes during ticket execution for
  quality, standards compliance, and security. Produces pass/fail verdicts.

Supporting agents used during implementation:
- **python-expert** — Implements Python code during ticket execution.
- **documentation-expert** — Updates documentation during ticket execution.

## Skills

Reusable workflows that correspond to each stage:

- **elicit-requirements** — Stage 1a: narrative → brief → use cases
- **create-technical-plan** — Stage 1b: brief + use cases → technical plan
- **create-tickets** — Stage 2: technical plan → numbered tickets
- **execute-ticket** — Stage 3: ticket → plan → implement → test → done
- **project-status** — Anytime: scan artifacts and report progress
- **plan-sprint** — Plan and set up a new sprint
- **close-sprint** — Validate and close a completed sprint

Supporting skills used during ticket execution:

- **python-code-review** — Code review against coding standards and security
- **generate-documentation** — Create or update project documentation

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

### 4. Sprints (`docs/plans/sprints/NNN-slug/`)

Each sprint is a **directory** containing its planning documents and tickets.
Ticket numbering is per-sprint (starts at 001 within each sprint).

Directory structure:
```
docs/plans/sprints/NNN-slug/
├── sprint.md              # Sprint goals, scope, architecture notes
├── brief.md               # Sprint-level brief
├── usecases.md            # Sprint-level use cases (SUC-NNN)
├── technical-plan.md      # Sprint-level technical plan
└── tickets/
    ├── 001-first-task.md  # Active ticket
    ├── 002-next-task.md   # Active ticket
    └── done/              # Completed tickets and plans
        └── ...
```

Sprint frontmatter (`sprint.md`):
```yaml
---
id: "NNN"
title: Sprint title
status: planning | active | done
branch: sprint/NNN-slug
use-cases: [UC-XXX, ...]
---
```

Active sprints live in `docs/plans/sprints/`. Completed sprints live in
`docs/plans/sprints/done/`.

### 5. Tickets (within sprint: `tickets/NNN-slug.md`)

Numbered implementation tickets broken out from the technical plan.
Tickets are numbered per-sprint starting at 001.

File naming: `001-setup-project-skeleton.md`, `002-add-auth-endpoints.md`, etc.

Each ticket has YAML frontmatter:
```yaml
---
id: "NNN"
title: Short title
status: todo | in-progress | done
use-cases: [SUC-001, SUC-002]
depends-on: ["NNN"]
---
```

Followed by: description, acceptance criteria (checkboxes), and
implementation notes.

### 6. Ticket Plans (`tickets/NNN-slug-plan.md`)

Before starting work on a ticket, create a plan file with the same number
and slug, ending in `-plan`. For example, ticket `003-add-auth.md` gets a
plan file `003-add-auth-plan.md`. The plan lives in the same `tickets/`
directory as the ticket.

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

### Stage 1a: Requirements (requirements-analyst)

Skill: **elicit-requirements**

1. Take the stakeholder's narrative about the project.
2. Ask clarifying questions about stakeholders, components, requirements,
   constraints, and success criteria.
3. Write the brief.
4. Derive use cases from the brief.
5. **Review gate**: Present the brief and use cases to the stakeholder.
   Wait for approval before proceeding. If the stakeholder requests changes,
   revise and re-present.

### Stage 1b: Architecture (architect)

Skill: **create-technical-plan**

1. Read the brief and use cases.
2. Design the architecture and write the technical plan.
3. Verify every component traces to at least one use case.
4. **Review gate**: Present the technical plan to the stakeholder.
   Wait for approval before proceeding. If the stakeholder requests changes,
   revise and re-present.

### Sprints (Default Working Mode)

After Stages 1a and 1b are complete, all work is organized into sprints.
A sprint is a focused batch of work with its own lifecycle, branch, and
ticket set.

**Sprint directories** live in `docs/plans/sprints/NNN-slug/`. Each sprint
directory contains `sprint.md`, `brief.md`, `usecases.md`,
`technical-plan.md`, and a `tickets/` subdirectory (see Artifacts §4 above).

**Sprint lifecycle** (skills: **plan-sprint**, **close-sprint**):
1. Stakeholder describes the next batch of work.
2. Create sprint directory with planning documents (brief, use cases,
   technical plan) and a `tickets/` subdirectory.
3. Create sprint branch (`sprint/NNN-slug`).
4. **Architecture review**: Delegate to the **architecture-reviewer** to
   validate the plan against the existing codebase and technical plan.
5. **Review gate**: Present the sprint plan and architecture review to the
   stakeholder. Wait for approval.
6. Create tickets for the sprint in `tickets/` (Stage 2 below).
7. Execute tickets on the sprint branch (Stage 3 below).
8. When all tickets are done, close the sprint: merge branch to main,
   move sprint directory to `docs/plans/sprints/done/`.

Active sprints live in `docs/plans/sprints/`. Completed sprints live in
`docs/plans/sprints/done/`.

### Stage 2: Ticketing (systems-engineer)

Skill: **create-tickets**

1. Break the technical plan into numbered tickets in dependency order.
2. Ensure every use case is covered by at least one ticket.
3. Ensure every ticket traces to at least one use case.
4. **Review gate**: Present the ticket list to the stakeholder. Walk
   through the sequencing and coverage. Wait for approval before starting
   implementation. If the stakeholder requests changes, revise and re-present.

### Stage 3: Implementation (project-manager coordinates)

Skill: **execute-ticket** (repeated for each ticket)

1. Pick the next `todo` ticket whose dependencies are all `done`.
2. Create the ticket plan (`NNN-slug-plan.md`).
3. Set the ticket status to `in-progress` in its YAML frontmatter.
4. Implement the ticket following its plan (python-expert or appropriate
   dev agent).
5. Write tests as specified in the plan.
6. Delegate code review to the **code-reviewer** agent. The reviewer checks
   coding standards, security, test coverage, and acceptance criteria. If
   the review fails, fix the findings and re-review.
7. Update documentation as specified in the plan (documentation-expert).
8. Verify all acceptance criteria are met and check them off (`[x]`).
9. Complete the ticket (see **Completing a Ticket** below).

#### Definition of Done

A ticket is not done until ALL of the following are true:

- [ ] All acceptance criteria in the ticket are met and checked off
- [ ] Tests are written and passing (see `instructions/testing.md`)
- [ ] Code review passed by **code-reviewer** (coding standards, security, test coverage)
- [ ] Documentation updated as specified in the ticket plan
- [ ] Changes committed to git with a message referencing the ticket ID
- [ ] Ticket and plan moved to the sprint's `tickets/done/` directory

Do not mark a ticket done if any item is incomplete. If an item cannot be
satisfied, document why in the ticket before completing.

#### Completing a Ticket

When a ticket satisfies the Definition of Done:

1. Set the ticket's `status` to `done` in its YAML frontmatter.
2. Check off all acceptance criteria (`- [x]`).
3. Commit all changes following `instructions/git-workflow.md`. The commit
   message must reference the ticket ID and sprint number if applicable
   (e.g., `feat: add auth endpoint (#003, sprint 001)`).
4. Move the ticket file to the sprint's `tickets/done/` directory.
5. Move the ticket plan file to the sprint's `tickets/done/` directory.

Active tickets live in the sprint's `tickets/` directory. Completed tickets
live in `tickets/done/`. This separation makes it easy to see at a glance
what work remains (active directory) versus what has been finished (done
directory).

#### Error Recovery

Things go wrong during implementation. Here is what to do.

**Test failures:**
1. Read the error output carefully. Diagnose the root cause.
2. Fix the code (not the test, unless the test is wrong).
3. Re-run the tests. Repeat until all pass.
4. If the failure reveals a flaw in the ticket plan, update the plan.

**Plan gaps** (the plan missed something needed for implementation):
1. If the gap is small and local (e.g., a missing helper function), update
   the ticket plan and continue.
2. If the gap is architectural (e.g., a missing component, wrong API design),
   stop implementation. Flag the gap to the architect. Update the technical
   plan first, then update the ticket plan, then resume.

**Ticket too large** (the ticket is taking much longer than expected):
1. Stop and assess what is done vs. what remains.
2. Split the ticket: complete and close the part that is done (with tests).
3. Create a new ticket for the remaining work. Update dependencies so the
   new ticket depends on the closed one.
4. Resume with the new ticket.

**Unresolvable blockers:**
1. If you cannot make progress despite trying the above patterns, stop.
2. Document what you tried and what blocked you in the ticket.
3. Set the ticket status back to `todo` (not `in-progress` — it is not
   being actively worked).
4. Escalate to the human: explain the blocker and ask for guidance.

### Stage 4: Maintenance

1. If a change alters scope, update the brief and affected use cases first.
2. If new work is needed, create new tickets following the numbering
   sequence.

## Directory Layout

```
docs/plans/
├── brief.md                     # Top-level project brief
├── usecases.md                  # Top-level use cases
├── technical-plan.md            # Top-level technical plan
└── sprints/
    ├── 001-mcp-server/          # Active sprint directory
    │   ├── sprint.md            # Sprint goals, scope, notes
    │   ├── brief.md             # Sprint-level brief
    │   ├── usecases.md          # Sprint-level use cases
    │   ├── technical-plan.md    # Sprint-level technical plan
    │   └── tickets/
    │       ├── 003-add-auth.md      # Active ticket
    │       ├── 003-add-auth-plan.md # Its plan
    │       └── done/                # Completed tickets
    │           ├── 001-setup.md
    │           └── 001-setup-plan.md
    └── done/                    # Completed sprint directories
        └── 000-initial-setup/
            ├── sprint.md
            └── tickets/done/
                └── ...
```

## Rules for AI Assistants

- The **project-manager** is the entry point for new projects. It determines
  current state and delegates to the right agent/skill.
- After initial setup (brief, use cases, technical plan), always work within
  a sprint. Use **plan-sprint** to start and **close-sprint** to finish.
- When asked to plan work, produce or update these artifacts rather than
  jumping straight to code.
- When asked to implement, find the next unfinished ticket and work from it.
- Always create a ticket plan before starting implementation.
- A ticket is not done until it satisfies the **Definition of Done** (see
  above): acceptance criteria met, tests passing, code review passed,
  documentation updated, changes committed to git.
- Delegate code review to the **code-reviewer** agent, not self-review.
- Delegate architecture review to the **architecture-reviewer** agent during
  sprint planning.
- Follow `instructions/coding-standards.md` when writing code.
- Follow `instructions/git-workflow.md` when committing changes.
- Follow `instructions/testing.md` when writing tests.
- When a ticket is completed, follow the **Completing a Ticket** steps
  immediately — do not batch completions.
- Do not create new artifacts without updating the existing ones to stay
  consistent.
- If a change alters scope, update the brief and affected use cases first.
- Use the **project-status** skill at any time to check where things stand.
