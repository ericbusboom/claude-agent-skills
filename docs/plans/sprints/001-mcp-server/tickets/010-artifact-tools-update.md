---
id: "010"
title: Artifact Management tools — update and close
status: todo
use-cases: [SUC-006]
depends-on: ["001", "005"]
---

# Artifact Management Tools — Update and Close

Add mutation tools to `artifact_tools.py` — MCP tools for updating status,
moving tickets to done, and closing sprints.

## Description

These tools modify artifact frontmatter and move files between active and
done directories.

## Acceptance Criteria

- [ ] `update_ticket_status(path, status)` updates the status field in
      the ticket's YAML frontmatter without changing the body
- [ ] Validates status is one of: todo, in-progress, done
- [ ] Returns JSON with {path, old_status, new_status}
- [ ] `move_ticket_to_done(path)` moves the ticket file and its
      corresponding plan file to the sprint's tickets/done/ directory
- [ ] Returns JSON with {old_path, new_path}
- [ ] Handles case where plan file doesn't exist (moves ticket only)
- [ ] `close_sprint(sprint_id)` moves the entire sprint directory to
      `docs/plans/sprints/done/`
- [ ] Updates sprint status to "done" in frontmatter before moving
- [ ] Returns JSON with {old_path, new_path}
- [ ] All tools return clear errors for invalid paths or missing files
