"""SE Process Access tools for the CLASI MCP server.

Read-only tools that serve agent, skill, and instruction content
from the installed package.
"""

import json
from pathlib import Path

from claude_agent_skills.frontmatter import read_document
from claude_agent_skills.mcp_server import server, get_repo_root


def _list_definitions(directory: Path) -> list[dict[str, str]]:
    """List all .md files in a directory, returning name and description from frontmatter."""
    results = []
    if not directory.exists():
        return results
    for path in sorted(directory.glob("*.md")):
        fm, _ = read_document(path)
        results.append({
            "name": fm.get("name", path.stem),
            "description": fm.get("description", ""),
        })
    return results


def _get_definition(directory: Path, name: str) -> str:
    """Read the full content of a named .md file from a directory."""
    path = directory / f"{name}.md"
    if not path.exists():
        available = [p.stem for p in sorted(directory.glob("*.md"))]
        raise ValueError(
            f"'{name}' not found in {directory.name}/. "
            f"Available: {', '.join(available)}"
        )
    return path.read_text(encoding="utf-8")


@server.tool()
def get_se_overview() -> str:
    """Get a curated overview of the CLASI SE process.

    Returns a summary of the process stages, available agents and skills,
    and guidance on which MCP tools to use for each activity.
    """
    root = get_repo_root()
    agents = _list_definitions(root / "agents")
    skills = _list_definitions(root / "skills")
    instructions = _list_definitions(root / "instructions")

    agent_lines = "\n".join(
        f"- **{a['name']}**: {a['description']}" for a in agents
    )
    skill_lines = "\n".join(
        f"- **{s['name']}**: {s['description']}" for s in skills
    )
    instruction_lines = "\n".join(
        f"- **{i['name']}**: {i['description']}" for i in instructions
    )

    return f"""# CLASI SE Process Overview

## Process Stages

1. **Stage 1a — Requirements**: Elicit requirements, produce brief and use cases
   - Skill: `elicit-requirements` | Agent: `requirements-analyst`
2. **Stage 1b — Architecture**: Design architecture, produce technical plan
   - Skill: `create-technical-plan` | Agent: `architect`
3. **Sprints**: Organize work into sprint directories with planning docs and tickets
   - Skills: `plan-sprint`, `close-sprint` | Agent: `project-manager`
4. **Stage 2 — Ticketing**: Break plan into numbered tickets
   - Skill: `create-tickets` | Agent: `systems-engineer`
5. **Stage 3 — Implementation**: Execute tickets (plan → implement → test → review → done)
   - Skill: `execute-ticket` | Agents: `python-expert`, `code-reviewer`, `documentation-expert`

## Available Agents

{agent_lines}

## Available Skills

{skill_lines}

## Available Instructions

{instruction_lines}

## MCP Tools Quick Reference

### SE Process Access (this tool group)
- `get_se_overview()` — This overview
- `get_activity_guide(activity)` — Tailored guidance for a specific activity
- `list_agents()` / `get_agent_definition(name)` — Agent definitions
- `list_skills()` / `get_skill_definition(name)` — Skill definitions
- `list_instructions()` / `get_instruction(name)` — Instruction files

### Artifact Management
- `create_sprint(title)` / `list_sprints()` / `get_sprint_status(sprint_id)` — Sprint management
- `create_ticket(sprint_id, title)` / `list_tickets()` — Ticket management
- `update_ticket_status(path, status)` / `move_ticket_to_done(path)` — Ticket lifecycle
- `close_sprint(sprint_id)` — Sprint closure
- `create_brief()` / `create_technical_plan()` / `create_use_cases()` — Top-level artifacts
"""


@server.tool()
def list_agents() -> str:
    """List all available agent definitions.

    Returns a JSON array of objects with 'name' and 'description' fields.
    """
    root = get_repo_root()
    return json.dumps(_list_definitions(root / "agents"), indent=2)


@server.tool()
def list_skills() -> str:
    """List all available skill definitions.

    Returns a JSON array of objects with 'name' and 'description' fields.
    """
    root = get_repo_root()
    return json.dumps(_list_definitions(root / "skills"), indent=2)


