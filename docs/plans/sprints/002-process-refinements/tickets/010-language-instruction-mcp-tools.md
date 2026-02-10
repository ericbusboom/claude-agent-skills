---
id: "010"
title: Add MCP tools for per-language instructions
status: todo
use-cases: [SUC-008]
depends-on: ["009"]
---

# Add MCP Tools for Per-Language Instructions

## Description

Add two MCP tools to the SE Process Access group for discovering and
reading language-specific instructions. These follow the same pattern
as `list_instructions` / `get_instruction` but are scoped to the
`instructions/languages/` subdirectory.

## Changes Required

1. Update `claude_agent_skills/process_tools.py`:
   - Add `list_language_instructions` tool:
     - Scans `instructions/languages/` for `.md` files
     - Returns `[{name, description}]` from frontmatter
   - Add `get_language_instruction(language)` tool:
     - Reads the specified language file (e.g., "python" ->
       `instructions/languages/python.md`)
     - Returns the full markdown content
     - Returns an error if the language is not found

2. Update MCP server registration to include the new tools.

3. Update `get_activity_guide("implementation")` to mention available
   language instructions when applicable.

## Acceptance Criteria

- [ ] `list_language_instructions` MCP tool exists and returns all
      language instruction files
- [ ] `get_language_instruction("python")` returns the Python instruction
      content
- [ ] `get_language_instruction("nonexistent")` returns a clear error
- [ ] Tools are registered in the MCP server
- [ ] Activity guide for implementation mentions language instructions
- [ ] Unit tests cover both tools including error cases
