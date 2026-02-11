---
status: draft
---

# Sprint 007 Technical Plan

## Architecture Overview

The core change is moving content directories into the Python package and
replacing all direct path construction with a single resolver function.
This is a structural refactor with a small init_command enhancement.

```
BEFORE:                          AFTER:
repo/                            repo/
├── agents/                      ├── claude_agent_skills/
├── skills/                      │   ├── agents/
├── instructions/                │   ├── skills/
├── claude_agent_skills/         │   ├── instructions/
│   ├── mcp_server.py            │   ├── mcp_server.py
│   └── process_tools.py         │   ├── process_tools.py
└── pyproject.toml               │   └── ...
                                 └── pyproject.toml
```

## Component Design

### Component: content_path() resolver — mcp_server.py

**Use Cases**: SUC-001

Replace `get_repo_root()` with:

```python
_CONTENT_ROOT = Path(__file__).parent.resolve()

def content_path(*parts: str) -> Path:
    """Resolve a relative content path to an absolute path.

    Examples:
        content_path("agents")                    → .../claude_agent_skills/agents/
        content_path("agents", "technical-lead.md") → .../claude_agent_skills/agents/technical-lead.md
        content_path("instructions", "languages")  → .../claude_agent_skills/instructions/languages/
    """
    return _CONTENT_ROOT.joinpath(*parts)
```

- Module-level constant `_CONTENT_ROOT` computed once
- `content_path()` accepts one or more path segments
- No validation inside the function (callers handle missing files)
- Remove `get_repo_root()` entirely

### Component: process_tools.py call site updates

**Use Cases**: SUC-001

All 10 call sites change from:
```python
root = get_repo_root()
# ... root / "agents" ...
```
to:
```python
# ... content_path("agents") ...
```

The two helper functions `_list_definitions()` and `_get_definition()` already
take a `directory: Path` argument — their callers just change what they pass.

Affected functions (10 total):
- `get_se_overview()` — uses agents, skills, instructions
- `list_agents()` — uses agents
- `list_skills()` — uses skills
- `list_instructions()` — uses instructions
- `get_agent_definition()` — uses agents
- `get_skill_definition()` — uses skills
- `get_instruction()` — uses instructions
- `list_language_instructions()` — uses instructions/languages
- `get_language_instruction()` — uses instructions/languages
- `get_activity_guide()` — uses agents, skills, instructions

### Component: pyproject.toml package data

**Use Cases**: SUC-001

Add to `pyproject.toml`:
```toml
[tool.setuptools.package-data]
claude_agent_skills = ["agents/*.md", "skills/*.md", "instructions/*.md", "instructions/languages/*.md"]
```

### Component: init_command.py — MCP permissions

**Use Cases**: SUC-002

Add to `run_init()`:
- Create/merge `.claude/settings.local.json`
- Set `{"permissions": {"allow": ["mcp__clasi__*"]}}`
- Same merge pattern as `.mcp.json` (read existing, merge, write)

### Component: Smoke test — tests/system/test_content_smoke.py

**Use Cases**: SUC-003

New test file that imports and calls the actual MCP tool functions:
- `list_agents()` returns non-empty JSON array
- `get_instruction("coding-standards")` returns markdown with content
- `list_skills()` returns non-empty JSON array
- Validates that `content_path("agents")` directory exists and has `.md` files

### Component: Test updates

**Use Cases**: SUC-001

- `tests/unit/test_mcp_server.py`: Update `TestGetRepoRoot` → test
  `content_path()` instead
- `tests/system/test_process_tools.py`: Replace `get_repo_root()` calls
  with `content_path()` calls
- `tests/unit/test_init_command.py`: Add test for settings.local.json creation

## Decisions

1. **`content_path()` does NOT validate** — it is a pure path resolver.
   Callers already raise context-specific errors for missing files.
   (Architecture review recommendation, accepted.)
