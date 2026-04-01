"""
CLI entry point for CLASI.

Subcommands:
    clasi init [target]             — Initialize a repo for CLASI
    clasi mcp                       — Run the MCP server (stdio)
    clasi todo-split                — Split multi-heading TODO files
    clasi version                   — Show the current project version
    clasi version bump              — Bump version, update files, tag
"""

import click


@click.group()
@click.version_option(package_name="clasi")
def cli():
    """CLASI.

    MCP server for AI-driven software engineering process.
    """


@cli.command()
@click.argument("target", default=".", type=click.Path(exists=True))
@click.option("--plugin", is_flag=True, help="Install as a Claude Code plugin instead of project-local .claude/ content.")
def init(target, plugin):
    """Initialize a repository for the CLASI SE process.

    By default, copies skills, agents, and hooks into the project's
    .claude/ directory (project-local mode). With --plugin, registers
    the CLASI plugin with Claude Code (plugin mode).
    """
    from clasi.init_command import run_init

    run_init(target, plugin_mode=plugin)


@cli.command("todo-split")
@click.argument("todo_dir", default="docs/clasi/todo", type=click.Path(exists=True))
def todo_split(todo_dir):
    """Split multi-heading TODO files into individual files.

    Scans the TODO directory for markdown files with multiple level-1
    headings and splits each into a separate file.
    """
    from pathlib import Path

    from clasi.todo_split import split_todo_files

    actions = split_todo_files(Path(todo_dir))
    if actions:
        click.echo("TODO split results:")
        for action in actions:
            click.echo(action)
    else:
        click.echo("No files needed splitting.")


@cli.group(invoke_without_command=True)
@click.pass_context
def version(ctx):
    """Show or bump the project version.

    With no subcommand, shows the current version.
    """
    if ctx.invoked_subcommand is None:
        from clasi.versioning import read_current_version

        ver = read_current_version()
        if ver:
            click.echo(ver)
        else:
            click.echo("No version file found.", err=True)
            ctx.exit(1)


@version.command(name="bump")
@click.option("--major", default=0, type=int, help="Major version number.")
@click.option("--no-tag", is_flag=True, help="Skip creating a git tag.")
def version_bump(major, no_tag):
    """Compute the next version, update version files, and tag.

    Reads version_format from settings to determine the format.
    Updates the source file and all sync files, then creates a git tag.
    """
    from clasi.versioning import bump_version

    result = bump_version(major=major, tag=not no_tag)
    click.echo(f"Version: {result['version']}")
    if result["source"]:
        click.echo(f"Updated: {result['source']}")
    for s in result["synced"]:
        click.echo(f"Synced:  {s}")
    if result["tag"]:
        click.echo(f"Tagged:  {result['tag']}")


@cli.command()
def mcp():
    """Run the CLASI MCP server (stdio transport)."""
    from clasi.mcp_server import run_server

    run_server()


@cli.command()
@click.argument(
    "event",
    type=click.Choice(
        [
            "role-guard",
            "subagent-start",
            "subagent-stop",
            "task-created",
            "task-completed",
        ]
    ),
)
def hook(event):
    """Handle a Claude Code hook event.

    Reads hook payload from stdin (JSON), delegates to the appropriate
    handler in clasi.hooks, and exits with the correct code.
    """
    from clasi.hook_handlers import handle_hook

    handle_hook(event)
