#!/usr/bin/env python3
"""
Link Claude agent and skill definitions from this repository into target projects.

This script creates symlinks from a target repository's .github directory to the
agents and skills directories in the claude-agent-skills repository.
"""

import os
import sys
import argparse
from pathlib import Path


def get_source_dir():
    """
    Get the directory containing the agents and skills directories.
    
    For editable installs, this will be the original repository location.
    """
    # The package is installed, so __file__ points to the installed location
    # For editable installs, this will point back to the original source
    package_dir = Path(__file__).parent.resolve()
    
    # Navigate up to the repository root (one level up from claude_agent_skills/)
    repo_root = package_dir.parent
    
    # Verify that .github/agents and .github/skills exist
    github_dir = repo_root / ".github"
    agents_dir = github_dir / "agents"
    skills_dir = github_dir / "skills"
    
    if not github_dir.exists():
        raise RuntimeError(f"Could not find .github directory at {github_dir}")
    if not agents_dir.exists():
        raise RuntimeError(f"Could not find agents directory at {agents_dir}")
    if not skills_dir.exists():
        raise RuntimeError(f"Could not find skills directory at {skills_dir}")
    
    return github_dir


def create_directory_link(source_dir, target_dir, dir_name):
    """
    Create a symlink for a directory (agents or skills).
    
    If the target directory doesn't exist, create a direct symlink.
    If it exists, link individual files from the source into the target.
    """
    source_path = source_dir / dir_name
    target_path = target_dir / dir_name
    
    if not source_path.exists():
        print(f"Warning: Source directory {source_path} does not exist")
        return
    
    # If target doesn't exist, create a direct symlink to the directory
    if not target_path.exists():
        print(f"Creating symlink: {target_path} -> {source_path}")
        target_path.symlink_to(source_path)
        return
    
    # If target exists, link individual files
    print(f"Directory {target_path} already exists, linking individual files...")
    
    # Iterate through all files in the source directory
    for source_file in source_path.rglob("*"):
        if source_file.is_file():
            # Calculate relative path from source_path
            rel_path = source_file.relative_to(source_path)
            target_file = target_path / rel_path
            
            # Create parent directories if needed
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if target file already exists
            if target_file.exists() or target_file.is_symlink():
                # Check if it's already a symlink to our source
                if target_file.is_symlink() and target_file.resolve() == source_file.resolve():
                    print(f"  Already linked: {target_file.name}")
                else:
                    print(f"  Skipping (exists): {rel_path}")
            else:
                print(f"  Linking: {rel_path}")
                target_file.symlink_to(source_file)


def link_agents_and_skills(target_repo):
    """
    Link agents and skills directories from the source repository to the target.
    
    Args:
        target_repo: Path to the target repository (current directory if None)
    """
    # Determine target directory
    if target_repo is None:
        target_repo = Path.cwd()
    else:
        target_repo = Path(target_repo).resolve()
    
    # Verify target has .github directory
    target_github = target_repo / ".github"
    if not target_github.exists():
        print(f"Error: Target directory {target_repo} does not have a .github directory")
        print("This script should be run in a repository with a .github directory")
        sys.exit(1)
    
    # Get source directory
    try:
        source_github = get_source_dir()
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    print(f"Source: {source_github}")
    print(f"Target: {target_github}")
    print()
    
    # Link agents directory
    create_directory_link(source_github, target_github, "agents")
    print()
    
    # Link skills directory
    create_directory_link(source_github, target_github, "skills")
    print()
    
    print("Done! Agent and skill definitions are now linked.")


def main():
    """Main entry point for the link-claude-agents command."""
    parser = argparse.ArgumentParser(
        description="Link Claude agent and skill definitions into the current repository"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Target repository path (defaults to current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
        print()
    
    try:
        link_agents_and_skills(args.target)
    except KeyboardInterrupt:
        print("\nAborted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
