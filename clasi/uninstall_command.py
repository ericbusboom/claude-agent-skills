"""Implementation of the `clasi uninstall` command.

Removes CLASI-managed platform integration files from a target repository.
Supports --claude and --codex flags to select which platform(s) to uninstall.

In interactive mode (no flag, TTY), inspects what is installed and prompts
the user to choose.

In non-interactive mode (no flag), exits with a clear error requiring an
explicit flag.

Public interface::

    run_uninstall(target: str, claude: bool, codex: bool) -> None
"""

import sys
from pathlib import Path

import click


def _prompt_uninstall(target: Path) -> str:
    """Inspect installed CLASI platform files and prompt the user.

    Uses detect_platforms() to determine which platforms are installed,
    then presents a numbered menu.  Returns one of "claude", "codex", "both".
    """
    from clasi.platforms.detect import detect_platforms

    signals = detect_platforms(target)

    has_claude = signals.claude_score > 0
    has_codex = signals.codex_score > 0

    if has_claude and has_codex:
        options = [
            ("1", "Claude only", "claude"),
            ("2", "Codex only", "codex"),
            ("3", "Both", "both"),
        ]
    elif has_claude:
        options = [
            ("1", "Claude", "claude"),
        ]
    elif has_codex:
        options = [
            ("1", "Codex", "codex"),
        ]
    else:
        # No CLASI artifacts detected; offer both anyway so the user can
        # still request a clean-up.
        options = [
            ("1", "Claude only", "claude"),
            ("2", "Codex only", "codex"),
            ("3", "Both", "both"),
        ]

    click.echo("Uninstall CLASI platform integration:")
    for num, label, _ in options:
        click.echo(f"  [{num}] {label}")

    valid_nums = {o[0] for o in options}
    while True:
        choice = click.prompt("Choice", type=str).strip()
        for num, _label, value in options:
            if choice == num:
                return value
        click.echo(
            f"Invalid choice. Enter one of: {', '.join(n for n, _, _ in options)}"
        )


def run_uninstall(
    target: str,
    claude: bool = False,
    codex: bool = False,
    copy: bool = False,
) -> None:
    """Remove CLASI platform integration files from *target*.

    Parameters
    ----------
    target:
        Path to the target project directory.
    claude:
        If True, run the Claude platform uninstaller.
    codex:
        If True, run the Codex platform uninstaller.
    copy:
        If True, alias operations use file-copy removal semantics.
        In practice ``_links.unlink_alias`` handles both symlinks and
        regular files identically, so this flag is surfaced for parity
        with ``clasi init --copy`` and passed through to the uninstallers.
    """
    target_path = Path(target).resolve()
    interactive = sys.stdin.isatty() and sys.stdout.isatty()

    if not claude and not codex:
        if interactive:
            choice = _prompt_uninstall(target_path)
            claude = choice in ("claude", "both")
            codex = choice in ("codex", "both")
        else:
            click.echo(
                "Error: specify --claude, --codex, or --claude --codex.", err=True
            )
            raise SystemExit(1)

    if claude:
        from clasi.platforms.claude import uninstall as claude_uninstall
        claude_uninstall(target_path, copy=copy)

    if codex:
        from clasi.platforms.codex import uninstall as codex_uninstall
        codex_uninstall(target_path, copy=copy)
