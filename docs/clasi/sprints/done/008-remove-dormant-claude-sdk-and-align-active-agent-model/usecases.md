---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 008 Use Cases

## SUC-001: MCP server starts without importing claude_agent_sdk

- **Actor**: Operator (running `clasi serve` or the MCP server via an IDE)
- **Preconditions**: `claude-agent-sdk` is not installed in the environment.
- **Main Flow**:
  1. Operator starts the CLASI MCP server.
  2. `mcp_server.py` imports `clasi.tools.process_tools` and `clasi.tools.artifact_tools` (dispatch_tools import has been removed).
  3. Preflight check passes — no attempt is made to import `claude_agent_sdk`.
  4. Server is healthy and all MCP tools respond normally.
- **Postconditions**: Server is running; `claude_agent_sdk` is not on the import path.
- **Acceptance Criteria**:
  - [ ] `dispatch_tools` is no longer imported in `mcp_server.py`.
  - [ ] `claude_agent_sdk` does not appear in the import graph of any module loaded during normal server startup.
  - [ ] A guard test asserts that importing `clasi.mcp_server` does not trigger import of `claude_agent_sdk`.

## SUC-002: Agent object loads and renders prompts without SDK dependency

- **Actor**: Any CLASI agent (team-lead, sprint-planner, programmer) calling `agent.render_prompt()`.
- **Preconditions**: `claude-agent-sdk` is not installed.
- **Main Flow**:
  1. Agent calls `project.get_agent("sprint-planner")`.
  2. Agent calls `agent.render_prompt(...)` to render a Jinja2 dispatch template.
  3. Rendered prompt text is returned without error.
- **Postconditions**: Prompt rendered; no SDK import attempted.
- **Acceptance Criteria**:
  - [ ] `Agent.dispatch()`, `_build_role_guard_hooks()`, and `_build_retry_prompt()` are removed from `agent.py`.
  - [ ] `agent.py` has no remaining imports of or references to `claude_agent_sdk`.
  - [ ] `render_prompt()`, `definition`, `contract`, `tier`, `model`, and related read-only properties continue to work.
  - [ ] Existing `test_agent.py` tests that mock `claude_agent_sdk` are removed or updated to reflect the stripped class.

## SUC-003: Project resolves active agents only (no old/ fallback)

- **Actor**: Dispatch tool or skill calling `project.get_agent(name)`.
- **Preconditions**: An old agent name (e.g., `"architect"`) is passed to `get_agent()`.
- **Main Flow**:
  1. Caller requests `project.get_agent("architect")`.
  2. `get_agent()` checks `clasi/plugin/agents/architect/` — does not exist in active dir.
  3. Old fallback is absent; `ValueError` is raised with the list of active agents.
- **Postconditions**: Caller receives a clear error naming the available active agents.
- **Acceptance Criteria**:
  - [ ] `Project.get_agent()` no longer searches `clasi/plugin/agents/old/`.
  - [ ] `list_agents()` does not include agents from `old/`.
  - [ ] Tests confirm that requesting an old agent name raises `ValueError`.

## SUC-004: Active agent contracts and instructions reference current agent roster

- **Actor**: Team-lead or sprint-planner reading their own `agent.md` or `contract.yaml`.
- **Preconditions**: Active agent files previously contained references to old agent names (`project-manager`, `architect`, `technical-lead`, `sprint-executor`, `code-reviewer`, `code-monkey`, `ad-hoc-executor`).
- **Main Flow**:
  1. Agent reads its `agent.md` or `contract.yaml`.
  2. All agent names referenced match the current active roster: `team-lead`, `sprint-planner`, `programmer`.
  3. No old-architecture delegation references appear.
- **Postconditions**: Active plugin files are accurate.
- **Acceptance Criteria**:
  - [ ] `team-lead/contract.yaml` `delegates_to` lists only active agents.
  - [ ] `team-lead/agent.md` does not direct the agent to dispatch to old agent names.
  - [ ] `sprint-planner/contract.yaml` and `agent.md` contain no references to `architect`, `architecture-reviewer`, `technical-lead` as dispatch targets.
  - [ ] A content-check test asserts that no active plugin `.md` or `.yaml` file under `clasi/plugin/agents/` (excluding `old/`) contains the string `code-monkey`, `sprint-executor`, `ad-hoc-executor`, `technical-lead`, `project-manager`, or `code-reviewer` as a delegation target.

## SUC-005: pyproject.toml reflects actual package contents

- **Actor**: Package maintainer running `uv build` or `pip install`.
- **Preconditions**: `pyproject.toml` has stale `package-data` globs and `claude-agent-sdk` dependency.
- **Main Flow**:
  1. Maintainer runs `uv build`.
  2. Only files that exist in the package tree are included.
  3. `claude-agent-sdk` is not listed in dependencies.
- **Postconditions**: Package builds cleanly; `claude-agent-sdk` is absent from the dependency list.
- **Acceptance Criteria**:
  - [ ] `claude-agent-sdk` is removed from `[project.dependencies]` in `pyproject.toml`.
  - [ ] Stale package-data globs (`agents/**`, `skills/*.md`, `instructions/*.md`, `rules/*.md`) that point to non-existent top-level dirs under `clasi/` are removed.
  - [ ] `plugin/**/*` glob (which covers actual plugin content) is retained.
  - [ ] `uv lock` or `uv sync` does not error after the dependency is removed.
