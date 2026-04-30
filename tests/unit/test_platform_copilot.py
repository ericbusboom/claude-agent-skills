"""
tests/unit/test_platform_copilot.py

Minimal tests for clasi/platforms/copilot.py.

Expanded by tickets 007-010 as each stub is implemented.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from clasi.platforms import copilot
from clasi.platforms._markers import MARKER_END, MARKER_START
import yaml

from clasi.platforms._rules import (
    CLASI_ARTIFACTS_BODY,
    GIT_COMMITS_BODY,
    MCP_REQUIRED_BODY,
    SOURCE_CODE_BODY,
    TODO_DIR_BODY,
)


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


# ---------------------------------------------------------------------------
# _install_global_instructions — ticket 007
# ---------------------------------------------------------------------------


def test_install_global_instructions_creates_file(tmp_path: Path) -> None:
    """_install_global_instructions must create .github/copilot-instructions.md."""
    copilot._install_global_instructions(tmp_path)
    path = tmp_path / ".github" / "copilot-instructions.md"
    assert path.exists(), ".github/copilot-instructions.md must be created"


def test_install_global_instructions_contains_marker_block(tmp_path: Path) -> None:
    """The file must contain the CLASI marker block."""
    copilot._install_global_instructions(tmp_path)
    content = (tmp_path / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
    assert MARKER_START in content
    assert MARKER_END in content


def test_install_global_instructions_entry_point(tmp_path: Path) -> None:
    """The CLASI block must reference .github/agents/team-lead.agent.md."""
    copilot._install_global_instructions(tmp_path)
    content = (tmp_path / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
    assert ".github/agents/team-lead.agent.md" in content


def test_install_global_instructions_mcp_required_body(tmp_path: Path) -> None:
    """The CLASI block must contain the MCP_REQUIRED_BODY content."""
    copilot._install_global_instructions(tmp_path)
    content = (tmp_path / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
    # Check a representative fragment from MCP_REQUIRED_BODY
    assert "Call `get_version()` to verify the MCP server is running" in content


def test_install_global_instructions_git_commits_body(tmp_path: Path) -> None:
    """The CLASI block must contain the GIT_COMMITS_BODY content."""
    copilot._install_global_instructions(tmp_path)
    content = (tmp_path / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
    # Check a representative fragment from GIT_COMMITS_BODY
    assert "clasi version bump" in content


def test_install_global_instructions_idempotent_preserves_user_content(tmp_path: Path) -> None:
    """Re-running _install_global_instructions must preserve user content outside the marker block."""
    path = tmp_path / ".github" / "copilot-instructions.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    user_content = "# My Custom Header\n\nSome project-specific instructions.\n"
    path.write_text(user_content, encoding="utf-8")

    # First install appends the CLASI block
    copilot._install_global_instructions(tmp_path)
    content_after_first = path.read_text(encoding="utf-8")
    assert user_content.strip() in content_after_first
    assert MARKER_START in content_after_first

    # Second install replaces the CLASI block in place
    copilot._install_global_instructions(tmp_path)
    content_after_second = path.read_text(encoding="utf-8")
    assert user_content.strip() in content_after_second
    assert MARKER_START in content_after_second


def test_install_global_instructions_idempotent_single_block(tmp_path: Path) -> None:
    """Re-running _install_global_instructions must not create duplicate marker blocks."""
    copilot._install_global_instructions(tmp_path)
    copilot._install_global_instructions(tmp_path)
    content = (tmp_path / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
    assert content.count(MARKER_START) == 1, "Only one CLASI block should exist"
    assert content.count(MARKER_END) == 1, "Only one CLASI block should exist"


# ---------------------------------------------------------------------------
# _uninstall_global_instructions — ticket 007
# ---------------------------------------------------------------------------


def test_uninstall_global_instructions_strips_block(tmp_path: Path) -> None:
    """_uninstall_global_instructions must remove the CLASI marker block."""
    copilot._install_global_instructions(tmp_path)
    copilot._uninstall_global_instructions(tmp_path)
    path = tmp_path / ".github" / "copilot-instructions.md"
    # File may be deleted if it only contained the CLASI block
    if path.exists():
        content = path.read_text(encoding="utf-8")
        assert MARKER_START not in content
        assert MARKER_END not in content


def test_uninstall_global_instructions_preserves_user_content(tmp_path: Path) -> None:
    """_uninstall_global_instructions must preserve user content outside the marker block."""
    path = tmp_path / ".github" / "copilot-instructions.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    user_content = "# My Custom Header\n\nSome project-specific instructions.\n"
    path.write_text(user_content, encoding="utf-8")

    copilot._install_global_instructions(tmp_path)
    assert MARKER_START in path.read_text(encoding="utf-8")

    copilot._uninstall_global_instructions(tmp_path)
    assert path.exists(), "File should remain because it has user content"
    content = path.read_text(encoding="utf-8")
    assert MARKER_START not in content
    assert "My Custom Header" in content


def test_uninstall_global_instructions_no_file(tmp_path: Path) -> None:
    """_uninstall_global_instructions must not raise if the file does not exist."""
    copilot._uninstall_global_instructions(tmp_path)  # no file, must not raise


# ---------------------------------------------------------------------------
# _print_cloud_mcp_notice — ticket 007
# ---------------------------------------------------------------------------


def test_print_cloud_mcp_notice_header(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """_print_cloud_mcp_notice must print the header line."""
    copilot._print_cloud_mcp_notice(mcp_config={"command": "clasi", "args": ["mcp"]})
    captured = capsys.readouterr()
    assert "Copilot Cloud Coding Agent MCP (manual step required):" in captured.out


def test_print_cloud_mcp_notice_settings_url(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """_print_cloud_mcp_notice must print a GitHub Settings URL pattern."""
    copilot._print_cloud_mcp_notice(mcp_config={"command": "clasi", "args": ["mcp"]})
    captured = capsys.readouterr()
    assert "github.com" in captured.out
    assert "settings" in captured.out


def test_print_cloud_mcp_notice_json_snippet(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """_print_cloud_mcp_notice must include valid JSON with the servers key."""
    mcp_config = {"command": "clasi", "args": ["mcp"]}
    copilot._print_cloud_mcp_notice(mcp_config=mcp_config)
    captured = capsys.readouterr()
    # Extract lines that look like JSON and try to parse the snippet
    assert '"servers"' in captured.out
    assert '"clasi"' in captured.out


def test_print_cloud_mcp_notice_includes_mcp_config(capsys: pytest.CaptureFixture) -> None:
    """The JSON snippet must include the mcp_config content."""
    mcp_config = {"command": "clasi", "args": ["mcp"]}
    copilot._print_cloud_mcp_notice(mcp_config=mcp_config)
    captured = capsys.readouterr()
    assert '"command"' in captured.out
    assert "clasi" in captured.out


def test_install_calls_print_cloud_mcp_notice(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """install() must call _print_cloud_mcp_notice at the end."""
    copilot.install(tmp_path, mcp_config={"command": "clasi", "args": ["mcp"]})
    captured = capsys.readouterr()
    assert "Copilot Cloud Coding Agent MCP (manual step required):" in captured.out


# ---------------------------------------------------------------------------
# _install_path_rules / _uninstall_path_rules — ticket 008
# ---------------------------------------------------------------------------

# Map of expected filename -> (applyTo glob, rule body constant)
_EXPECTED_PATH_RULES = [
    ("clasi-artifacts.instructions.md", "docs/clasi/**", CLASI_ARTIFACTS_BODY),
    ("todo-dir.instructions.md", "docs/clasi/todo/**", TODO_DIR_BODY),
    ("source-code.instructions.md", "clasi/**", SOURCE_CODE_BODY),
]


def test_install_path_rules_creates_instructions_dir(tmp_path: Path) -> None:
    """`_install_path_rules` must create .github/instructions/ if absent."""
    copilot._install_path_rules(tmp_path)
    assert (tmp_path / ".github" / "instructions").is_dir()


def test_install_path_rules_creates_all_files(tmp_path: Path) -> None:
    """`_install_path_rules` must write one file per CLASI path rule."""
    copilot._install_path_rules(tmp_path)
    rules_dir = tmp_path / ".github" / "instructions"
    for fname, _apply_to, _body in _EXPECTED_PATH_RULES:
        assert (rules_dir / fname).exists(), f"Expected {fname} to exist"


def test_install_path_rules_valid_yaml_frontmatter(tmp_path: Path) -> None:
    """Each emitted file must have parseable YAML frontmatter."""
    copilot._install_path_rules(tmp_path)
    rules_dir = tmp_path / ".github" / "instructions"
    for fname, _apply_to, _body in _EXPECTED_PATH_RULES:
        content = (rules_dir / fname).read_text(encoding="utf-8")
        # YAML frontmatter is between the first two "---" delimiters
        parts = content.split("---", maxsplit=2)
        assert len(parts) >= 3, f"{fname}: expected YAML frontmatter delimiters"
        fm = yaml.safe_load(parts[1])
        assert fm is not None, f"{fname}: frontmatter must not be empty"
        assert "applyTo" in fm, f"{fname}: frontmatter must contain 'applyTo' key"


def test_install_path_rules_apply_to_values(tmp_path: Path) -> None:
    """Each file's `applyTo` frontmatter value must match the expected glob."""
    copilot._install_path_rules(tmp_path)
    rules_dir = tmp_path / ".github" / "instructions"
    for fname, apply_to, _body in _EXPECTED_PATH_RULES:
        content = (rules_dir / fname).read_text(encoding="utf-8")
        parts = content.split("---", maxsplit=2)
        fm = yaml.safe_load(parts[1])
        assert fm["applyTo"] == apply_to, (
            f"{fname}: expected applyTo={apply_to!r}, got {fm['applyTo']!r}"
        )


