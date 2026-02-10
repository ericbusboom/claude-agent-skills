---
id: "009"
title: Artifact Management tools — query and status
status: done
use-cases: [SUC-005]
depends-on: ["001", "005"]
---

# Artifact Management Tools — Query and Status

Add query tools to `artifact_tools.py` — MCP tools for listing sprints,
listing tickets, and getting status summaries.

## Description

These tools read frontmatter from existing artifacts to provide structured
data about project state. The calling LLM can use these instead of manually
scanning the filesystem.

## Acceptance Criteria

- [ ] `list_sprints(status?)` returns all sprints as JSON array of
      {id, title, status, path, branch}
- [ ] `list_sprints` supports optional status filter (planning, active, done)
- [ ] Scans both `docs/plans/sprints/` and `docs/plans/sprints/done/`
- [ ] `list_tickets(sprint_id?, status?)` returns tickets as JSON array of
      {id, title, status, sprint_id, path}
- [ ] `list_tickets` supports optional sprint_id and status filters
- [ ] Scans both tickets/ and tickets/done/ within sprint directories
- [ ] `get_sprint_status(sprint_id)` returns JSON with {id, title, status,
      branch, tickets: {todo: N, in_progress: N, done: N}}
- [ ] All query tools use the frontmatter parser from ticket 001
- [ ] Empty results return empty arrays (not errors)
