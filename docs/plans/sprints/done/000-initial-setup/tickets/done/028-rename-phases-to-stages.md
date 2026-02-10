---
id: "028"
title: Rename phases to stages in SE instructions
status: done
use-cases: [UC-010]
depends-on: []
---

# Rename Phases to Stages in SE Instructions

Rename "Phase" to "Stage" throughout the SE instructions and related files
to free the term "phase/sprint" for the new sprint concept.

## Description

The SE workflow currently uses "Phase 1a", "Phase 1b", etc. The user wants
to use "sprint" for the new work-grouping concept. To avoid confusion,
rename the existing workflow steps from "Phase" to "Stage" (Stage 1a,
Stage 1b, Stage 2, Stage 3, Stage 4).

This is a terminology change only — no structural changes to the workflow.

## Acceptance Criteria

- [ ] All occurrences of "Phase" in `instructions/system-engineering.md`
      are replaced with "Stage"
- [ ] All occurrences of "Phase" in `agents/project-manager.md` are
      replaced with "Stage"
- [ ] All occurrences of "phase" in `skills/*.md` that refer to workflow
      stages are updated
- [ ] UC-009 in usecases.md is updated (already done in this round)
- [ ] No broken references or inconsistencies after rename
