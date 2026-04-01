---
status: pending
---
# Fix Content Path Resolution After Install

## Problem

When the CLASI MCP server is installed via pipx (or pip), the code resolves
the `agents/`, `skills/`, and `instructions/` directories relative to
`site-packages/` rather than inside the `claude_agent_skills/` package
directory. This means the server can't find its own content files.

Example broken path:
```
/Users/eric/.local/pipx/venvs/claude-agent-skills/lib/python3.14/site-packages/agents
```

Expected correct path:
```
.../site-packages/claude_agent_skills/agents
```

## Likely Cause

The path resolution in `process_tools.py` (or wherever content directories
are located) probably uses `Path(__file__).parent.parent` or similar, which
works in development (where `__file__` is inside `claude_agent_skills/` and
parent.parent reaches the repo root containing `agents/`) but breaks after
installation (where parent.parent reaches `site-packages/`).

## Fix

The content directories (`agents/`, `skills/`, `instructions/`) need to be
either:
1. Bundled inside the `claude_agent_skills/` package and resolved relative
   to `Path(__file__).parent`, or
2. Included as package data in `pyproject.toml` so they get installed inside
   the package directory.

Need to check `pyproject.toml` `[tool.setuptools.package-data]` or
`[tool.setuptools.packages.find]` configuration and the path resolution code.
