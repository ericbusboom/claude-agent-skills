---
status: pending
---

# Move Tool Logic Into Domain Models (Project, Sprint, Ticket)

Nearly all of the logic in the MCP tool files (artifact_tools.py, process_tools.py) should be moved into the domain model classes: Project, Sprint, and Ticket. The tool functions should be thin glue code that:

1. Gets the Project instance
2. Finds the relevant Sprint or Ticket
3. Calls one or two methods on it
4. Returns the result

Business logic like path construction, frontmatter manipulation, file moves, validation, and state transitions belongs in the model classes, not in the tool layer.
