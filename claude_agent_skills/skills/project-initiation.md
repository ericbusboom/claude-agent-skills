---
name: project-initiation
description: Guides a stakeholder through a project initiation interview and produces a project overview document
---

# Project Initiation Skill

This skill creates a project overview document through a guided interview
with the stakeholder, using the product-manager agent.

## Agent Used

**product-manager**

## Inputs

- Stakeholder narration describing what they want to build

## Process

1. **Capture narration**: Take the stakeholder's initial description of the
   project. This may come as a spoken narration, a written description, or a
   conversation.

2. **Ask clarifying questions**: Present 2-4 targeted questions using
   `AskUserQuestion` to fill gaps in the narration. Focus on:
   - Problem statement and target users (if unclear)
   - Key constraints (timeline, technology, budget)
   - High-level requirements (key scenarios)
   - Out of scope

3. **Create overview document**: Call `create_overview` MCP tool to create
   `docs/plans/overview.md` with the template, then fill in each section
   using the narration and answers.

4. **Link into IDE instructions**: After creating the overview:
   - Copy or link it to `.claude/rules/project-overview.md` so Claude Code
     sees it as project context
   - Copy or link it to `.github/copilot/instructions/project-overview.md`
     for GitHub Copilot

5. **Stakeholder review**: Present the completed overview to the stakeholder.
   Use `AskUserQuestion`:
   - "Approve overview" (recommended)
   - "Request changes"

   If the stakeholder requests changes, revise and re-present. Only proceed
   when approved.

## Output

- `docs/plans/overview.md` — The project overview document
- `.claude/rules/project-overview.md` — IDE-visible copy
- `.github/copilot/instructions/project-overview.md` — IDE-visible copy

## Notes

- This skill is for project initiation only. For detailed requirements on
  complex projects, use the **elicit-requirements** skill instead.
- After the overview is approved, use **plan-sprint** to begin the first
  sprint.
