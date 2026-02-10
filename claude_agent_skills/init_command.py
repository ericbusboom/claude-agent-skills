"""Implementation of the `clasi init` command."""

import click


def run_init(target: str, *, global_config: bool = False) -> None:
    """Initialize a repository for the CLASI SE process.

    Placeholder — full implementation in ticket 004.
    """
    click.echo(f"clasi init: target={target}, global={global_config}")
    click.echo("Not yet implemented.")
