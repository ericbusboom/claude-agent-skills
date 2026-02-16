"""Implementation of the `clasi init` command.

Installs the CLASI SE process into a target repository with minimal
footprint: one skill stub, one AGENTS.md section, MCP config, and
permissions. Does not take over existing files.
"""

import json
from pathlib import Path

import click

MCP_CONFIG = {
    "clasi": {
        "command": "clasi",
        "args": ["mcp"],
    }
}

SE_SKILL_STUB = """\
---
description: CLASI Software Engineering process dispatcher
---

# /se

Dispatch to the CLASI SE process. Call the appropriate CLASI MCP tool
based on the argument provided.

## Usage

- `/se` or `/se status` — Run project status report
- `/se next` — Determine and execute the next process step
- `/se todo <description>` — Create a TODO file
- `/se init` — Start a new project with guided interview
- `/se report` — Report a bug with CLASI tools
- `/se ghtodo <description>` — Create a GitHub issue

## How to execute

Parse the argument after `/se` and call the matching MCP tool:

| Argument | MCP call |
|----------|----------|
| *(none)* or `status` | `get_skill_definition("project-status")` |
| `next` | `get_skill_definition("next")` |
| `todo` | `get_skill_definition("todo")` |
| `init` | `get_skill_definition("project-initiation")` |
| `report` | `get_skill_definition("report")` |
| `ghtodo` | `get_skill_definition("ghtodo")` |

Pass any remaining text after the subcommand as the argument to the
skill (e.g., `/se todo fix the login bug` passes "fix the login bug"
to the todo skill).

For general SE process guidance, call `get_se_overview()`.
"""

# Marker used to find/replace the CLASI section in AGENTS.md.
_AGENTS_SECTION_START = "<!-- CLASI:START -->"
_AGENTS_SECTION_END = "<!-- CLASI:END -->"

AGENTS_MD_SECTION = f"""\
{_AGENTS_SECTION_START}
## CLASI Software Engineering Process

This project uses the **CLASI** (Claude Agent Skills Instructions)
software engineering process, managed via an MCP server.

**The SE process is the default.** When asked to build a feature, fix a
bug, or make any code change, follow this process unless the stakeholder
explicitly says "out of process" or "direct change".

### Process

Work flows through four stages organized into sprints:

1. **Requirements** — Elicit requirements, produce overview and use cases
2. **Architecture** — Produce technical plan
3. **Ticketing** — Break plan into actionable tickets
4. **Implementation** — Execute tickets

Use `/se` or call `get_se_overview()` for full process details and MCP
tool reference.

### Stakeholder Corrections

When the stakeholder corrects your behavior or expresses frustration
("that's wrong", "why did you do X?", "I told you to..."):

1. Acknowledge the correction immediately.
2. Run `get_skill_definition("self-reflect")` to produce a structured
   reflection in `docs/plans/reflections/`.
3. Continue with the corrected approach.

Do NOT trigger on simple clarifications, new instructions, or questions
about your reasoning.
{_AGENTS_SECTION_END}"""


def _write_se_skill(target: Path) -> bool:
    """Write the /se skill stub to .claude/skills/se/SKILL.md.

    Returns True if the file was written/updated, False if unchanged.
    """
    path = target / ".claude" / "skills" / "se" / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    rel = ".claude/skills/se/SKILL.md"

    if path.exists() and path.read_text(encoding="utf-8") == SE_SKILL_STUB:
        click.echo(f"  Unchanged: {rel}")
        return False

    path.write_text(SE_SKILL_STUB, encoding="utf-8")
    click.echo(f"  Wrote: {rel}")
    return True


