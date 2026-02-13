"""Implementation of the `clasi init` command.

Writes instruction files and configures the MCP server in a target
repository.
"""

import json
from pathlib import Path

import click

# Package root for reading bundled content files (rules, etc.).
_PACKAGE_ROOT = Path(__file__).parent.resolve()

MCP_CONFIG = {
    "clasi": {
        "command": "clasi",
        "args": ["mcp"],
    }
}

# Thin skill stubs that delegate to MCP for real instructions.
# Each key is the subdirectory name under .claude/skills/<name>/SKILL.md.
AGENTS_MD_CONTENT = """\
# CLASI Software Engineering Process

This project uses the **CLASI** (Claude Agent Skills Instructions)
software engineering process, managed via an MCP server.

## How It Works

All work follows a structured lifecycle. The MCP server (`clasi`)
provides tools, skills, and instructions that guide you through each
step. When in doubt, call `get_se_overview()` for the full process map.

## What To Do

### Starting a new project

Run the project initiation interview to produce a project overview:

```
get_skill_definition("project-initiation")
```

### Planning a sprint

Create a sprint with planning documents, use cases, and a technical plan:

```
get_skill_definition("plan-sprint")
```

### Working on a ticket

Execute a ticket through the full lifecycle (plan, implement, test, review):

```
get_skill_definition("execute-ticket")
```

### Closing a sprint

Verify all tickets are done, merge, archive, and tag a release:

```
get_skill_definition("close-sprint")
```

### Checking project status

See where the project stands — active sprints, tickets, and next actions:

```
get_skill_definition("project-status")
```

### Reporting a bug with the tools

File an issue against the CLASI tools themselves:

```
get_skill_definition("report")
```

## MCP Tools Quick Reference

| Tool | Purpose |
|------|---------|
| `get_se_overview()` | Full process overview |
| `get_activity_guide(activity)` | Guidance for a specific activity |
| `get_skill_definition(name)` | Load a skill's full instructions |
| `get_agent_definition(name)` | Load an agent definition |
| `get_instruction(name)` | Load a process instruction file |
| `create_sprint(title)` | Create a new sprint |
| `create_ticket(sprint_id, title)` | Create a ticket in a sprint |
| `list_sprints()` / `list_tickets()` | List sprints and tickets |

## Key Principle

**The SE process is the default.** When asked to build a feature, fix a
bug, or make any code change, follow this process unless the stakeholder
explicitly says "out of process" or "direct change".
"""

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
    "project-initiation": """\
---
description: Start a new project with a guided interview
---

# /project-initiation

To execute this skill, call the CLASI MCP tool
`get_skill_definition("project-initiation")` to retrieve the full
instructions, then follow them.
""",
    "report": """\
---
description: Report a bug or issue with CLASI tools
---

# /report

To execute this skill, call the CLASI MCP tool
`get_skill_definition("report")` to retrieve the full instructions,
then follow them.
""",
    "ghtodo": """\
---
description: Create a GitHub issue from user input
---

# /ghtodo

To execute this skill, call the CLASI MCP tool
`get_skill_definition("ghtodo")` to retrieve the full instructions,
then follow them.
""",
}


def _write_rule_file(target: Path, rule_name: str, dest_dir: str) -> bool:
    """Read a rule from the package and write it to the target project.

    Args:
        target: Target project root.
        rule_name: Filename of the rule (e.g., "clasi-se-process.md").
        dest_dir: Destination directory relative to target (e.g., ".claude/rules").

    Returns True if the file was written/updated, False if unchanged.
    """
    source = _PACKAGE_ROOT / "rules" / rule_name
    content = source.read_text(encoding="utf-8")

    rel_path = f"{dest_dir}/{rule_name}"
    path = target / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and path.read_text(encoding="utf-8") == content:
        click.echo(f"  Unchanged: {rel_path}")
        return False

    path.write_text(content, encoding="utf-8")
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


SETTINGS_PERMISSIONS = {
    "permissions": {
        "allow": [
            "mcp__clasi__*",
        ]
    }
}


def _update_settings_json(settings_path: Path) -> bool:
    """Merge MCP permission allowlist into .claude/settings.local.json.

    Returns True if the file was written/updated, False if unchanged.
    """
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    rel = str(settings_path.relative_to(settings_path.parent.parent.parent))

    if settings_path.exists():
        try:
            data = json.loads(settings_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            data = {}
    else:
        data = {}

    permissions = data.setdefault("permissions", {})
    allow = permissions.setdefault("allow", [])

    target_perm = "mcp__clasi__*"
    if target_perm in allow:
        click.echo(f"  Unchanged: {rel}")
        return False

    allow.append(target_perm)
    settings_path.write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    click.echo(f"  Updated: {rel}")
    return True


def run_init(target: str) -> None:
    """Initialize a repository for the CLASI SE process.

    Writes instruction files and configures the MCP server.
    """
    target_path = Path(target).resolve()
    click.echo(f"Initializing CLASI in {target_path}")
    click.echo()

    # Write AGENTS.md at project root
    click.echo("AGENTS.md:")
    agents_md = target_path / "AGENTS.md"
    if agents_md.exists() and agents_md.read_text(encoding="utf-8") == AGENTS_MD_CONTENT:
        click.echo("  Unchanged: AGENTS.md")
    else:
        agents_md.write_text(AGENTS_MD_CONTENT, encoding="utf-8")
        click.echo("  Wrote: AGENTS.md")
    click.echo()

    # Install rule files from the package into .claude/rules/
    rules_dir = _PACKAGE_ROOT / "rules"
    rule_files = sorted(rules_dir.glob("*.md"))

    click.echo("Rule files:")
    for rule_path in rule_files:
        _write_rule_file(target_path, rule_path.name, ".claude/rules")
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

    # Create .codex symlink to .claude for ChatGPT Codex
    click.echo("Codex symlink:")
    codex_link = target_path / ".codex"
    if codex_link.is_symlink():
        if codex_link.resolve() == (target_path / ".claude").resolve():
            click.echo("  Unchanged: .codex -> .claude")
        else:
            click.echo(f"  Warning: .codex points to {codex_link.readlink()}, skipping")
    elif codex_link.exists():
        click.echo("  Warning: .codex exists as file/directory, skipping")
    else:
        codex_link.symlink_to(".claude")
        click.echo("  Created: .codex -> .claude")
    click.echo()

    # Configure MCP permissions in .claude/settings.local.json
    click.echo("MCP permissions:")
    settings_json = target_path / ".claude" / "settings.local.json"
    _update_settings_json(settings_json)

    click.echo()
    click.echo("Done! The CLASI SE process is now configured.")
