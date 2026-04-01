---
status: pending
---

# Reorganize CLASI as a Claude Code Plugin

## Context

The CLASI SE process currently has 13 agents, 10 skills, 9 instructions, and 3 rules scattered across `clasi/{agents,skills,instructions,rules,hooks}`. An `init_command.py` copies files from scattered sources into a project's `.claude/` directory. This is fragile, hard to version, and requires manual setup.

Claude Code has a native plugin system that provides exactly what we need: bundled skills, agents, hooks, and MCP servers, installable with a single command. CLASI becomes a plugin.

## Decisions made

1. **Consolidate 13 agents to 3** (per `consolidate-agents-13-to-3.md`)
2. **CLASI becomes a Claude Code plugin** — skills, agents, hooks bundled natively. No `init` command. Install via `/plugin install clasi`.
3. **Break embedded skills out of agents** into standalone plugin skills
4. **Remove all `dispatch_to_*` MCP tools** — use native Agent tool for sprint-planner, agent teams + Tasks for programmer
5. **Hooks are thin glue** — `uv run clasi hook <event>` calls into testable Python code in `clasi/hooks/`
6. **Agent teams + Tasks for sprint execution** — parallel programmer teammates in worktrees, replacing serial dispatch loop
7. **Programmer resolves its own merge conflicts** — TaskCompleted hook blocks, programmer fixes and retries

## New 3-Agent Model

| Agent | Absorbs | Invocation |
|-------|---------|------------|
| **team-lead** | sprint-executor, sprint-reviewer, ad-hoc-executor, project-manager, project-architect, todo-worker | IS the session. Behavior defined by plugin rules + skills |
| **sprint-planner** | architect, architecture-reviewer, technical-lead | Invoked via native Agent tool by team-lead |
| **programmer** | code-reviewer (dropped for now) | Spawned as agent-team teammate via Tasks |

## Plugin Structure

```
clasi-plugin/                              # or a subdirectory of the existing repo
├── .claude-plugin/
│   └── plugin.json                        # manifest: name, version, description
│
├── .mcp.json                              # bundles the CLASI MCP server (artifact + process tools)
│
├── hooks/
│   └── hooks.json                         # all hook registrations → `uv run clasi hook <event>`
│
├── settings.json                          # agent config (only `agent` key supported by plugins)
│
├── agents/
│   ├── sprint-planner/
│   │   └── agent.md                       # Consolidated from architect + arch-reviewer + technical-lead
│   └── programmer/
│       └── agent.md                       # Renamed from code-monkey, simplified
│
├── skills/
│   ├── se/SKILL.md                        # /clasi:se — main dispatcher
│   │
│   │  # -- Extracted from agents (embedded docs become standalone skills) --
│   ├── plan-sprint/SKILL.md               # FROM sprint-planner/plan-sprint.md
│   ├── execute-sprint/SKILL.md            # FROM sprint-executor/execute-ticket.md + close-sprint.md
│   ├── create-tickets/SKILL.md            # FROM sprint-planner/create-tickets.md + technical-lead/agent.md
│   ├── oop/SKILL.md                       # FROM ad-hoc-executor/oop.md
│   ├── todo/SKILL.md                      # FROM todo-worker/todo.md
│   ├── gh-import/SKILL.md                 # FROM todo-worker/gh-import.md
│   ├── project-status/SKILL.md            # FROM team-lead/project-status.md
│   ├── project-initiation/SKILL.md        # FROM project-manager/agent.md (initiation mode)
│   ├── sprint-roadmap/SKILL.md            # FROM project-manager/agent.md (roadmap mode)
│   ├── sprint-review/SKILL.md             # FROM sprint-reviewer/agent.md
│   ├── close-sprint/SKILL.md              # FROM sprint-executor/close-sprint.md
│   ├── tdd-cycle/SKILL.md                 # FROM code-monkey/tdd-cycle.md
│   ├── systematic-debugging/SKILL.md      # FROM code-monkey/systematic-debugging.md
│   ├── code-review/SKILL.md               # FROM code-reviewer/agent.md + python-code-review.md
│   ├── architecture-authoring/SKILL.md    # FROM architect/agent.md + architectural-quality.md
│   ├── architecture-review/SKILL.md       # FROM architecture-reviewer/agent.md
│   │
│   │  # -- Existing skills (moved from clasi/skills/) --
│   ├── consolidate-architecture/SKILL.md  # FROM clasi/skills/consolidate-architecture.md
│   ├── self-reflect/SKILL.md              # FROM clasi/skills/self-reflect.md
│   ├── project-knowledge/SKILL.md         # FROM clasi/skills/project-knowledge.md
│   ├── auto-approve/SKILL.md              # FROM clasi/skills/auto-approve.md
│   ├── generate-documentation/SKILL.md    # FROM clasi/skills/generate-documentation.md
│   ├── parallel-execution/SKILL.md        # FROM clasi/skills/parallel-execution.md + worktree-protocol.md
│   ├── report/SKILL.md                    # FROM clasi/skills/report.md
│   └── estimation-rubric/SKILL.md         # FROM clasi/skills/web_app_estimation_rubric.md
│
└── commands/                              # simple flat skills (if any don't need SKILL.md structure)
```

