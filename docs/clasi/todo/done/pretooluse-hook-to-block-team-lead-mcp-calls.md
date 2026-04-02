---
status: done
sprint: '002'
tickets:
- '016'
---

# PreToolUse Hook to Block Team-Lead MCP Calls and Log All Hooks

Three changes:

## 1. Block team-lead from calling artifact-creation MCP tools

Add a PreToolUse hook that blocks Tier 0 (team-lead) from calling MCP tools that create planning artifacts directly. At minimum: `create_ticket`, `create_sprint`. The sprint-planner agent (Tier 1) should be the only one calling these.

Use the same pattern as the existing role guard — check `CLASI_AGENT_TIER` env var, exit 2 to block with a message telling the team-lead to dispatch to sprint-planner.

## 2. Add a hook activity log

Log all hook invocations to a log file in `docs/clasi/log/`. Every PreToolUse, PostToolUse, SubagentStart, SubagentStop, TaskCreated, TaskCompleted event should append a line to a hook log (e.g. `docs/clasi/log/hooks.log`) with timestamp, event type, and key payload fields. This provides an audit trail of all hook activity.

## 3. Remove the handle_hook dispatcher

The `handle_hook()` function in `hook_handlers.py` is unnecessary indirection. Each hook script (e.g. `.claude/hooks/role_guard.py`) already knows which event it handles. The handler function should be called directly from the script instead of going through a dispatcher. For example, `role_guard.py` should call `_handle_role_guard(payload)` directly instead of `handle_hook("role-guard")`.
