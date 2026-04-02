---
status: done
sprint: '002'
tickets:
- '011'
---

# Tool Returns Should Be Sprint Object, Not Dicts

MCP tools like `create_sprint` currently return hand-built dicts with id, path, branch, files, phase, etc. They should just return the Sprint object (or its serialization). All of those values are already available as properties on the Sprint object — the tools shouldn't have to reconstruct them manually.

This reduces duplication and ensures the returned data is always consistent with the Sprint model.
