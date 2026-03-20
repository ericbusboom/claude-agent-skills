---
timestamp: '2026-03-20T23:01:05'
parent: team-lead
child: sprint-executor
scope: claude_agent_skills/, tests/, docs/clasi/sprints/024-e2e-guessing-game-test/
sprint: 024-e2e-guessing-game-test
result: "success \u2014 tickets 015+016 done, 439 tests"
files_modified:
- claude_agent_skills/artifact_tools.py
- claude_agent_skills/dispatch_log.py
- claude_agent_skills/process_tools.py
- claude_agent_skills/se-overview-template.md
- pyproject.toml
- claude_agent_skills/agents/domain-controllers/sprint-planner/dispatch-template.md.j2
- claude_agent_skills/agents/domain-controllers/sprint-executor/dispatch-template.md.j2
- claude_agent_skills/agents/task-workers/code-monkey/dispatch-template.md.j2
---

# Dispatch: team-lead → sprint-executor

You are the sprint-executor. Execute tickets 015 and 016 for sprint 024.

Read both tickets first.

**Ticket 015: Typed dispatch MCP tools with Jinja2 templates**

1. Add `jinja2` to dependencies in pyproject.toml.

2. Convert the 3 dispatch templates to Jinja2:
   - `claude_agent_skills/agents/domain-controllers/sprint-planner/dispatch-template.md` — replace UPPERCASE placeholders with `{{ variable_name }}`
   - `claude_agent_skills/agents/domain-controllers/sprint-executor/dispatch-template.md` — same
   - `claude_agent_skills/agents/task-workers/code-monkey/dispatch-template.md` — same

3. Create 3 new MCP tools in artifact_tools.py:

```python
@server.tool()
def dispatch_to_sprint_planner(sprint_id: str, sprint_directory: str, todo_ids: list[str], goals: str) -> str:
    """Prepare and log a dispatch to sprint-planner. Returns rendered prompt."""

@server.tool()  
def dispatch_to_sprint_executor(sprint_id: str, sprint_directory: str, branch_name: str, tickets: list[str]) -> str:
    """Prepare and log a dispatch to sprint-executor. Returns rendered prompt."""

@server.tool()
def dispatch_to_code_monkey(ticket_path: str, ticket_plan_path: str, scope_directory: str, sprint_name: str, ticket_id: str) -> str:
    """Prepare and log a dispatch to code-monkey. Returns rendered prompt."""
```

Each tool: loads the Jinja2 template from the agent directory, renders with parameters, calls log_dispatch internally (with template_used set), returns JSON with {prompt, log_path}.

4. Remove `get_dispatch_template` MCP tool. Remove `TEMPLATED_AGENTS` enforcement from dispatch_log.py. Keep `log_subagent_dispatch` for non-templated dispatches (todo-worker, architect, etc.) but remove `template_used` enforcement (it's handled by the typed tools now).

5. Update agent definitions (team-lead, sprint-executor) to reference the new tools instead of manual template loading.

6. Update test_mcp_server.py — add 3 new tools, remove get_dispatch_template, adjust count.

7. Write tests for the 3 new tools.

**Ticket 016: Extract SE overview inline text to file**

1. Create a content file at `claude_agent_skills/content/se-overview-template.md` (or similar) containing the Process Stages and MCP Tools Quick Reference sections currently hardcoded in get_se_overview().

2. Update get_se_overview() in process_tools.py to read from the file and interpolate the dynamic agent/skill/instruction listings.

3. Write a test verifying get_se_overview() still returns the expected sections.

For each ticket: implement, run tests (`uv run pytest -p no:cacheprovider --override-ini="addopts="`), update frontmatter to done, check off criteria, move to tickets/done/, commit.

Working directory: /Volumes/Proj/proj/RobotProjects/scratch/claude-agent-skills
