"""Tests for clasi/uninstall_command.py and the `clasi uninstall` CLI command.

Covers:
- --claude only removes Claude artifacts.
- --codex only removes Codex artifacts.
- --claude --codex removes both.
- Non-interactive, no flag: exits with error.
- Interactive, no flag: prompts (mocked).
- Idempotency: running uninstall twice does not error.
- User content preservation: CLAUDE.md and AGENTS.md user sections survive.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from clasi.cli import cli
from clasi.platforms.claude import install as claude_install
from clasi.platforms.codex import install as codex_install


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

_MCP_CONFIG = {
    "command": "clasi",
    "args": ["mcp"],
}


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """Return a fresh empty project directory with both platforms installed."""
    d = tmp_path / "project"
    d.mkdir()
    return d


@pytest.fixture
def both_installed(project: Path) -> Path:
    """Install both Claude and Codex into *project*; return the project path."""
    claude_install(project, _MCP_CONFIG)
    codex_install(project, _MCP_CONFIG)
    return project


# ---------------------------------------------------------------------------
# Helper: check Claude artifacts absent / present
# ---------------------------------------------------------------------------

def _claude_artifacts_absent(project: Path) -> None:
    """Assert all CLASI-managed Claude artifacts are removed."""
    claude_md = project / "CLAUDE.md"
    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")
        assert "<!-- CLASI:START -->" not in content, "CLASI section should be gone from CLAUDE.md"
        assert "<!-- CLASI:END -->" not in content


def _codex_artifacts_absent(project: Path) -> None:
    """Assert all CLASI-managed Codex artifacts are removed."""
    agents_md = project / "AGENTS.md"
    if agents_md.exists():
        content = agents_md.read_text(encoding="utf-8")
        assert "<!-- CLASI:START -->" not in content, "CLASI section should be gone from AGENTS.md"
        assert "<!-- CLASI:END -->" not in content

    config_path = project / ".codex" / "config.toml"
    if config_path.exists():
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib  # type: ignore[no-redef]
        data = tomllib.loads(config_path.read_text(encoding="utf-8"))
        assert "clasi" not in data.get("mcp_servers", {}), "clasi mcp_server entry should be gone"
        assert "codex_hooks" not in data, "codex_hooks should be gone"

    hooks_path = project / ".codex" / "hooks.json"
    if hooks_path.exists():
        data = json.loads(hooks_path.read_text(encoding="utf-8"))
        stop_list = data.get("hooks", {}).get("Stop", [])
        clasi_hook = {"command": "clasi", "args": ["hook", "codex-plan-to-todo"]}
        assert clasi_hook not in stop_list, "CLASI Stop hook should be gone"

    skill = project / ".agents" / "skills" / "se" / "SKILL.md"
    assert not skill.exists(), ".agents/skills/se/SKILL.md should be deleted"


# ---------------------------------------------------------------------------
# run_uninstall() direct tests
# ---------------------------------------------------------------------------


def test_uninstall_claude_only_removes_claude_artifacts(both_installed: Path) -> None:
    """--claude removes Claude artifacts and leaves Codex artifacts intact."""
    project = both_installed
    from clasi.uninstall_command import run_uninstall

    run_uninstall(str(project), claude=True, codex=False)

    # Claude CLASI section gone from CLAUDE.md
    _claude_artifacts_absent(project)

    # Codex AGENTS.md still has CLASI section
    agents_md = project / "AGENTS.md"
    assert agents_md.exists(), "AGENTS.md should still exist"
    content = agents_md.read_text(encoding="utf-8")
    assert "<!-- CLASI:START -->" in content, "Codex CLASI section should remain"

    # Codex skill still present
    skill = project / ".agents" / "skills" / "se" / "SKILL.md"
    assert skill.exists(), "Codex skill should remain"


def test_uninstall_codex_only_removes_codex_artifacts(both_installed: Path) -> None:
    """--codex removes Codex artifacts and leaves Claude artifacts intact."""
    project = both_installed
    from clasi.uninstall_command import run_uninstall

    run_uninstall(str(project), claude=False, codex=True)

    # Codex artifacts gone
    _codex_artifacts_absent(project)

    # Claude CLAUDE.md CLASI section still present
    claude_md = project / "CLAUDE.md"
    assert claude_md.exists(), "CLAUDE.md should still exist"
    content = claude_md.read_text(encoding="utf-8")
    assert "<!-- CLASI:START -->" in content, "Claude CLASI section should remain"

    # Claude rules still present
    rules_dir = project / ".claude" / "rules"
    assert rules_dir.exists(), ".claude/rules/ should still exist"


def test_uninstall_both_removes_all_artifacts(both_installed: Path) -> None:
    """--claude --codex removes all CLASI artifacts from both platforms."""
    project = both_installed
    from clasi.uninstall_command import run_uninstall

    run_uninstall(str(project), claude=True, codex=True)

    _claude_artifacts_absent(project)
    _codex_artifacts_absent(project)


def test_uninstall_non_interactive_no_flag_exits_with_error(project: Path) -> None:
    """Non-interactive mode with no flag exits 1 with a clear error message."""
    from clasi.uninstall_command import run_uninstall

    # Force non-interactive by patching isatty to return False
    with patch("sys.stdin") as mock_stdin, patch("sys.stdout") as mock_stdout:
        mock_stdin.isatty.return_value = False
        mock_stdout.isatty.return_value = False

        with pytest.raises(SystemExit) as exc_info:
            run_uninstall(str(project), claude=False, codex=False)

    assert exc_info.value.code == 1


def test_uninstall_interactive_no_flag_prompts(project: Path) -> None:
    """Interactive mode with no flag calls _prompt_uninstall and dispatches."""
    from clasi.uninstall_command import run_uninstall

    # Install Claude so the prompt has something to offer
    claude_install(project, _MCP_CONFIG)

    # Patch the isatty calls at the module level in uninstall_command so we
    # don't have to replace sys.stdin/stdout entirely (which breaks click.echo).
    with patch("clasi.uninstall_command.sys") as mock_sys:
        mock_sys.stdin.isatty.return_value = True
        mock_sys.stdout.isatty.return_value = True

        with patch("clasi.uninstall_command._prompt_uninstall", return_value="claude") as mock_prompt:
            run_uninstall(str(project), claude=False, codex=False)

    mock_prompt.assert_called_once()

    # Claude artifacts should be removed
    _claude_artifacts_absent(project)


def test_uninstall_idempotent_claude(both_installed: Path) -> None:
    """Running --claude uninstall twice does not raise an error."""
    project = both_installed
    from clasi.uninstall_command import run_uninstall

    run_uninstall(str(project), claude=True, codex=False)
    # Second call is idempotent — should not raise
    run_uninstall(str(project), claude=True, codex=False)


def test_uninstall_idempotent_codex(both_installed: Path) -> None:
    """Running --codex uninstall twice does not raise an error."""
    project = both_installed
    from clasi.uninstall_command import run_uninstall

    run_uninstall(str(project), claude=False, codex=True)
    # Second call is idempotent — should not raise
    run_uninstall(str(project), claude=False, codex=True)


def test_uninstall_idempotent_both(both_installed: Path) -> None:
    """Running --claude --codex uninstall twice does not raise an error."""
    project = both_installed
    from clasi.uninstall_command import run_uninstall

    run_uninstall(str(project), claude=True, codex=True)
    run_uninstall(str(project), claude=True, codex=True)


def test_uninstall_never_installed_is_noop(project: Path) -> None:
    """Uninstalling a platform that was never installed is a no-op (no error)."""
    from clasi.uninstall_command import run_uninstall

    # No install step — both platforms are absent
    run_uninstall(str(project), claude=True, codex=True)


# ---------------------------------------------------------------------------
# User content preservation
# ---------------------------------------------------------------------------


def test_uninstall_claude_md_user_section_preserved(project: Path) -> None:
    """CLAUDE.md user content outside the CLASI block survives --claude uninstall."""
    user_section = "# My Project Notes\n\nThis is user-owned content.\n"
    claude_md = project / "CLAUDE.md"
    claude_md.write_text(user_section, encoding="utf-8")

    claude_install(project, _MCP_CONFIG)

    from clasi.uninstall_command import run_uninstall
    run_uninstall(str(project), claude=True, codex=False)

    assert claude_md.exists(), "CLAUDE.md should still exist when user content present"
    content = claude_md.read_text(encoding="utf-8")
    assert "My Project Notes" in content
    assert "user-owned content" in content
    assert "<!-- CLASI:START -->" not in content
    assert "<!-- CLASI:END -->" not in content


def test_uninstall_agents_md_user_section_preserved(project: Path) -> None:
    """AGENTS.md user content outside the CLASI block survives --codex uninstall."""
    user_section = "# My Agent Instructions\n\nCustom guidance here.\n"
    agents_md = project / "AGENTS.md"
    agents_md.write_text(user_section, encoding="utf-8")

    codex_install(project, _MCP_CONFIG)

    from clasi.uninstall_command import run_uninstall
    run_uninstall(str(project), claude=False, codex=True)

    assert agents_md.exists(), "AGENTS.md should still exist when user content present"
    content = agents_md.read_text(encoding="utf-8")
    assert "My Agent Instructions" in content
    assert "Custom guidance here" in content
    assert "<!-- CLASI:START -->" not in content
    assert "<!-- CLASI:END -->" not in content


def test_uninstall_does_not_touch_docs_clasi(both_installed: Path) -> None:
    """Uninstall never removes docs/clasi/ or its contents."""
    project = both_installed

    # Create a docs/clasi/todo directory with a user file alongside the
    # AGENTS.md that install already created.
    todo_dir = project / "docs" / "clasi" / "todo"
    todo_dir.mkdir(parents=True, exist_ok=True)
    todo_file = todo_dir / "sample-todo.md"
    todo_file.write_text("---\nstatus: pending\n---\n# A TODO\n", encoding="utf-8")

    from clasi.uninstall_command import run_uninstall
    run_uninstall(str(project), claude=True, codex=True)

    assert todo_file.exists(), "docs/clasi/todo/sample-todo.md must not be touched by uninstall"


# ---------------------------------------------------------------------------
# CLI integration tests (via click.testing.CliRunner)
# ---------------------------------------------------------------------------


def test_cli_uninstall_claude_flag(both_installed: Path) -> None:
    """CLI `clasi uninstall --claude` removes Claude artifacts."""
    runner = CliRunner()
    result = runner.invoke(cli, ["uninstall", str(both_installed), "--claude"])
    assert result.exit_code == 0, f"Expected exit 0, got: {result.output}"
    _claude_artifacts_absent(both_installed)


def test_cli_uninstall_codex_flag(both_installed: Path) -> None:
    """CLI `clasi uninstall --codex` removes Codex artifacts."""
    runner = CliRunner()
    result = runner.invoke(cli, ["uninstall", str(both_installed), "--codex"])
    assert result.exit_code == 0, f"Expected exit 0, got: {result.output}"
    _codex_artifacts_absent(both_installed)


def test_cli_uninstall_both_flags(both_installed: Path) -> None:
    """CLI `clasi uninstall --claude --codex` removes both platforms."""
    runner = CliRunner()
    result = runner.invoke(cli, ["uninstall", str(both_installed), "--claude", "--codex"])
    assert result.exit_code == 0, f"Expected exit 0, got: {result.output}"
    _claude_artifacts_absent(both_installed)
    _codex_artifacts_absent(both_installed)


def test_cli_uninstall_no_flag_non_interactive_error(project: Path) -> None:
    """CLI `clasi uninstall` with no flags in non-interactive mode exits 1."""
    runner = CliRunner()
    # CliRunner uses non-TTY by default
    result = runner.invoke(cli, ["uninstall", str(project)])
    assert result.exit_code == 1
    assert "specify" in result.output.lower() or "--claude" in result.output


def test_cli_uninstall_help(project: Path) -> None:
    """CLI `clasi uninstall --help` exits 0 and mentions the flags."""
    runner = CliRunner()
    result = runner.invoke(cli, ["uninstall", "--help"])
    assert result.exit_code == 0
    assert "--claude" in result.output
    assert "--codex" in result.output