Skills are invoked as `/clasi:se`, `/clasi:plan-sprint`, `/clasi:todo`, etc.

## What stays in `clasi/` Python package (MCP server)

The MCP server remains a Python package providing tools. The plugin bundles it via `.mcp.json`.

- `clasi/tools/artifact_tools.py` — sprint, ticket, TODO CRUD
- `clasi/tools/process_tools.py` — read-only SE process access (list_agents, list_skills, get_instruction, etc.)
- `clasi/hooks/` — Python modules implementing hook logic (testable, importable)
- `clasi/templates/*.md` — used by MCP tools for file scaffolding
- `clasi/instructions/languages/python.md` — served via `get_language_instruction()`
- `clasi/state_db.py` — sprint lifecycle state
- `clasi/cli.py` — `clasi hook <event>` subcommand for hook glue

Removed from MCP server:
- `clasi/tools/dispatch_tools.py` — all `dispatch_to_*` tools eliminated
- `clasi/agent.py` — dispatch/contract logic (or kept for test-time validation only)
- `clasi/dispatch_log.py` — replaced by SubagentStart/SubagentStop hooks

## What gets archived

All 10 absorbed agent directories move to `clasi/agents/archived/` until stable.

## What gets removed

- `clasi/init_command.py` — no more init command; plugin handles installation
- `clasi/skills/*.md` — moved to plugin skills/
- `clasi/rules/*.md` — moved to plugin (or project .claude/rules/ if needed)
- Hardcoded RULES dict, HOOKS_CONFIG dict in init_command.py

## Directory Scopes (Write Permissions)

| Agent | Can write to | Enforced by |
|-------|-------------|-------------|
| **team-lead** | `docs/clasi/` (TODOs, sprint frontmatter, reviews), `.claude/`, `CLAUDE.md` | role-guard hook — allow team-lead writes to `docs/clasi/` |
| **sprint-planner** | `docs/clasi/sprints/<sprint>/` (sprint.md, architecture-update.md, usecases.md, tickets/) | role-guard hook — scope_directory passed in Agent tool prompt |
| **programmer** | Source code, tests, docs within scope_directory passed by team-lead | role-guard hook — worktree isolation provides additional safety |

The scope is documented in:
- **Agent definitions** (plugin `agents/sprint-planner/agent.md`, `agents/programmer/agent.md`)
- **Role guard hook** (`clasi.hooks.on_role_guard()`) — updated for 3-agent model
- **Agent tool prompts / Task descriptions** — team-lead passes scope_directory

## Hooks

All hooks are thin glue registered in `hooks/hooks.json`:

```json
{
  "hooks": {
    "SubagentStart": [{
      "matcher": ".*",
      "hooks": [{ "type": "command", "command": "uv run clasi hook subagent-start" }]
    }],
    "SubagentStop": [{
      "matcher": ".*",
      "hooks": [{ "type": "command", "command": "uv run clasi hook subagent-stop" }]
    }],
    "TaskCreated": [{
      "hooks": [{ "type": "command", "command": "uv run clasi hook task-created" }]
    }],
    "TaskCompleted": [{
      "hooks": [{ "type": "command", "command": "uv run clasi hook task-completed" }]
    }],
    "PreToolUse": [{
      "matcher": "Edit|Write|MultiEdit",
      "hooks": [{ "type": "command", "command": "uv run clasi hook role-guard" }]
    }]
  }
}
```

Each `clasi hook <event>` reads stdin JSON from Claude Code, delegates to `clasi.hooks.on_<event>()`, exits with appropriate code. All logic is in testable Python.

### Dispatch logging (SubagentStart/SubagentStop)

