---
status: pending
---
# Commit After Artifact Moves

The MCP tools `move_ticket_to_done`, `close_sprint`, and `move_todo_to_done`
move files on disk but do not create git commits. The skill instructions
(`execute-ticket`, `close-sprint`, `plan-sprint`) should explicitly state
that a git commit is required after these file-move operations so that
nothing is left uncommitted at the end of a sprint.
