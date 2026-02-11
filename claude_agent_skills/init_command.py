"""Implementation of the `clasi init` command.

Writes instruction files and configures the MCP server in a target
repository.
"""

import json
from pathlib import Path

import click

# Embedded instruction file content — stable overview of SE process with
# MCP tool reference.
INSTRUCTION_CONTENT = """\
# CLASI SE Process

This project uses the CLASI (Claude Agent Skills Instructions) software
engineering process, served via MCP tools.

## Process Overview

The SE process has four stages:

1. **Stage 1a — Requirements**: Elicit requirements, produce brief and use cases
2. **Stage 1b — Architecture**: Produce technical plan from brief and use cases
3. **Stage 2 — Ticketing**: Break technical plan into actionable tickets
4. **Stage 3 — Implementation**: Execute tickets in sprints

Work is organized into **sprints** — each sprint is a directory containing
planning documents and tickets.

## MCP Tools Reference

Use these MCP tools (provided by the `clasi` server) to interact with the
SE process:

### SE Process Access

| Tool | Description |
|------|-------------|
| `get_se_overview` | High-level SE process description |
| `get_activity_guide(activity)` | Tailored guidance for an activity |
| `list_agents` | List available agent definitions |
| `list_skills` | List available skill definitions |
| `list_instructions` | List available instruction files |
| `get_agent_definition(name)` | Full agent definition |
| `get_skill_definition(name)` | Full skill definition |
| `get_instruction(name)` | Full instruction content |

### Artifact Management

| Tool | Description |
|------|-------------|
| `create_overview()` | Create project overview document |
| `create_sprint(title)` | Create a new sprint directory |
| `create_ticket(sprint_id, title)` | Create a ticket in a sprint |
| `list_sprints(status?)` | List sprints |
| `list_tickets(sprint_id?, status?)` | List tickets |
| `get_sprint_status(sprint_id)` | Sprint summary with ticket counts |
| `update_ticket_status(path, status)` | Update ticket status |
| `move_ticket_to_done(path)` | Move completed ticket to done/ |
| `close_sprint(sprint_id)` | Close and archive a sprint |

## Getting Started

1. Use `get_se_overview` to understand the full process
2. Use `get_activity_guide("requirements")` when starting a new project
3. Use `create_sprint(title)` to begin a new sprint
"""

MCP_CONFIG = {
    "clasi": {
        "command": "clasi",
        "args": ["mcp"],
    }
}

# Thin skill stubs that delegate to MCP for real instructions.
# Each key is the subdirectory name under .claude/skills/<name>/SKILL.md.
SKILL_STUBS = {
    "todo": """\
---
description: Create a TODO file from user input
---

# /todo

To execute this skill, call the CLASI MCP tool `get_skill_definition("todo")`
to retrieve the full instructions, then follow them.
""",
    "next": """\
---
description: Determine and execute the next process step
---

# /next

To execute this skill, call the CLASI MCP tool `get_skill_definition("next")`
to retrieve the full instructions, then follow them.
""",
    "status": """\
---
description: Run project status report
---

# /status

To execute this skill, call the CLASI MCP tool
`get_skill_definition("project-status")` to retrieve the full instructions,
then follow them.
""",
}


def _write_instruction_file(target: Path, rel_path: str) -> bool:
    """Write the instruction file at the given relative path.

    Returns True if the file was written/updated, False if unchanged.
    """
    path = target / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and path.read_text(encoding="utf-8") == INSTRUCTION_CONTENT:
        click.echo(f"  Unchanged: {rel_path}")
        return False

    path.write_text(INSTRUCTION_CONTENT, encoding="utf-8")
    click.echo(f"  Wrote: {rel_path}")
    return True


def _write_skill_stub(target: Path, name: str, content: str) -> bool:
    """Write a skill stub to .claude/skills/<name>/SKILL.md.

    Returns True if the file was written/updated, False if unchanged.
    """
    path = target / ".claude" / "skills" / name / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    rel = f".claude/skills/{name}/SKILL.md"

    if path.exists() and path.read_text(encoding="utf-8") == content:
        click.echo(f"  Unchanged: {rel}")
        return False

    path.write_text(content, encoding="utf-8")
    click.echo(f"  Wrote: {rel}")
    return True


def _update_mcp_json(mcp_json_path: Path) -> bool:
    """Merge MCP server config into .mcp.json.

    Returns True if the file was written/updated, False if unchanged.
    """
    if mcp_json_path.exists():
        try:
            data = json.loads(mcp_json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            data = {}
    else:
        data = {}

    mcp_servers = data.setdefault("mcpServers", {})

    if mcp_servers.get("clasi") == MCP_CONFIG["clasi"]:
        click.echo(f"  Unchanged: {mcp_json_path}")
        return False

    mcp_servers["clasi"] = MCP_CONFIG["clasi"]
    mcp_json_path.write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    click.echo(f"  Updated: {mcp_json_path}")
    return True


def run_init(target: str) -> None:
    """Initialize a repository for the CLASI SE process.

    Writes instruction files and configures the MCP server.
    """
    target_path = Path(target).resolve()
    click.echo(f"Initializing CLASI in {target_path}")
    click.echo()

    # Write instruction files
    click.echo("Instruction files:")
    _write_instruction_file(target_path, ".claude/rules/clasi-se-process.md")
    _write_instruction_file(
        target_path, ".github/copilot/instructions/clasi-se-process.md"
    )
    click.echo()

    # Install skill stubs
    click.echo("Skill stubs:")
    for filename, content in SKILL_STUBS.items():
        _write_skill_stub(target_path, filename, content)
    click.echo()

    # Configure MCP server in .mcp.json at project root
    click.echo("MCP server configuration:")
    mcp_json = target_path / ".mcp.json"
    _update_mcp_json(mcp_json)

    click.echo()
    click.echo("Done! The CLASI SE process is now configured.")
