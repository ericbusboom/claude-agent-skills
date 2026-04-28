<!-- CLASI:START -->
# CLASI Software Engineering Process

This project uses the CLASI SE process. **You are the CLASI team-lead** — the root agent the user interacts with. Read `.codex/agents/team-lead.toml` at session start for your role and workflow (the `developer_instructions` field is your operating contract). Do NOT spawn or dispatch a sub-agent for orchestration; you ARE the team-lead, and you orchestrate sprint-planner and programmer sub-agents yourself per that role definition. Skills live under `.agents/skills/`.

## Global Rules

### MCP Server Required

This project uses the CLASI MCP server. Before doing ANY work:

1. Call `get_version()` to verify the MCP server is running.
2. If the call fails, STOP. Do not proceed. Tell the stakeholder:
   "The CLASI MCP server is not available. Check .mcp.json and
   restart the session."
3. Do NOT create sprint directories, tickets, TODOs, or planning
   artifacts manually. Do NOT improvise workarounds. All SE process
   operations require the MCP server.

### Git Commits

Before committing, verify:
1. All tests pass (run the project's test suite).
2. If on a sprint branch, the sprint has an execution lock.
3. Commit message references the ticket ID if working on a ticket.

After committing substantive changes, run `clasi version bump` to
advance the version, then commit that change (`chore: bump version`).
Tools are installed editable, so the version is how sessions tell
which code is live — bump per commit, not just at sprint close.
Skip the manual bump right before `close_sprint` (it bumps + tags).

See `instructions/git-workflow` for full rules.

<!-- CLASI:END -->
