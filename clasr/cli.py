"""clasr CLI entry point.

Provides:
  clasr --instructions        Print bundled instructions and exit.
  clasr install               (stub) Install asr/ to target platforms.
  clasr uninstall             (stub) Uninstall a provider from target platforms.
"""

from __future__ import annotations

import argparse
import importlib.resources
import sys


def _print_instructions() -> None:
    """Load and print clasr/instructions.md via importlib.resources."""
    package_ref = importlib.resources.files("clasr")
    instructions_file = package_ref / "instructions.md"
    content = instructions_file.read_text(encoding="utf-8")
    print(content, end="")


def _validate_platform_flags(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    """Exit with an error if no platform flag (--claude, --codex, --copilot) was given."""
    if not (args.claude or args.codex or args.copilot):
        parser.error("at least one of --claude, --codex, --copilot is required")


def _validate_required_flag(
    args: argparse.Namespace,
    flag: str,
    parser: argparse.ArgumentParser,
) -> None:
    """Exit with an error if a required named flag is missing."""
    if not getattr(args, flag, None):
        parser.error(f"--{flag} is required")


def _cmd_install(args: argparse.Namespace, install_parser: argparse.ArgumentParser) -> int:
    """Stub install subcommand — dispatches to platform stubs."""
    _validate_required_flag(args, "source", install_parser)
    _validate_required_flag(args, "provider", install_parser)
    _validate_platform_flags(args, install_parser)
    print("not yet implemented (ticket 011)")
    return 0


def _cmd_uninstall(args: argparse.Namespace, uninstall_parser: argparse.ArgumentParser) -> int:
    """Stub uninstall subcommand — dispatches to platform stubs."""
    _validate_required_flag(args, "provider", uninstall_parser)
    _validate_platform_flags(args, uninstall_parser)
    print("not yet implemented (ticket 011)")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Entry point for the clasr CLI."""
    parser = argparse.ArgumentParser(
        prog="clasr",
        description=(
            "clasr — cross-platform agent-config renderer. "
            "Renders an asr/ source directory into platform-specific agent config installs."
        ),
    )
    parser.add_argument(
        "--instructions",
        action="store_true",
        default=False,
        help="Print bundled usage instructions and exit.",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="command")

    # install subcommand (stub)
    install_parser = subparsers.add_parser(
        "install",
        help="Install an asr/ source directory into one or more platforms.",
    )
    install_parser.add_argument(
        "--source",
        metavar="PATH",
        help="Path to the asr/ source directory (required).",
    )
    install_parser.add_argument(
        "--provider",
        metavar="NAME",
        help="Provider name (used to namespace installed files; required).",
    )
    install_parser.add_argument(
        "--target",
        metavar="PATH",
        default=".",
        help="Target project root directory (default: current directory).",
    )
    install_parser.add_argument(
        "--claude",
        action="store_true",
        default=False,
        help="Install to the Claude platform (.claude/).",
    )
    install_parser.add_argument(
        "--codex",
        action="store_true",
        default=False,
        help="Install to the Codex platform (.codex/).",
    )
    install_parser.add_argument(
        "--copilot",
        action="store_true",
        default=False,
        help="Install to the Copilot platform (.github/).",
    )
    install_parser.add_argument(
        "--copy",
        action="store_true",
        default=False,
        help="Use file copies instead of symlinks.",
    )

    # uninstall subcommand (stub)
    uninstall_parser = subparsers.add_parser(
        "uninstall",
        help="Uninstall a provider from one or more platforms.",
    )
    uninstall_parser.add_argument(
        "--provider",
        metavar="NAME",
        help="Provider name to uninstall (required).",
    )
    uninstall_parser.add_argument(
        "--target",
        metavar="PATH",
        default=".",
        help="Target project root directory (default: current directory).",
    )
    uninstall_parser.add_argument(
        "--claude",
        action="store_true",
        default=False,
        help="Uninstall from the Claude platform.",
    )
    uninstall_parser.add_argument(
        "--codex",
        action="store_true",
        default=False,
        help="Uninstall from the Codex platform.",
    )
    uninstall_parser.add_argument(
        "--copilot",
        action="store_true",
        default=False,
        help="Uninstall from the Copilot platform.",
    )

    args = parser.parse_args(argv)

    if args.instructions:
        _print_instructions()
        return 0

    if args.command == "install":
        return _cmd_install(args, install_parser)

    if args.command == "uninstall":
        return _cmd_uninstall(args, uninstall_parser)

    # No subcommand given — print help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