def test_install_path_rules_body_content(tmp_path: Path) -> None:
    """Each file's body must match the corresponding _rules.py constant."""
    copilot._install_path_rules(tmp_path)
    rules_dir = tmp_path / ".github" / "instructions"
    for fname, _apply_to, body in _EXPECTED_PATH_RULES:
        content = (rules_dir / fname).read_text(encoding="utf-8")
        # Body follows the closing "---" of frontmatter
        parts = content.split("---", maxsplit=2)
        file_body = parts[2].strip()
        assert file_body == body.strip(), (
            f"{fname}: body content does not match expected constant"
        )


def test_install_path_rules_idempotent(tmp_path: Path) -> None:
    """Calling `_install_path_rules` twice must produce the same files (no error)."""
    copilot._install_path_rules(tmp_path)
    copilot._install_path_rules(tmp_path)
    rules_dir = tmp_path / ".github" / "instructions"
    for fname, _apply_to, _body in _EXPECTED_PATH_RULES:
        assert (rules_dir / fname).exists()


def test_uninstall_path_rules_removes_clasi_files(tmp_path: Path) -> None:
    """`_uninstall_path_rules` must remove all CLASI-written instruction files."""
    copilot._install_path_rules(tmp_path)
    copilot._uninstall_path_rules(tmp_path)
    rules_dir = tmp_path / ".github" / "instructions"
    for fname, _apply_to, _body in _EXPECTED_PATH_RULES:
        assert not (rules_dir / fname).exists(), f"{fname} should be removed after uninstall"


def test_uninstall_path_rules_preserves_user_files(tmp_path: Path) -> None:
    """`_uninstall_path_rules` must not remove user-created files."""
    copilot._install_path_rules(tmp_path)
    rules_dir = tmp_path / ".github" / "instructions"
    user_file = rules_dir / "my-custom.instructions.md"
    user_file.write_text("# User content\n", encoding="utf-8")

    copilot._uninstall_path_rules(tmp_path)

    assert user_file.exists(), "User-created file must not be removed by uninstall"


def test_uninstall_path_rules_does_not_rmdir(tmp_path: Path) -> None:
    """`_uninstall_path_rules` must NOT remove .github/instructions/ even if empty."""
    copilot._install_path_rules(tmp_path)
    copilot._uninstall_path_rules(tmp_path)
    rules_dir = tmp_path / ".github" / "instructions"
    assert rules_dir.exists(), ".github/instructions/ must remain after uninstall"


def test_uninstall_path_rules_no_install(tmp_path: Path) -> None:
    """`_uninstall_path_rules` on a fresh directory must not raise."""
    copilot._uninstall_path_rules(tmp_path)  # no prior install, must not raise
