---
id: "021"
title: Fix step numbering in system-engineering.md
status: done
use-cases: [UC-004]
depends-on: []
---

# 021: Fix Step Numbering in System-Engineering.md

## Description

The workflow section has duplicate step numbers across phases caused by
incremental edits. Fix by restarting numbering within each phase so steps
are unambiguous.

## Acceptance Criteria

- [x] No duplicate step numbers across the workflow
- [x] Each phase has its own numbering starting at 1
- [x] Review gate steps are included in each phase's numbering
