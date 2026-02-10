---
id: "005"
title: State MCP tools
status: todo
use-cases:
  - SUC-001
  - SUC-002
  - SUC-003
depends-on:
  - "002"
  - "003"
  - "004"
---

# State MCP tools

## Description

Add five new MCP tools to `claude_agent_skills/artifact_tools.py` that expose
the state database functions to AI agents. These are thin wrappers around the
`state_db.py` functions created in tickets 001-004. All tools return JSON
responses.

The tools bridge the gap between the database layer and the AI agent layer. AI
agents never interact with the SQLite database directly -- they call these MCP
tools, which handle database path resolution and JSON serialization.

### Tools to add

1. **`get_sprint_phase(sprint_id)`** -- Returns the sprint's current phase,
   gate statuses, and lock information. Wraps `get_sprint_state()`. Useful for
   agents to check where a sprint is in its lifecycle before attempting
   operations.

2. **`advance_sprint_phase(sprint_id)`** -- Advances the sprint to the next
   phase if all exit conditions are met. Wraps `advance_phase()`. Returns the
   new phase on success or an error describing unmet conditions on failure.

3. **`record_gate_result(sprint_id, gate, result, notes)`** -- Records the
   outcome of an architecture review or stakeholder approval. Wraps
   `record_gate()`. The `notes` parameter is optional.

4. **`acquire_execution_lock(sprint_id)`** -- Claims the global execution slot
   for a sprint. Wraps `acquire_lock()`. Returns success or an error identifying
   the current lock holder.

5. **`release_execution_lock(sprint_id)`** -- Releases the execution slot.
   Wraps `release_lock()`. Used when a sprint finishes execution or during
   sprint closure.

### Implementation notes

- All tools should resolve the database path using `_plans_dir() / ".clasi.db"`.
- All tools should return JSON (use `json.dumps`).
- Error cases should return JSON with an `"error"` key rather than raising
  exceptions, so agents receive structured error messages.
- Each tool needs the `@server.tool()` decorator.
- Import `state_db` functions at the top of `artifact_tools.py`.

## Acceptance Criteria

- [ ] `get_sprint_phase(sprint_id)` MCP tool is registered and returns JSON with phase, gates, and lock info
- [ ] `advance_sprint_phase(sprint_id)` MCP tool is registered and advances phase or returns structured error
- [ ] `record_gate_result(sprint_id, gate, result, notes)` MCP tool is registered with `notes` as optional
- [ ] `acquire_execution_lock(sprint_id)` MCP tool is registered and returns success or structured lock-holder error
- [ ] `release_execution_lock(sprint_id)` MCP tool is registered and returns success or structured error
- [ ] All five tools are thin wrappers (no business logic duplicated from state_db.py)
- [ ] All tools resolve DB path via `_plans_dir() / ".clasi.db"`
- [ ] All tools return JSON responses
- [ ] Error cases return JSON with an `"error"` key (not raw exceptions)
- [ ] Tools are added to the MCP tools quick reference in `get_se_overview()`
- [ ] Unit tests or integration tests verify each tool's success and error paths
