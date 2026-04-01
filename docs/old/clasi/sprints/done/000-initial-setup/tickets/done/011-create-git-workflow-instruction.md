---
id: "011"
title: Create git workflow instruction
status: done
use-cases: [UC-005]
depends-on: []
---

# 011: Create Git Workflow Instruction

## Description

Create `instructions/git-workflow.md` defining when and how agents interact
with git during ticket execution: commit timing, message format, branch
strategy, and safety rules.

## Acceptance Criteria

- [x] `instructions/git-workflow.md` exists with YAML frontmatter
- [x] Defines commit timing (at minimum: commit when ticket is complete)
- [x] Defines commit message format with ticket ID references
- [x] Defines branch strategy options (feature branches vs. main)
- [x] Includes safety rules (no force-push, no skipping hooks)
