---
id: "002"
title: Templates module
status: done
use-cases: [SUC-003, SUC-004, SUC-007]
depends-on: []
---

# Templates Module

Create `claude_agent_skills/templates.py` — artifact templates for sprints,
tickets, briefs, technical plans, and use cases.

## Description

The MCP artifact creation tools need templates with correct YAML frontmatter
and section structure. Templates use Python string formatting for dynamic
values (id, title, slug, branch name, etc.).

## Acceptance Criteria

- [ ] `SPRINT_TEMPLATE` — sprint.md with frontmatter (id, title, status,
      branch, use-cases) and sections (Goals, Scope, Architecture Notes, Tickets)
- [ ] `SPRINT_BRIEF_TEMPLATE` — sprint-level brief with frontmatter and
      standard sections
- [ ] `SPRINT_USECASES_TEMPLATE` — sprint-level use cases with frontmatter
- [ ] `SPRINT_TECHNICAL_PLAN_TEMPLATE` — sprint-level technical plan with
      frontmatter and standard sections
- [ ] `TICKET_TEMPLATE` — ticket with frontmatter (id, title, status,
      use-cases, depends-on) and sections (Description, Acceptance Criteria)
- [ ] `BRIEF_TEMPLATE` — top-level brief
- [ ] `TECHNICAL_PLAN_TEMPLATE` — top-level technical plan
- [ ] `USE_CASES_TEMPLATE` — top-level use cases
- [ ] Each template produces valid YAML frontmatter when formatted
- [ ] A `slugify(title)` helper converts titles to filesystem-safe slugs
