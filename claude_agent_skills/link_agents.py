#!/usr/bin/env python3
"""
Link agent and skill definitions from this repository into target projects.

This script creates symlinks from a target repository for both GitHub Copilot
(.github/copilot/) and Claude Code (.claude/), adapting the layout to each
tool's expected directory structure.

Source layout (this repo):
    agents/<name>.md
    skills/<name>.md

Copilot target layout:
    .github/copilot/agents/  ->  <source>/agents/
    .github/copilot/skills/  ->  <source>/skills/

Claude Code target layout:
    .claude/agents/           ->  <source>/agents/
    .claude/skills/<name>/SKILL.md  ->  <source>/skills/<name>.md
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

    agents_dir = repo_root / "agents"
    skills_dir = repo_root / "skills"

    if not agents_dir.exists():
        raise RuntimeError(f"Could not find agents directory at {agents_dir}")
    if not skills_dir.exists():
        raise RuntimeError(f"Could not find skills directory at {skills_dir}")

    return repo_root


def link_directory(source_path, target_path, dry_run=False):
    """
    Create a directory symlink from target_path -> source_path.

    If target_path already exists as a symlink pointing to source_path, skip.
    If target_path already exists as something else, warn and skip.
    """
    if target_path.is_symlink():
        if target_path.resolve() == source_path.resolve():
            print(f"  Already linked: {target_path}")
            return
        else:
            print(f"  Replacing stale symlink: {target_path}")
            if not dry_run:
                target_path.unlink()

    if target_path.exists():
        print(f"  Skipping (already exists): {target_path}")
        return

    print(f"  Linking: {target_path} -> {source_path}")
    if not dry_run:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.symlink_to(source_path)


def link_file(source_file, target_file, dry_run=False):
    """
    Create a file symlink from target_file -> source_file.

    If target_file already exists as a symlink pointing to source_file, skip.
    If target_file already exists as something else, warn and skip.
    """
    if target_file.is_symlink():
        if target_file.resolve() == source_file.resolve():
            print(f"  Already linked: {target_file}")
            return
        else:
            print(f"  Replacing stale symlink: {target_file}")
            if not dry_run:
                target_file.unlink()

    if target_file.exists():
        print(f"  Skipping (already exists): {target_file}")
        return

    print(f"  Linking: {target_file} -> {source_file}")
    if not dry_run:
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.symlink_to(source_file)


def link_claude_skills(source_skills_dir, target_claude_dir, dry_run=False):
    """
    Link skills for Claude Code, which expects:
        .claude/skills/<skill-name>/SKILL.md

    Each <source>/skills/<name>.md becomes:
        <target>/.claude/skills/<name>/SKILL.md  ->  <source>/skills/<name>.md
    """
    target_skills = target_claude_dir / "skills"

    # If skills is a stale directory symlink (from an older version of this
    # script), remove it so we can create per-skill subdirectories instead.
    if target_skills.is_symlink():
        print(f"  Removing stale directory symlink: {target_skills}")
        if not dry_run:
            target_skills.unlink()

    for source_file in sorted(source_skills_dir.glob("*.md")):
        skill_name = source_file.stem
        target_file = target_skills / skill_name / "SKILL.md"
        link_file(source_file, target_file, dry_run)


def link_agents_and_skills(target_repo, dry_run=False):
    """
    Link agents and skills from this repository into the target.
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

    source_agents = repo_root / "agents"
    source_skills = repo_root / "skills"

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
    link_claude_skills(source_skills, claude_dir, dry_run)
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
