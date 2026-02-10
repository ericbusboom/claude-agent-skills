"""
CLI entry point for clasi (Claude Agent Skills Instructions).

Subcommands:
    clasi init [--global] [target]  — Initialize a repo for CLASI
    clasi mcp                       — Run the MCP server (stdio)
"""

import click


@click.group()
@click.version_option(package_name="claude-agent-skills")
def cli():
    """CLASI — Claude Agent Skills Instructions.

    MCP server for AI-driven software engineering process.
    """


@cli.command()
@click.option(
    "--global",
    "global_config",
    is_flag=True,
    help="Also add MCP server config to global Claude settings (~/.claude/settings.json)",
)
@click.argument("target", default=".", type=click.Path(exists=True))
def init(target, global_config):
    """Initialize a repository for the CLASI SE process.

    Writes instruction files and configures the MCP server in the target
    directory (defaults to current directory).
    """
    from claude_agent_skills.init_command import run_init

    run_init(target, global_config=global_config)


@cli.command()
def mcp():
    """Run the CLASI MCP server (stdio transport)."""
    from claude_agent_skills.mcp_server import run_server

    run_server()
