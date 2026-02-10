#!/usr/bin/env python3
"""
Link agent and skill definitions from this repository into target projects.

This script creates directory symlinks from a target repository into the
agents and skills directories in this repository, for both GitHub Copilot
(.github/copilot/) and Claude Code (.claude/).
"""

import sys
import argparse
from pathlib import Path


def get_repo_root():
    """
    Get the repository root containing the source agents and skills.

    For editable installs, this will be the original repository location.
    """
    package_dir = Path(__file__).parent.resolve()
    repo_root = package_dir.parent

    copilot_dir = repo_root / ".github" / "copilot"
    if not copilot_dir.exists():
        raise RuntimeError(f"Could not find .github/copilot directory at {copilot_dir}")
    if not (copilot_dir / "agents").exists():
        raise RuntimeError(f"Could not find agents directory at {copilot_dir / 'agents'}")
    if not (copilot_dir / "skills").exists():
        raise RuntimeError(f"Could not find skills directory at {copilot_dir / 'skills'}")

    return repo_root


def link_directory(source_path, target_path, dry_run=False):
    """
    Create a directory symlink from target_path -> source_path.

    If target_path already exists as a symlink pointing to source_path, skip.
    If target_path already exists as something else, warn and skip.
    """
    if target_path.is_symlink():
        if target_path.resolve() == source_path.resolve():
            print(f"  Already linked: {target_path} -> {source_path}")
            return
        else:
            print(f"  Skipping (symlink exists to different target): {target_path}")
            return

    if target_path.exists():
        print(f"  Skipping (already exists): {target_path}")
        return

    print(f"  Linking: {target_path} -> {source_path}")
    if not dry_run:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.symlink_to(source_path)


def link_agents_and_skills(target_repo, dry_run=False):
    """
    Link agents and skills directories from the source repository to the target.

    Creates symlinks for both GitHub Copilot and Claude Code:
      - <target>/.github/copilot/agents -> <source>/.github/copilot/agents
      - <target>/.github/copilot/skills -> <source>/.github/copilot/skills
      - <target>/.claude/agents         -> <source>/.github/copilot/agents
      - <target>/.claude/skills         -> <source>/.github/copilot/skills
    """
    if target_repo is None:
        target_repo = Path.cwd()
    else:
        target_repo = Path(target_repo).resolve()

    try:
        repo_root = get_repo_root()
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    source_agents = repo_root / ".github" / "copilot" / "agents"
    source_skills = repo_root / ".github" / "copilot" / "skills"

    print(f"Source repo: {repo_root}")
    print(f"Target repo: {target_repo}")
    print()

    # --- GitHub Copilot ---
    print("GitHub Copilot (.github/copilot/):")
    copilot_dir = target_repo / ".github" / "copilot"
    if not copilot_dir.exists() and not dry_run:
        copilot_dir.mkdir(parents=True, exist_ok=True)
    link_directory(source_agents, copilot_dir / "agents", dry_run)
    link_directory(source_skills, copilot_dir / "skills", dry_run)
    print()

    # --- Claude Code ---
    print("Claude Code (.claude/):")
    claude_dir = target_repo / ".claude"
    if not claude_dir.exists() and not dry_run:
        claude_dir.mkdir(parents=True, exist_ok=True)
    link_directory(source_agents, claude_dir / "agents", dry_run)
    link_directory(source_skills, claude_dir / "skills", dry_run)
    print()

    print("Done! Agent and skill definitions are now linked.")


def main():
    """Main entry point for the link-claude-agents command."""
    parser = argparse.ArgumentParser(
        description="Link agent and skill definitions into the current repository"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Target repository path (defaults to current directory)",
    )
    parser.add_argument(
        "-N",
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
        print()

    try:
        link_agents_and_skills(args.target, args.dry_run)
    except KeyboardInterrupt:
        print("\nAborted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
