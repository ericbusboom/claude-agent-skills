"""
CLI entry point for clasi (Claude Agent Skills Instructions).

Subcommands:
    clasi init [target]             — Initialize a repo for CLASI
    clasi mcp                       — Run the MCP server (stdio)
    clasi todo-split                — Split multi-heading TODO files
"""

import click


@click.group()
@click.version_option(package_name="claude-agent-skills")
def cli():
    """CLASI — Claude Agent Skills Instructions.

    MCP server for AI-driven software engineering process.
    """


@cli.command()
@click.argument("target", default=".", type=click.Path(exists=True))
def init(target):
    """Initialize a repository for the CLASI SE process.

    Writes instruction files and configures the MCP server in the target
    directory (defaults to current directory).
    """
    from claude_agent_skills.init_command import run_init

    run_init(target)


@cli.command("todo-split")
@click.argument("todo_dir", default="docs/plans/todo", type=click.Path(exists=True))
def todo_split(todo_dir):
    """Split multi-heading TODO files into individual files.

    Scans the TODO directory for markdown files with multiple level-1
    headings and splits each into a separate file.
    """
    from pathlib import Path

    from claude_agent_skills.todo_split import split_todo_files

    actions = split_todo_files(Path(todo_dir))
    if actions:
        click.echo("TODO split results:")
        for action in actions:
            click.echo(action)
    else:
        click.echo("No files needed splitting.")


@cli.command()
def mcp():
    """Run the CLASI MCP server (stdio transport)."""
    from claude_agent_skills.mcp_server import run_server

    run_server()
