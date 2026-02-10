"""CLASI MCP server — stdio transport.

Provides SE Process Access and Artifact Management tools via MCP.
"""

from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Create the MCP server instance
server = FastMCP(
    "clasi",
    instructions=(
        "CLASI — Claude Agent Skills Instructions. "
        "Provides SE process access tools (agents, skills, instructions) "
        "and artifact management tools (sprints, tickets, briefs)."
    ),
)


def get_repo_root() -> Path:
    """Locate the repository root containing agents/, skills/, instructions/.

    For editable installs, this is the original repository location.
    """
    package_dir = Path(__file__).parent.resolve()
    repo_root = package_dir.parent

    if not (repo_root / "agents").exists():
        raise RuntimeError(f"Could not find agents directory at {repo_root / 'agents'}")
    if not (repo_root / "skills").exists():
        raise RuntimeError(f"Could not find skills directory at {repo_root / 'skills'}")

    return repo_root


def run_server() -> None:
    """Start the CLASI MCP server (stdio transport)."""
    # Import tool modules to register their tools with the server
    import claude_agent_skills.process_tools  # noqa: F401
    import claude_agent_skills.artifact_tools  # noqa: F401

    server.run(transport="stdio")
