---
status: draft
---

# Sprint 001 Technical Plan

## Architecture Overview

The `claude-agent-skills` package is restructured from a symlink-based
distribution tool into an MCP server with a CLI frontend. The package
provides two entry points:

```
clasi init [--global] [target]    # Initialize a repo for CLASI
clasi mcp                         # Run the MCP server (stdio)
```

The MCP server exposes two tool groups: SE Process Access (read-only,
serves content from the installed package) and Artifact Management
(read-write, operates on `docs/plans/` in the working directory).

## Package Structure

```
claude-agent-skills/
├── agents/                        # Agent definitions (served via MCP)
├── skills/                        # Skill definitions (served via MCP)
├── instructions/                  # Instructions (served via MCP)
├── docs/plans/                    # SE artifacts for THIS project
├── claude_agent_skills/
│   ├── __init__.py
│   ├── cli.py                     # CLI entry point (clasi)
│   ├── init_command.py            # clasi init implementation
│   ├── mcp_server.py              # MCP server implementation
│   ├── process_tools.py           # SE Process Access MCP tools
│   ├── artifact_tools.py          # Artifact Management MCP tools
│   ├── templates.py               # Artifact templates
│   └── frontmatter.py             # YAML frontmatter parsing/editing
└── pyproject.toml
```

## Technology Stack

- Python 3.10+ (bump from 3.7 — needed for MCP SDK)
- `mcp` — Model Context Protocol Python SDK
- `pyyaml` — YAML frontmatter parsing
- `click` — CLI framework (replaces argparse for subcommand support)

## Component Design

### Component: CLI (`cli.py`)

**Use Cases**: SUC-001

Entry point registered as `clasi` in pyproject.toml. Uses `click` for
subcommand routing:

```python
@click.group()
def cli(): ...

@cli.command()
@click.option('--global', 'global_config', is_flag=True)
@click.argument('target', default='.')
def init(target, global_config): ...

@cli.command()
def mcp(): ...
```

### Component: Init Command (`init_command.py`)

**Use Cases**: SUC-001

Writes two things:

1. **Instruction files** — Markdown files placed in:
   - `.claude/rules/clasi-se-process.md` — For Claude Code
   - `.github/copilot/instructions/clasi-se-process.md` — For Copilot

   Content: High-level SE process overview with a table mapping activities
   to MCP tool names. Stable across MCP server updates.

2. **MCP server configuration** — JSON merged into `.claude/settings.json`:
   ```json
   {
     "mcpServers": {
       "clasi": {
         "command": "clasi",
         "args": ["mcp"]
       }
     }
   }
   ```
   With `--global`, also updates `~/.claude/settings.json`.

Idempotency: checks if instruction file and MCP config already exist
before writing. Updates if content has changed, skips if identical.

### Component: MCP Server (`mcp_server.py`)

**Use Cases**: SUC-002, SUC-003, SUC-004, SUC-005, SUC-006, SUC-007

Stdio-based MCP server using the `mcp` Python SDK. Registers tools from
`process_tools.py` and `artifact_tools.py`. Locates the source repo
(agents, skills, instructions) using the same `get_repo_root()` approach.

### Component: SE Process Access Tools (`process_tools.py`)

**Use Cases**: SUC-002

Read-only tools that serve content from the installed package:

| Tool | Description | Returns |
|------|-------------|---------|
| `get_se_overview` | High-level SE process description | Markdown text |
| `get_activity_guide(activity)` | Tailored guidance for a specific activity | Markdown text |
| `list_agents` | List all agent definitions | JSON array of {name, description} |
| `list_skills` | List all skill definitions | JSON array of {name, description} |
| `list_instructions` | List all instruction files | JSON array of {name, description} |
| `get_agent_definition(name)` | Full agent markdown | Markdown text |
| `get_skill_definition(name)` | Full skill markdown | Markdown text |
| `get_instruction(name)` | Full instruction markdown | Markdown text |

The `get_se_overview` tool returns a curated overview (not just the raw
system-engineering.md). It should summarize the process stages, list
available agents with one-line descriptions, list skills with one-line
descriptions, and explain when to use each MCP tool.

The `get_activity_guide(activity)` tool returns tailored guidance for a
specific activity, combining the relevant agent definition, skill workflow,
and instruction content into a single response. Activities include:
`requirements`, `architecture`, `ticketing`, `implementation`, `testing`,
`code-review`, `sprint-planning`, `sprint-closing`. This saves the LLM
from having to call multiple tools to assemble context for a given task.

