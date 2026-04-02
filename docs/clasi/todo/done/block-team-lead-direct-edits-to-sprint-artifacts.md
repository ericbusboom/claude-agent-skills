---
status: done
sprint: '002'
tickets:
- '002'
---

# Block Team-Lead Direct Edits to Sprint Artifacts

Team-lead (Tier 0) can currently directly Edit/Write files under `docs/clasi/sprints/`, bypassing the MCP tools that enforce sprint lifecycle rules.

Fix: in `_handle_role_guard()` at `clasi/hook_handlers.py:102`, add a `docs/clasi/sprints/` exclusion inside the existing Tier 0 `docs/clasi/` allow block. Block the write and tell the model to use MCP tools instead.

Also update the `clasi-artifacts.md` rule (both live and in `init_command.py`) and add tests in `test_role_guard.py`.
