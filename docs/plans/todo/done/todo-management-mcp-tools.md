# TODO Management MCP Tools

The CLASI MCP server has tools for managing tickets (`move_ticket_to_done`,
`update_ticket_status`) but no tools for managing the TODO directory itself.

When reviewing TODOs to move implemented items to `done/`, we had to use
file system operations directly instead of going through the MCP server.

## Needed tools

| Tool | Description |
|------|-------------|
| `list_todos()` | List TODO files in `docs/plans/todo/` with their titles |
| `move_todo_to_done(filename)` | Move a TODO file to `docs/plans/todo/done/` |

These would mirror the ticket management pattern and let AI agents manage
TODOs entirely through the MCP interface.
