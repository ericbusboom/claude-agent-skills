---
id: "004"
title: Merge sprint.md and brief.md into single document
status: todo
use-cases: [SUC-004]
depends-on: []
---

# Merge sprint.md and brief.md

## Description

The sprint.md and brief.md files in each sprint directory overlap
significantly. Both describe what the sprint is about and why. Merge
them into a single sprint.md that includes the brief content (problem,
solution, success criteria) alongside the sprint metadata (goals, scope,
tickets).

## Changes Required

1. Update `claude_agent_skills/templates.py`:
   - Update `SPRINT_TEMPLATE` to include Problem, Solution, and Success
     Criteria sections (currently in the brief template).
   - Remove or deprecate `SPRINT_BRIEF_TEMPLATE`.
   - The `create_sprint` MCP tool should no longer create `brief.md`.

2. Update `instructions/system-engineering.md`:
   - Update the sprint directory structure to not show `brief.md`.
   - Update any references to sprint-level brief.md.

3. Update `skills/plan-sprint.md`:
   - Remove the step that creates a separate brief.
   - Update the workflow to write problem/solution into sprint.md.

## New Sprint Template Structure

```markdown
# Sprint NNN: Title

## Problem
(What problem this sprint addresses — from brief)

## Solution
(High-level approach — from brief)

## Goals
(Sprint goals — existing)

## Scope
### In Scope
### Out of Scope

## Success Criteria
(Measurable outcomes — from brief)

## Architecture Notes

## Test Strategy
(See ticket 005)

## Tickets
| ID | Title | Depends On |
```

## Acceptance Criteria

- [ ] Sprint template includes Problem, Solution, and Success Criteria
- [ ] Sprint template does not reference a separate brief.md
- [ ] `create_sprint` MCP tool creates sprint.md without brief.md
- [ ] Plan-sprint skill workflow uses the merged template
- [ ] SE instructions reflect the merged structure
