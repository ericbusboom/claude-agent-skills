---
id: "008"
title: Artifact Management tools — create
status: done
use-cases: [SUC-003, SUC-004, SUC-007]
depends-on: ["001", "002", "005"]
---

# Artifact Management Tools — Create

Add creation tools to `claude_agent_skills/artifact_tools.py` — MCP tools
for creating sprints, tickets, and top-level planning artifacts.

## Description

These tools create SE artifacts with proper templates, auto-assigned
numbering, and correct directory structure. They return the path and
template content so the calling LLM knows what to edit.

## Acceptance Criteria

- [ ] `create_sprint(title)` creates the sprint directory structure:
      `docs/plans/sprints/NNN-slug/` with sprint.md, brief.md, usecases.md,
      technical-plan.md, and tickets/ + tickets/done/ dirs
- [ ] Sprint number is auto-assigned (scans existing sprints for next number)
- [ ] Slug is derived from title (lowercase, hyphenated, filesystem-safe)
- [ ] Returns JSON with {id, path, branch, files} where files lists all
      created template files
- [ ] `create_ticket(sprint_id, title)` creates a ticket file in the
      sprint's tickets/ dir with auto-assigned number
- [ ] Returns JSON with {id, path, template_content}
- [ ] `create_brief()` creates `docs/plans/brief.md` with template
- [ ] `create_technical_plan()` creates `docs/plans/technical-plan.md`
- [ ] `create_use_cases()` creates `docs/plans/usecases.md`
- [ ] All creation tools refuse to overwrite existing files (return error)
- [ ] All templates use the templates module from ticket 002
- [ ] `docs/plans/` directory is created if it doesn't exist
