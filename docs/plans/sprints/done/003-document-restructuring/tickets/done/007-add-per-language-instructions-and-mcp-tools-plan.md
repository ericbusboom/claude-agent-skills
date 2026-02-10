# Ticket 007 Plan: Add per-language instructions and MCP tools

## Approach

Follow the existing `list_instructions`/`get_instruction` pattern in
`process_tools.py`. The language instructions live in a subdirectory
(`instructions/languages/`) rather than in the top-level `instructions/`
directory. The two new MCP tools reuse the existing `_list_definitions`
and `_get_definition` helpers pointed at the `languages/` subdirectory.

## Files to create or modify

1. **Create** `instructions/languages/python.md` — Python-specific instruction
   file with frontmatter covering venvs/uv, pyproject.toml, type hints,
   pytest patterns, and Python idioms.
2. **Modify** `claude_agent_skills/process_tools.py` — Add
   `list_language_instructions` and `get_language_instruction` MCP tools.
3. **Modify** `tests/test_process_tools.py` — Add tests for both new tools.

## Testing plan

- Unit test: `list_language_instructions` returns a JSON array containing
  at least the `python` entry with name and description.
- Unit test: `get_language_instruction("python")` returns content containing
  expected sections (venvs, type hints, pytest, etc.).
- Unit test: `get_language_instruction("nonexistent")` raises `ValueError`.

## Documentation updates

None required — the MCP tools are self-documenting via their docstrings
and the SE instructions already reference per-language instructions in the
sprint technical plan.