### Component: Artifact Management Tools (`artifact_tools.py`)

**Use Cases**: SUC-003, SUC-004, SUC-005, SUC-006, SUC-007

Read-write tools that operate on `docs/plans/` relative to cwd:

| Tool | Description | Returns |
|------|-------------|---------|
| `create_sprint(title)` | Create sprint dir with templates | {id, path, branch, files} |
| `create_ticket(sprint_id, title)` | Create ticket in sprint | {id, path, template} |
| `create_brief()` | Create top-level brief | {path, template} |
| `create_technical_plan()` | Create top-level technical plan | {path, template} |
| `create_use_cases()` | Create top-level use cases | {path, template} |
| `list_sprints(status?)` | List sprints | [{id, title, status, path}] |
| `list_tickets(sprint_id?, status?)` | List tickets | [{id, title, status, sprint, path}] |
| `get_sprint_status(sprint_id)` | Sprint summary | {id, title, status, tickets: {todo, in_progress, done}} |
| `update_ticket_status(path, status)` | Update frontmatter | {path, old_status, new_status} |
| `move_ticket_to_done(path)` | Move ticket + plan to done/ | {old_path, new_path} |
| `close_sprint(sprint_id)` | Move sprint dir to done/ | {old_path, new_path} |

### Component: Templates (`templates.py`)

**Use Cases**: SUC-003, SUC-004, SUC-007

Python module containing template strings for each artifact type:

- `SPRINT_TEMPLATE` — Sprint document with frontmatter + sections
- `SPRINT_BRIEF_TEMPLATE` — Sprint-level brief
- `SPRINT_USECASES_TEMPLATE` — Sprint-level use cases
- `SPRINT_TECHNICAL_PLAN_TEMPLATE` — Sprint-level technical plan
- `TICKET_TEMPLATE` — Ticket with frontmatter + sections
- `BRIEF_TEMPLATE` — Top-level brief
- `TECHNICAL_PLAN_TEMPLATE` — Top-level technical plan
- `USE_CASES_TEMPLATE` — Top-level use cases

Templates use Python string formatting for dynamic values (id, title, etc.).

### Component: Frontmatter Parser (`frontmatter.py`)

**Use Cases**: SUC-005, SUC-006

Utility for reading and writing YAML frontmatter in markdown files:

- `read_frontmatter(path)` → dict
- `write_frontmatter(path, data)` — Updates frontmatter, preserves body
- `read_document(path)` → (frontmatter_dict, body_str)

Uses `pyyaml` for YAML parsing. Handles the `---` delimiters.

### Component: pyproject.toml Updates

- Rename entry point: `clasi = "claude_agent_skills.cli:cli"`
- Remove old entry point: `link-claude-agents`
- Add dependencies: `mcp`, `pyyaml`, `click`
- Bump `requires-python` to `>=3.10`

## Sprint Directory Structure

Each sprint is a directory under `docs/plans/sprints/`:

```
docs/plans/sprints/
├── 001-mcp-server/
│   ├── sprint.md
│   ├── brief.md
│   ├── usecases.md
│   ├── technical-plan.md
│   └── tickets/
│       ├── 001-setup-cli.md
│       ├── 001-setup-cli-plan.md
│       └── done/
│           └── ...
└── done/
    └── ...  (completed sprint directories)
```

Ticket numbering is per-sprint (starts at 001 within each sprint).

## Artifact Frontmatter Schemas

**Sprint** (`sprint.md`):
```yaml
id: "NNN"
title: string
status: planning | active | done
branch: sprint/NNN-slug
use-cases: [UC-XXX, ...]
```

**Ticket** (within sprint):
```yaml
id: "NNN"
title: string
status: todo | in-progress | done
use-cases: [SUC-XXX, ...]
depends-on: ["NNN", ...]
```

**Brief, Technical Plan, Use Cases**:
```yaml
status: draft | approved
```

## Resolved Decisions

- **Activity guide tool**: Yes — `get_activity_guide(activity)` included.
  Combines agent + skill + instruction into one curated response per activity.
- **Old tickets (001-034)**: Move into a retroactive sprint 000. Create
  `docs/plans/sprints/done/000-initial-setup/` and move the old
  `docs/plans/tickets/` contents there. This unifies everything under the
  sprint-directory model.
- **Init instruction file**: Single file (`clasi-se-process.md`) with
  overview + MCP tool reference table. Placed in both `.claude/rules/` and
  `.github/copilot/instructions/`.

## Open Questions

- Should `clasi init` also create a `.gitignore` entry for any CLASI-
  generated files?