Replaces the old `log_dispatch()`/`update_dispatch_result()` from `Agent.dispatch()`. Writes markdown log files to `docs/clasi/log/`. Works for all agent invocations — native Agent tool, agent teams, ad-hoc — not just MCP dispatches.

### Quality gates (TaskCreated/TaskCompleted)

- `on_task_created()` — verify ticket exists, sprint is in executing phase, ticket not already done
- `on_task_completed()` — run tests, check acceptance criteria, update ticket frontmatter, merge worktree back to sprint branch. Blocks (exit 2) on failure; programmer fixes and retries.

### Write protection (PreToolUse role-guard)

- `on_role_guard()` — enforces directory scopes per agent. Updated error messages for 3-agent model.

## Agent Teams + Tasks for Sprint Execution

### Execution flow

1. **Team-lead reads the sprint tickets** (ordered by dependency)
2. **Creates one Task per ticket** — title is ticket title, description includes ticket file path and scope_directory
3. **Spawns a team of programmer teammates** — each uses the programmer agent definition from plugin `agents/programmer/`
4. **Each programmer claims a task**, gets an isolated worktree branching off the sprint branch, reads the ticket file, implements it
5. **TaskCompleted hook** runs before a task can close (see quality gates above)
6. **Team-lead monitors** via task list, handles any failures
7. **After all tasks complete**, team-lead proceeds to review and close

### Git branching with worktrees

1. **Sprint starts** — create `sprint/NNN-slug` branch off master
2. **Planning** — sprint-planner writes tickets and architecture on the sprint branch
3. **Execution** — each programmer teammate gets a worktree branching off the sprint branch (e.g. `sprint/NNN-slug/ticket-001`)
4. **Ticket completion** — programmer merges worktree branch back to sprint branch, worktree is cleaned up
5. **Sprint close** — sprint branch merges to master via PR

Worktree isolation:
- No conflicts between concurrent programmers (diverge from same base)
- Tests run in isolation
- Failed worktrees preserved for debugging
- Merge conflicts on return to sprint branch: TaskCompleted hook attempts merge, if conflict → blocks completion (exit 2), programmer resolves in its worktree, re-runs tests, retries. Escalate to team-lead only after repeated failures.

### Dependency ordering

- **Task dependencies** — team-lead sets blocking relationships when creating tasks
- **Phased batches** — alternative: create tasks in waves (independent first, then dependent)

## MCP Tools

With skills and agents now native to Claude Code (via the plugin), the MCP process-access tools (`list_skills`, `get_skill_definition`, `list_agents`, `get_agent_definition`, `get_instruction`, `list_instructions`) are likely redundant — Claude Code already discovers plugin skills and agents natively. These can be deprecated or removed.

What stays:
- **Artifact tools** — `create_sprint`, `create_ticket`, `list_todos`, `move_ticket_to_done`, etc. These manage data Claude Code doesn't natively understand.
- **State DB tools** — `get_sprint_phase`, `advance_sprint_phase`, `acquire_execution_lock`, `record_gate_result`, etc. Sprint lifecycle state management.
- **Language instructions** — `get_language_instruction` (project-specific, not plugin content)

## Implementation Phases

### Phase 1: Create plugin structure (non-breaking, additive)
- Create `.claude-plugin/plugin.json` manifest
- Create all ~26 SKILL.md files, rewritten to remove `dispatch_to_*` refs
- Create consolidated agent definitions (sprint-planner, programmer)
- Create `hooks/hooks.json` with all hook registrations
- Create `.mcp.json` bundling the CLASI MCP server
- Old sources remain untouched — both coexist

### Phase 2: Implement hook handlers in Python
- Add `clasi hook <event>` CLI subcommand
- Implement `clasi.hooks.on_subagent_start()`, `on_subagent_stop()`, `on_task_created()`, `on_task_completed()`, `on_role_guard()`
- Write tests for each handler

### Phase 3: Remove MCP dispatch and archive old agents (breaking)
- Remove `clasi/tools/dispatch_tools.py`
- Remove `clasi/agent.py` dispatch logic
- Archive all 12 old agent directories to `clasi/agents/archived/`
- Update MCP tool registration

### Phase 4: Clean up old sources
- Remove `clasi/init_command.py`
- Remove `clasi/skills/*.md`, `clasi/rules/*.md`
- Remove old `clasi/hooks/role_guard.py` (logic now in `clasi/hooks/` modules)
- Remove hardcoded dicts
- Remove `clasi/instructions/` files that moved to plugin (keep languages/)
- Update `pyproject.toml` — remove init entry point, update package-data