@server.tool()
def list_instructions() -> str:
    """List all available instruction files.

    Returns a JSON array of objects with 'name' and 'description' fields.
    """
    root = get_repo_root()
    return json.dumps(_list_definitions(root / "instructions"), indent=2)


@server.tool()
def get_agent_definition(name: str) -> str:
    """Get the full markdown content of a named agent definition.

    Args:
        name: The agent name (e.g., 'project-manager', 'python-expert')
    """
    root = get_repo_root()
    return _get_definition(root / "agents", name)


@server.tool()
def get_skill_definition(name: str) -> str:
    """Get the full markdown content of a named skill definition.

    Args:
        name: The skill name (e.g., 'execute-ticket', 'plan-sprint')
    """
    root = get_repo_root()
    return _get_definition(root / "skills", name)


@server.tool()
def get_instruction(name: str) -> str:
    """Get the full markdown content of a named instruction file.

    Args:
        name: The instruction name (e.g., 'system-engineering', 'coding-standards')
    """
    root = get_repo_root()
    return _get_definition(root / "instructions", name)


# Activity guide configuration: maps activity names to their relevant
# agent, skill, and instruction files.
ACTIVITY_GUIDES: dict[str, dict[str, list[str]]] = {
    "requirements": {
        "agents": ["requirements-analyst"],
        "skills": ["elicit-requirements"],
        "instructions": ["system-engineering"],
    },
    "architecture": {
        "agents": ["architect"],
        "skills": ["create-technical-plan"],
        "instructions": ["system-engineering"],
    },
    "ticketing": {
        "agents": ["systems-engineer"],
        "skills": ["create-tickets"],
        "instructions": ["system-engineering"],
    },
    "implementation": {
        "agents": ["python-expert", "systems-engineer"],
        "skills": ["execute-ticket"],
        "instructions": ["system-engineering", "coding-standards", "testing", "git-workflow"],
    },
    "testing": {
        "agents": ["python-expert"],
        "skills": ["execute-ticket"],
        "instructions": ["testing", "coding-standards"],
    },
    "code-review": {
        "agents": ["code-reviewer"],
        "skills": ["execute-ticket"],
        "instructions": ["coding-standards", "testing"],
    },
    "sprint-planning": {
        "agents": ["project-manager", "architecture-reviewer"],
        "skills": ["plan-sprint"],
        "instructions": ["system-engineering", "git-workflow"],
    },
    "sprint-closing": {
        "agents": ["project-manager"],
        "skills": ["close-sprint"],
        "instructions": ["system-engineering", "git-workflow"],
    },
}


@server.tool()
def get_activity_guide(activity: str) -> str:
    """Get tailored guidance for a specific SE activity.

    Combines the relevant agent definition(s), skill workflow, and
    instruction content into a single curated response.

    Args:
        activity: One of: requirements, architecture, ticketing,
            implementation, testing, code-review, sprint-planning,
            sprint-closing
    """
    if activity not in ACTIVITY_GUIDES:
        available = ", ".join(sorted(ACTIVITY_GUIDES.keys()))
        raise ValueError(
            f"Unknown activity '{activity}'. "
            f"Available activities: {available}"
        )

    guide = ACTIVITY_GUIDES[activity]
    root = get_repo_root()
    sections = []

    sections.append(f"# Activity Guide: {activity}\n")

    # Agent definitions
    for agent_name in guide["agents"]:
        content = _get_definition(root / "agents", agent_name)
        sections.append(f"## Agent: {agent_name}\n\n{content}")

    # Skill workflows
    for skill_name in guide["skills"]:
        content = _get_definition(root / "skills", skill_name)
        sections.append(f"## Skill: {skill_name}\n\n{content}")

    # Instructions
    for instr_name in guide["instructions"]:
        content = _get_definition(root / "instructions", instr_name)
        sections.append(f"## Instruction: {instr_name}\n\n{content}")

    return "\n\n---\n\n".join(sections)
