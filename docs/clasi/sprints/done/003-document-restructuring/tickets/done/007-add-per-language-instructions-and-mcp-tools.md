---
id: '007'
title: Add per-language instructions and MCP tools
status: done
use-cases:
- SUC-007
depends-on: []
---

# Add per-language instructions and MCP tools

## Description

Create `instructions/languages/` directory with `python.md` as the first
language-specific instruction file. Add two MCP tools to `process_tools.py`
following the existing `list_instructions`/`get_instruction` pattern.

### Python instruction content

- Virtual environments and `uv` usage
- `pyproject.toml` project configuration
- Type hints conventions
- pytest patterns and fixtures
- Python idioms and style preferences

### MCP tools

| Tool | Description |
|------|-------------|
| `list_language_instructions` | List available language instruction files |
| `get_language_instruction(language)` | Get full content of a language instruction |

## Acceptance Criteria

- [x] `instructions/languages/python.md` exists with frontmatter
- [x] Python instruction covers venvs, pyproject.toml, type hints, pytest, idioms
- [x] `list_language_instructions` MCP tool returns available languages
- [x] `get_language_instruction("python")` returns full python.md content
- [x] Error handling for unknown language names
- [x] Unit tests for both MCP tools