### Phase 5: Verify
- `uv run pytest` — all tests pass
- Plugin installs correctly: `/plugin install` from local dir
- Skills appear as `/clasi:se`, `/clasi:todo`, etc.
- MCP artifact tools (create_sprint, create_ticket, etc.) still work
- Hooks fire correctly for SubagentStart/Stop, TaskCreated/Completed, PreToolUse
- Manual walkthrough: `/clasi:se status`, `/clasi:todo`, plan a sprint, execute with agent team

## Key Risks

1. **Plugin agent frontmatter limitations** — plugin agent.md files can't declare `hooks`, `mcpServers`, or `permissionMode` in their frontmatter. Hooks and MCP servers are registered at the plugin level and fire globally; the hook handler code filters by agent when needed (e.g. role-guard checks agent tier). This is fine for our design — just means scoping is done in Python, not in frontmatter.
2. **Hook command resolution** — `uv run clasi hook <event>` must resolve correctly from the plugin context. May need `${CLAUDE_PLUGIN_ROOT}` or require clasi installed in the project's venv.
3. **MCP server bundling** — `.mcp.json` in plugin must correctly launch `uv run clasi mcp`. Test in projects where clasi is not a direct dependency.
4. **Active sprints** — complete or pause before removing dispatch tools.
5. **MCP process tools** — `list_skills`, `list_agents`, `get_instruction`, etc. are likely redundant now. Deprecate or remove.
6. **Agent teams maturity** — agent teams require `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. This is experimental. Have a fallback (serial Agent tool dispatch) if teams aren't stable.
7. **Skill namespacing** — skills become `/clasi:se` instead of `/se`. Update all cross-references in skill content.

## Resolved Questions

- **Programmer context** — comes from the task description. Team-lead includes ticket path, sprint ID, scope_directory, and any relevant doc paths in the Task description. Programmer reads those files. Explicit, no magic.
- **Concurrency control** — team-lead controls how many programmer teammates to spawn.
- **Plugin rules and globs** — need to verify if plugin rules support path-scoped globs like `.claude/rules/` files.

## Installation

The repo is NOT the plugin. The plugin is a subdirectory (`plugin/`) containing the Claude Code plugin content. The `clasi` CLI remains the user-facing entry point.

### Repo structure

```
claude-agent-skills/               # repo root
├── clasi/                         # Python package (MCP server, CLI, hooks)
│   ├── cli.py                     # `clasi init`, `clasi hook <event>`, `clasi mcp`
│   ├── tools/                     # MCP artifact + state tools
│   ├── hooks/                     # Python hook handler logic (testable)
│   └── ...
├── plugin/                        # Claude Code plugin directory
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── agents/
│   ├── skills/
│   ├── hooks/
│   │   └── hooks.json
│   ├── .mcp.json
│   └── settings.json
├── tests/
└── pyproject.toml
```

### `clasi init` supports both installation modes

The `plugin/` directory is the single source of truth. `clasi init` can install it two ways:

**`clasi init [target]`** — project-local mode (default):
1. Copy `plugin/skills/` → `<target>/.claude/skills/`
2. Copy `plugin/agents/` → `<target>/.claude/agents/`
3. Merge `plugin/hooks/hooks.json` into `<target>/.claude/settings.json` hooks section
4. Copy `plugin/.mcp.json` → `<target>/.mcp.json`
5. Set up `docs/clasi/` directories (TODOs, sprints, etc.)
6. Set up MCP permissions in `.claude/settings.local.json`
- Skills are unnamespaced: `/plan-sprint`, `/se`, `/todo`
- Content is in git, visible to the whole team

**`clasi init --plugin`** — plugin mode:
1. Install via Claude Code plugin mechanism (`claude /plugin install <path>`)
2. Set up `docs/clasi/` directories
3. Set up MCP permissions
- Skills are namespaced: `/clasi:plan-sprint`, `/clasi:se`, `/clasi:todo`
- Plugin is global (user-level), not project-specific

Both modes use the same source content. The only differences are:
- Hooks format: `hooks.json` (plugin) vs merged into `settings.json` (.claude/)
- Skill namespacing: `/clasi:X` (plugin) vs `/X` (.claude/)
- Plugin manifest only needed for plugin mode

The plugin directory is bundled with the `clasi` Python package (via pyproject.toml package-data) so `clasi init` can find it at install time.
