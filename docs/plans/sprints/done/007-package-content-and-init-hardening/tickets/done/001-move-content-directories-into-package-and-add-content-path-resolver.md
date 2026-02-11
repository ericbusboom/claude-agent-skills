---
id: '001'
title: Move content directories into package and add content_path resolver
status: done
use-cases:
- SUC-001
depends-on: []
---

# Move content directories into package and add content_path resolver

## Description

Move `agents/`, `skills/`, `instructions/` into `claude_agent_skills/` so they
ship with the wheel. Replace `get_repo_root()` with `content_path(*parts)`.
Update all 10 call sites in `process_tools.py`, update `pyproject.toml`
package-data, and update tests.

## Steps

1. `git mv agents/ claude_agent_skills/agents/`
2. `git mv skills/ claude_agent_skills/skills/`
3. `git mv instructions/ claude_agent_skills/instructions/`
4. Add `[tool.setuptools.package-data]` to `pyproject.toml`
5. Replace `get_repo_root()` with `content_path(*parts)` in `mcp_server.py`
6. Update all imports and call sites in `process_tools.py`
7. Update `tests/unit/test_mcp_server.py`
8. Update `tests/system/test_process_tools.py`

## Acceptance Criteria

- [ ] `agents/`, `skills/`, `instructions/` live inside `claude_agent_skills/`
- [ ] `content_path()` resolves relative paths to absolute paths inside the package
- [ ] No code constructs content paths except through `content_path()`
- [ ] `get_repo_root()` is removed
- [ ] `pyproject.toml` includes `*.md` as package data
- [ ] All tests pass