def _update_agents_md(target: Path) -> bool:
    """Append or update the CLASI section in AGENTS.md.

    If AGENTS.md doesn't exist, creates it with just the CLASI section.
    If it exists but has no CLASI section, appends the section.
    If it exists with a CLASI section, replaces it in place.

    Returns True if the file was written/updated, False if unchanged.
    """
    agents_md = target / "AGENTS.md"

    if agents_md.exists():
        content = agents_md.read_text(encoding="utf-8")

        if _AGENTS_SECTION_START in content and _AGENTS_SECTION_END in content:
            # Replace existing CLASI section in place
            start_idx = content.index(_AGENTS_SECTION_START)
            end_idx = content.index(_AGENTS_SECTION_END) + len(_AGENTS_SECTION_END)
            new_content = content[:start_idx] + AGENTS_MD_SECTION + content[end_idx:]
        else:
            # Append to existing content
            if not content.endswith("\n"):
                content += "\n"
            new_content = content + "\n" + AGENTS_MD_SECTION + "\n"

        if new_content == content:
            click.echo("  Unchanged: AGENTS.md")
            return False

        agents_md.write_text(new_content, encoding="utf-8")
        click.echo("  Updated: AGENTS.md")
        return True
    else:
        agents_md.write_text(AGENTS_MD_SECTION + "\n", encoding="utf-8")
        click.echo("  Created: AGENTS.md")
        return True


VSCODE_MCP_CONFIG = {
    "clasi": {
        "type": "stdio",
        "command": "clasi",
        "args": ["mcp"],
    }
}


def _update_mcp_json(mcp_json_path: Path) -> bool:
    """Merge MCP server config into .mcp.json.

    Returns True if the file was written/updated, False if unchanged.
    """
    rel = str(mcp_json_path.name)

    if mcp_json_path.exists():
        try:
            data = json.loads(mcp_json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            data = {}
    else:
        data = {}

    mcp_servers = data.setdefault("mcpServers", {})

    if mcp_servers.get("clasi") == MCP_CONFIG["clasi"]:
        click.echo(f"  Unchanged: {rel}")
        return False

    mcp_servers["clasi"] = MCP_CONFIG["clasi"]
    mcp_json_path.write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    click.echo(f"  Updated: {rel}")
    return True


def _update_vscode_mcp_json(target: Path) -> bool:
    """Merge MCP server config into .vscode/mcp.json.

    Uses the VS Code format (servers key with type field).
    Returns True if the file was written/updated, False if unchanged.
    """
    vscode_dir = target / ".vscode"
    mcp_json_path = vscode_dir / "mcp.json"
    rel = ".vscode/mcp.json"

    if mcp_json_path.exists():
        try:
            data = json.loads(mcp_json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            data = {}
    else:
        data = {}

    servers = data.setdefault("servers", {})

    if servers.get("clasi") == VSCODE_MCP_CONFIG["clasi"]:
        click.echo(f"  Unchanged: {rel}")
        return False

    vscode_dir.mkdir(parents=True, exist_ok=True)
    servers["clasi"] = VSCODE_MCP_CONFIG["clasi"]
    mcp_json_path.write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    click.echo(f"  Updated: {rel}")
    return True


def _update_settings_json(settings_path: Path) -> bool:
    """Add mcp__clasi__* to the permissions allowlist in settings.local.json.

    Only adds the single permission entry; does not overwrite other settings.
    Creates the file if it doesn't exist.
    Returns True if the file was written/updated, False if unchanged.
    """
    settings_path.parent.mkdir(parents=True, exist_ok=True)

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
        click.echo("  Unchanged: .claude/settings.local.json")
        return False

    allow.append(target_perm)
    settings_path.write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    click.echo("  Updated: .claude/settings.local.json")
    return True


def run_init(target: str) -> None:
    """Initialize a repository for the CLASI SE process.

    Writes the /se skill stub, appends CLASI section to AGENTS.md,
    and configures the MCP server.
    """
    target_path = Path(target).resolve()
    click.echo(f"Initializing CLASI in {target_path}")
    click.echo()

    # Install the /se skill dispatcher
    click.echo("Skill stub:")
    _write_se_skill(target_path)
    click.echo()

    # Append CLASI section to AGENTS.md
    click.echo("AGENTS.md:")
    _update_agents_md(target_path)
    click.echo()

    # Configure MCP server in .mcp.json at project root
    click.echo("MCP server configuration:")
    _update_mcp_json(target_path / ".mcp.json")
    _update_vscode_mcp_json(target_path)
    click.echo()

    # Add MCP permission to .claude/settings.local.json
    click.echo("MCP permissions:")
    settings_json = target_path / ".claude" / "settings.local.json"
    _update_settings_json(settings_json)

    click.echo()
    click.echo("Done! The CLASI SE process is now configured.")
