---
id: "007"
title: Restructure project startup to single overview
status: todo
use-cases: [SUC-005]
depends-on: ["004"]
---

# Restructure Project Startup to Single Overview

## Description

Replace the current three separate top-level documents (brief.md,
usecases.md, technical-plan.md) with a single `docs/plans/overview.md`.
The overview is a general, stable document that covers project identity
and high-level direction. All detailed architecture and scenarios live
inside sprint directories.

This aligns with the principle that sprints are where all the real work
happens. The top-level overview just provides enough context for someone
to understand what the project is and roughly where it's headed.

## Changes Required

1. Update `instructions/system-engineering.md`:
   - Replace Stage 1a (requirements) and Stage 1b (architecture) with
     a single "Project Setup" stage that produces overview.md.
   - The overview document covers: project name, problem statement,
     target users, key constraints, technology stack, high-level
     scenarios, rough sprint roadmap, and out of scope.
   - Remove references to separate top-level brief, usecases, and
     technical-plan.
   - Update the directory layout.
   - All detailed architecture and scenarios are created per-sprint.

2. Update `claude_agent_skills/templates.py`:
   - Add `OVERVIEW_TEMPLATE` for the overview document.
   - Deprecate or remove `BRIEF_TEMPLATE`, `USE_CASES_TEMPLATE`,
     `TECHNICAL_PLAN_TEMPLATE` (for top-level use).
   - Sprint-level usecases and technical-plan templates remain.

3. Update MCP artifact tools:
   - Replace `create_brief()`, `create_technical_plan()`,
     `create_use_cases()` with `create_overview()`.
   - Or keep the old tools with deprecation warnings.

4. Update `skills/elicit-requirements.md`:
   - Workflow now produces overview.md instead of brief + use cases.

5. Update `skills/create-technical-plan.md`:
   - Workflow now operates at the sprint level. The top-level technical
     plan is just a section in the overview document.

## Overview Document Structure

```markdown
---
status: draft
---

# Project Overview

## Project Name
## Problem Statement
## Target Users
## Key Constraints
## Technology Stack
## Key Scenarios
(High-level, narrative descriptions — not formal use cases)
## Sprint Roadmap
(Rough sequence: Sprint 1 does X, Sprint 2 does Y, ...)
## Out of Scope
```

## Acceptance Criteria

- [ ] `docs/plans/overview.md` template exists
- [ ] Instructions describe the single-overview startup workflow
- [ ] Old separate top-level artifact references are removed or updated
- [ ] MCP tools support creating the overview document
- [ ] Elicit-requirements skill produces overview.md
- [ ] Sprint-level usecases.md and technical-plan.md still exist
