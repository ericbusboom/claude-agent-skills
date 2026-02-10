---
id: "008"
title: Rename use cases to scenarios
status: todo
use-cases: [SUC-006]
depends-on: ["007"]
---

# Rename Use Cases to Scenarios

## Description

Replace "use case" terminology with "scenario" throughout the process.
Scenarios are less formal and better match how the project actually
uses these descriptions. The identifier prefix changes from `UC-` /
`SUC-` to `SC-` / `SSC-` (Sprint Scenario).

This is a broad renaming that touches instructions, templates, skills,
agents, and the sprint-level usecases.md files (which become
scenarios.md).

## Changes Required

1. **Instructions** (`instructions/system-engineering.md`):
   - Replace "use case" with "scenario" throughout
   - Replace "UC-" references with "SC-"
   - Rename the "Use Cases" artifact to "Scenarios"
   - Update the scenario document format (ID prefix: SC-NNN)

2. **Templates** (`claude_agent_skills/templates.py`):
   - Rename `USE_CASES_TEMPLATE` to `SCENARIOS_TEMPLATE`
   - Rename `SPRINT_USECASES_TEMPLATE` to `SPRINT_SCENARIOS_TEMPLATE`
   - Update template content (headers, ID prefixes)

3. **Skills**:
   - Update `skills/elicit-requirements.md`: produce scenarios
   - Update `skills/create-tickets.md`: reference scenarios
   - Update `skills/plan-sprint.md`: reference scenarios
   - Update any other skills that mention use cases

4. **Agents**:
   - Update `agents/requirements-analyst.md`: produce scenarios
   - Update any agents that reference use cases

5. **Sprint-level files**:
   - Rename `usecases.md` to `scenarios.md` in sprint templates
   - Update MCP tools that reference usecases.md

6. **Ticket frontmatter**:
   - The `use-cases` field in ticket frontmatter becomes `scenarios`

## Acceptance Criteria

- [ ] All instructions use "scenario" instead of "use case"
- [ ] All templates use "scenario" terminology
- [ ] Sprint-level file is named `scenarios.md` not `usecases.md`
- [ ] Identifier prefix is `SC-` / `SSC-` not `UC-` / `SUC-`
- [ ] All skills reference scenarios
- [ ] Ticket frontmatter uses `scenarios` field
- [ ] No remaining references to "use case" in active instructions,
      templates, or skills
