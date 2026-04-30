"""
tests/unit/test_platform_copilot.py

Minimal tests for clasi/platforms/copilot.py.

Expanded by tickets 007-010 as each stub is implemented.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from clasi.platforms import copilot


# ---------------------------------------------------------------------------
# install() — smoke test and .github/skills/ alias
# ---------------------------------------------------------------------------


def test_install_runs_without_error(tmp_path: Path) -> None:
    """install() must complete without raising an exception."""
    copilot.install(tmp_path, mcp_config={})


def test_install_creates_github_skills_symlink(tmp_path: Path) -> None:
    """install() must create .github/skills/ as a symlink to .agents/skills/."""
    copilot.install(tmp_path, mcp_config={})

    github_skills = tmp_path / ".github" / "skills"
    assert github_skills.is_symlink(), ".github/skills/ should be a symlink"
    assert github_skills.resolve() == (tmp_path / ".agents" / "skills").resolve()


def test_install_creates_agents_skills_canonical(tmp_path: Path) -> None:
    """install() must write canonical skill files under .agents/skills/."""
    copilot.install(tmp_path, mcp_config={})

    agents_skills = tmp_path / ".agents" / "skills"
    assert agents_skills.is_dir(), ".agents/skills/ should be a directory"


def test_install_github_skills_is_directory_via_symlink(tmp_path: Path) -> None:
    """The .github/skills/ symlink must resolve to an actual directory."""
    copilot.install(tmp_path, mcp_config={})

    github_skills = tmp_path / ".github" / "skills"
    assert github_skills.is_dir(), ".github/skills/ should resolve to a directory"


def test_install_copy_mode_creates_directory_not_symlink(tmp_path: Path) -> None:
    """With copy=True, .github/skills/ should be a real directory, not a symlink."""
    copilot.install(tmp_path, mcp_config={}, copy=True)

    github_skills = tmp_path / ".github" / "skills"
    assert github_skills.exists(), ".github/skills/ should exist"
    assert not github_skills.is_symlink(), (
        "With copy=True, .github/skills/ should not be a symlink"
    )
    assert github_skills.is_dir(), ".github/skills/ should be a directory"


def test_install_idempotent_symlink(tmp_path: Path) -> None:
    """Calling install() twice must not raise an error (idempotent)."""
    copilot.install(tmp_path, mcp_config={})
    copilot.install(tmp_path, mcp_config={})  # second call should be fine

    github_skills = tmp_path / ".github" / "skills"
    assert github_skills.is_symlink()


# ---------------------------------------------------------------------------
# uninstall() — smoke test and alias removal
# ---------------------------------------------------------------------------


def test_uninstall_runs_without_error(tmp_path: Path) -> None:
    """uninstall() must complete without raising an exception."""
    copilot.install(tmp_path, mcp_config={})
    copilot.uninstall(tmp_path)


def test_uninstall_removes_github_skills_alias(tmp_path: Path) -> None:
    """uninstall() must remove the .github/skills/ alias."""
    copilot.install(tmp_path, mcp_config={})
    copilot.uninstall(tmp_path)

    github_skills = tmp_path / ".github" / "skills"
    assert not github_skills.exists() and not github_skills.is_symlink(), (
        ".github/skills/ should be removed after uninstall"
    )


def test_uninstall_preserves_agents_skills_canonical(tmp_path: Path) -> None:
    """uninstall() must NOT remove the canonical .agents/skills/ directory."""
    copilot.install(tmp_path, mcp_config={})
    copilot.uninstall(tmp_path)

    agents_skills = tmp_path / ".agents" / "skills"
    assert agents_skills.exists(), (
        ".agents/skills/ (canonical) should be preserved after uninstall"
    )


def test_uninstall_without_prior_install(tmp_path: Path) -> None:
    """uninstall() on a fresh directory must not raise."""
    copilot.uninstall(tmp_path)
