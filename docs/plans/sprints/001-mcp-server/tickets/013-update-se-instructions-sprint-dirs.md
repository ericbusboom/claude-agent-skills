---
id: "013"
title: Update SE instructions for sprint-as-directory
status: todo
use-cases: [SUC-003]
depends-on: []
---

# Update SE Instructions for Sprint-as-Directory

Update `instructions/system-engineering.md` and related files to reflect
the sprint-as-directory model and per-sprint ticket numbering.

## Description

The SE instructions currently describe sprints as single files
(`docs/plans/sprints/NNN-slug.md`). Update to reflect the directory model
where each sprint is a directory containing sprint.md, brief.md,
usecases.md, technical-plan.md, and tickets/.

Also update ticket numbering references from global to per-sprint, and
update the directory layout diagram.

## Acceptance Criteria

- [ ] Sprint section in SE instructions describes directory structure
- [ ] Sprint frontmatter example shows `docs/plans/sprints/NNN-slug/sprint.md`
- [ ] Directory layout diagram shows sprint directories with sub-files
- [ ] Ticket numbering described as per-sprint (001 within each sprint)
- [ ] Completing a Ticket section references sprint ticket paths
- [ ] `plan-sprint` skill updated for directory creation
- [ ] `close-sprint` skill updated for directory moves
- [ ] `project-status` skill updated for scanning sprint directories
- [ ] No references to the old `docs/plans/tickets/` top-level directory
      (except for historical context)
