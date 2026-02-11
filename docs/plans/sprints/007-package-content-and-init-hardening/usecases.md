---
status: draft
---

# Sprint 007 Use Cases

## SUC-001: Content path resolution works after install
Parent: none (bug fix)

- **Actor**: CLASI MCP server running after pipx install
- **Preconditions**: Package installed via pip/pipx (not editable)
- **Main Flow**:
  1. MCP tool is called (e.g. `list_agents`)
  2. Tool calls `content_path("agents")` to locate the agents directory
  3. Function resolves to the correct directory inside the installed package
  4. Tool reads `.md` files and returns content
- **Postconditions**: Tool returns valid agent/skill/instruction content
- **Acceptance Criteria**:
  - [ ] `agents/`, `skills/`, `instructions/` live inside `claude_agent_skills/`
  - [ ] `content_path()` resolves relative paths to absolute paths inside the package
  - [ ] No code constructs content paths except through `content_path()`
  - [ ] `get_repo_root()` is removed
  - [ ] `pyproject.toml` includes `*.md` as package data

## SUC-002: clasi init sets up MCP permissions
Parent: none (enhancement)

- **Actor**: Developer running `clasi init` on a new repo
- **Preconditions**: Target repo exists
- **Main Flow**:
  1. Developer runs `clasi init /path/to/repo`
  2. Init creates `.claude/settings.local.json`
  3. File contains `permissions.allow` with `mcp__clasi__*`
- **Postconditions**: All CLASI MCP tools are pre-approved
- **Acceptance Criteria**:
  - [ ] `clasi init` creates `.claude/settings.local.json`
  - [ ] File contains `{"permissions": {"allow": ["mcp__clasi__*"]}}`
  - [ ] Merges with existing file if present
  - [ ] Idempotent (running twice produces same result)

## SUC-003: Smoke test verifies MCP content access
Parent: none (testing)

- **Actor**: Test suite
- **Preconditions**: Package is importable
- **Main Flow**:
  1. Test calls `list_agents()` and verifies non-empty result
  2. Test calls `get_instruction("coding-standards")` and verifies content
  3. Test calls `list_skills()` and verifies non-empty result
- **Postconditions**: Content access confirmed working
- **Acceptance Criteria**:
  - [ ] Smoke test calls at least 3 MCP tool functions
  - [ ] Verifies returned content is non-empty and valid
  - [ ] Test lives in `tests/system/`
