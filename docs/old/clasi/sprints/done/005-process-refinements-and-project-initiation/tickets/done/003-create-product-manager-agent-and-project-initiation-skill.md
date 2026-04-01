---
id: '003'
title: Create product-manager agent and project-initiation skill
status: done
use-cases:
- SUC-002
depends-on:
- '001'
---

# Create product-manager agent and project-initiation skill

## Description

Create a new `agents/product-manager.md` agent definition that specializes in
project initiation interviews. Create `skills/project-initiation.md` that
defines the interview workflow: stakeholder narrates, agent asks clarifying
questions via AskUserQuestion, then synthesizes into `docs/plans/overview.md`.

The product-manager is distinct from the requirements-analyst — it handles the
initial overview-level interview, while the requirements-analyst does detailed
requirements elicitation. The project-manager delegates to product-manager for
initiation.

Also add a `project-initiation` thin skill stub to `SKILL_STUBS` in
`init_command.py` so the `/project-initiation` slash command works.

## Acceptance Criteria

- [ ] `agents/product-manager.md` exists with agent definition
- [ ] `skills/project-initiation.md` exists with interview workflow
- [ ] Skill references `create_overview` MCP tool
- [ ] Skill uses `AskUserQuestion` for clarifying questions
- [ ] `init_command.py` SKILL_STUBS includes `project-initiation`
- [ ] SE instruction updated to list product-manager agent
- [ ] Tests for init_command updated
