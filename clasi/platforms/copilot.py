"""GitHub Copilot platform installer and uninstaller for CLASI.

Handles all Copilot-specific file operations:
- Creating .github/skills/ as a symlink (or copy) to .agents/skills/
- Writing .github/copilot-instructions.md with the CLASI section (ticket 007)
- Writing .github/instructions/<n>.instructions.md path-rule files (ticket 008)
- Writing .github/agents/<n>.agent.md sub-agent files (ticket 009)
- Merging .vscode/mcp.json with the CLASI server entry (ticket 010)

Public interface::

    install(target: Path, mcp_config: dict, copy: bool = False, migrate: bool = False) -> None
    uninstall(target: Path, copy: bool = False) -> None

Neither function knows about shared scaffolding (TODO dirs, log dir, .mcp.json).
Those remain in init_command.py.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import click

from clasi.platforms import _links
from clasi.platforms import _markers  # noqa: F401 — imported for future stubs
from clasi.platforms import _rules  # noqa: F401 — imported for future stubs

# The plugin directory is bundled inside the clasi package.
_PLUGIN_DIR = Path(__file__).parent.parent / "plugin"


# ---------------------------------------------------------------------------
# Canonical skills writer
# ---------------------------------------------------------------------------


def _ensure_canonical_skills(target: Path) -> None:
    """Write plugin skills to .agents/skills/<n>/SKILL.md (idempotent).

    Copies each bundled SKILL.md to the canonical location only if the file
    does not already exist with matching content.  This means Claude or Codex
    installers that already wrote the canonical files are not disturbed.
    """
    plugin_skills = _PLUGIN_DIR / "skills"
    if not plugin_skills.exists():
        click.echo("  Warning: plugin/skills/ not found, skipping canonical skills write")
        return

    agents_skills = target / ".agents" / "skills"
    for skill_dir in sorted(plugin_skills.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_src = skill_dir / "SKILL.md"
        if not skill_src.exists():
            continue

        dest_dir = agents_skills / skill_dir.name
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / "SKILL.md"

        src_content = skill_src.read_text(encoding="utf-8")
        if dest.exists() and dest.read_text(encoding="utf-8") == src_content:
            # Already up to date — idempotent no-op
            continue

        shutil.copy2(skill_src, dest)
        click.echo(f"  Wrote: .agents/skills/{skill_dir.name}/SKILL.md")


# ---------------------------------------------------------------------------
# .github/skills/ symlink (or copy) — fully implemented here (not a stub)
# ---------------------------------------------------------------------------


def _install_skills(target: Path, copy: bool = False) -> None:
    """Create .github/skills/ as a directory-level alias for .agents/skills/.

    1. Ensures the canonical .agents/skills/ directory and its contents exist.
    2. Creates .github/skills/ -> .agents/skills/ via _links.link_or_copy.
       With copy=False (default), this is a directory symlink.
       With copy=True, the entire directory tree is copied (shutil.copytree).

    Idempotent: an existing symlink pointing at the correct target is replaced
    (removed then re-created) to handle stale symlinks on re-install.
    """
    _ensure_canonical_skills(target)

    agents_skills = target / ".agents" / "skills"
    github_skills = target / ".github" / "skills"

    # Ensure .agents/skills/ exists even if there are no plugin skills
    agents_skills.mkdir(parents=True, exist_ok=True)

    # Remove stale alias if present
    if github_skills.is_symlink() or github_skills.exists():
        if github_skills.is_symlink():
            github_skills.unlink()
        else:
            # It's a real directory — do not delete; leave it and skip
            click.echo(
                "  Warning: .github/skills/ exists as a real directory; "
                "skipping alias creation"
            )
            return

    github_skills.parent.mkdir(parents=True, exist_ok=True)

    if copy:
        shutil.copytree(agents_skills, github_skills)
        click.echo("  Copied: .github/skills/ <- .agents/skills/")
    else:
        import os
        try:
            os.symlink(agents_skills, github_skills)
            click.echo("  Symlinked: .github/skills/ -> .agents/skills/")
        except OSError as exc:
            import warnings
            warnings.warn(
                f"symlink({agents_skills!r} -> {github_skills!r}) failed ({exc}); "
                "falling back to copytree.",
                stacklevel=2,
            )
            shutil.copytree(agents_skills, github_skills)
            click.echo("  Copied (fallback): .github/skills/ <- .agents/skills/")


def _uninstall_skills(target: Path) -> None:
    """Remove the .github/skills/ alias (symlink or copy directory).

    Only the alias is removed; the canonical .agents/skills/ is preserved.
    """
    github_skills = target / ".github" / "skills"
    if github_skills.is_symlink():
        github_skills.unlink()
        click.echo("  Removed: .github/skills/ (symlink)")
    elif github_skills.exists():
        shutil.rmtree(github_skills)
        click.echo("  Removed: .github/skills/ (copy directory)")
    else:
        click.echo("  Skipped: .github/skills/ (not found)")


# ---------------------------------------------------------------------------
# Stubs — filled in by subsequent tickets
# ---------------------------------------------------------------------------


def _install_global_instructions(target: Path, copy: bool = False) -> None:
    """Write .github/copilot-instructions.md with the CLASI marker section.

    Stub — implemented in ticket 007.
    """
    # TODO(013-007): write .github/copilot-instructions.md using
    #   _markers.write_section with the CLASI entry-point and global rules.
    click.echo("  [stub] .github/copilot-instructions.md (ticket 007)")


def _uninstall_global_instructions(target: Path) -> None:
    """Remove the CLASI block from .github/copilot-instructions.md.

    Stub — implemented in ticket 007.
    """
    # TODO(013-007): strip the CLASI marker block from
    #   .github/copilot-instructions.md.
    click.echo("  [stub] uninstall .github/copilot-instructions.md (ticket 007)")


def _install_path_rules(target: Path) -> None:
    """Write .github/instructions/<n>.instructions.md path-rule files.

    Stub — implemented in ticket 008.
    """
    # TODO(013-008): write one .instructions.md file per CLASI rule using
    #   YAML frontmatter with applyTo field and body from _rules.py constants.
    click.echo("  [stub] .github/instructions/ (ticket 008)")


def _uninstall_path_rules(target: Path) -> None:
    """Remove CLASI .instructions.md files from .github/instructions/.

    Stub — implemented in ticket 008.
    """
    # TODO(013-008): remove the CLASI-owned .instructions.md files by name.
    click.echo("  [stub] uninstall .github/instructions/ (ticket 008)")


def _install_agents(target: Path, copy: bool = False) -> None:
    """Write .github/agents/<n>.agent.md for each active CLASI agent.

    Stub — implemented in ticket 009.
    """
    # TODO(013-009): write .github/agents/<name>.agent.md from
    #   plugin/agents/<name>/agent.md, transforming frontmatter to Copilot
    #   schema (description required; drop Claude-specific fields).
    click.echo("  [stub] .github/agents/ (ticket 009)")


def _uninstall_agents(target: Path) -> None:
    """Remove CLASI .agent.md files from .github/agents/.

    Stub — implemented in ticket 009.
    """
    # TODO(013-009): remove each CLASI-owned .agent.md by name; rmdir
    #   .github/agents/ if empty.
    click.echo("  [stub] uninstall .github/agents/ (ticket 009)")


def _install_vscode_mcp(target: Path, mcp_config: dict) -> None:
    """Merge the CLASI server entry into .vscode/mcp.json.

    Stub — implemented in ticket 010.
    """
    # TODO(013-010): create or merge .vscode/mcp.json with
    #   {"servers": {"clasi": mcp_config}}.  Parse-fail guard: log error and
    #   skip; never overwrite user content.
    click.echo("  [stub] .vscode/mcp.json (ticket 010)")


def _uninstall_vscode_mcp(target: Path) -> None:
    """Remove the CLASI entry from .vscode/mcp.json.

    Stub — implemented in ticket 010.
    """
    # TODO(013-010): remove servers.clasi from .vscode/mcp.json; delete the
    #   key but preserve the rest of the file.
    click.echo("  [stub] uninstall .vscode/mcp.json (ticket 010)")


def _print_cloud_mcp_notice(mcp_config: dict) -> None:
    """Print a post-install notice for cloud MCP configuration.

    Stub — implemented in ticket 010 or as a standalone note.
    """
    # TODO(013-010): emit a clear post-install message explaining that
    #   cloud Copilot Coding Agent cannot commit MCP config and the user
    #   must configure it manually in the GitHub Copilot settings UI.
    click.echo("  [stub] cloud MCP notice (ticket 010)")


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------


def install(
    target: Path,
    mcp_config: dict,
    copy: bool = False,
    migrate: bool = False,
) -> None:
    """Install the GitHub Copilot platform integration into *target*.

    Performs the Copilot-specific steps in order:
    1. Write canonical .agents/skills/ content and create .github/skills/ alias.
    2. Write .github/copilot-instructions.md (stub; ticket 007).
    3. Write .github/instructions/<n>.instructions.md (stub; ticket 008).
    4. Write .github/agents/<n>.agent.md (stub; ticket 009).
    5. Merge .vscode/mcp.json (stub; ticket 010).
    6. Print cloud MCP notice (stub; ticket 010).

    Shared scaffolding (TODO dirs, log dir, .mcp.json) is handled by the
    caller (init_command.run_init).

    Args:
        target: Resolved Path to the target project root.
        mcp_config: The MCP server command dict (written into .vscode/mcp.json
            under servers.clasi in ticket 010).
        copy: If True, use file copy instead of symlink for alias operations.
            Passed through to ``_links.link_or_copy`` and ``_install_skills``.
        migrate: If True, convert legacy direct-copy installs to symlinks.
            Accepted for forward-compatibility; wired in a later ticket.
            Currently a no-op.
    """
    click.echo("GitHub Copilot:")
    click.echo()

    click.echo("Skills:")
    _install_skills(target, copy=copy)
    click.echo()

    click.echo("Global instructions:")
    _install_global_instructions(target, copy=copy)
    click.echo()

    click.echo("Path rules:")
    _install_path_rules(target)
    click.echo()

    click.echo("Agents:")
    _install_agents(target, copy=copy)
    click.echo()

    click.echo("VS Code MCP:")
    _install_vscode_mcp(target, mcp_config)
    click.echo()

    click.echo("Cloud MCP notice:")
    _print_cloud_mcp_notice(mcp_config)
    click.echo()


def uninstall(target: Path, copy: bool = False) -> None:
    """Remove the GitHub Copilot platform integration from *target*.

    Reverses each Copilot-managed artifact:
    - Removes the .github/skills/ alias (symlink or copy); canonical
      .agents/skills/ is preserved.
    - Removes the CLASI block from .github/copilot-instructions.md (stub; 007).
    - Removes .github/instructions/ CLASI files (stub; ticket 008).
    - Removes .github/agents/ CLASI files (stub; ticket 009).
    - Removes servers.clasi from .vscode/mcp.json (stub; ticket 010).

    This function is non-destructive toward user-added files: only
    CLASI-owned sections and entries are removed.

    Args:
        target: Resolved Path to the target project root.
        copy: If True, alias removal uses file-copy semantics.  ``unlink_alias``
            handles both symlinks and regular files uniformly; this flag is
            accepted for CLI parity with ``clasi uninstall --copy``.
    """
    click.echo(f"Uninstalling GitHub Copilot platform integration from {target}")
    click.echo()

    click.echo("Skills:")
    _uninstall_skills(target)
    click.echo()

    click.echo("Global instructions:")
    _uninstall_global_instructions(target)
    click.echo()

    click.echo("Path rules:")
    _uninstall_path_rules(target)
    click.echo()

    click.echo("Agents:")
    _uninstall_agents(target)
    click.echo()

    click.echo("VS Code MCP:")
    _uninstall_vscode_mcp(target)
    click.echo()

    click.echo()
    click.echo("Done! GitHub Copilot platform integration removed.")
