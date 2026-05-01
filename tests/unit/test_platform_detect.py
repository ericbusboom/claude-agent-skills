"""Tests for clasi/platforms/detect.py — advisory platform detection."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from clasi.platforms.detect import PlatformSignals, detect_platforms


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_claude_project(tmp_path: Path) -> None:
    """Create Claude project-level signal files in *tmp_path*."""
    (tmp_path / ".claude").mkdir()
    (tmp_path / "CLAUDE.md").write_text("# CLASI\n")


def _make_codex_project(tmp_path: Path) -> None:
    """Create Codex project-level signal files in *tmp_path*."""
    (tmp_path / ".codex").mkdir()
    (tmp_path / "AGENTS.md").write_text("# AGENTS\n")
    agents_skills = tmp_path / ".agents" / "skills"
    agents_skills.mkdir(parents=True)


# ---------------------------------------------------------------------------
# Smoke test: return type
# ---------------------------------------------------------------------------


def test_returns_platform_signals(tmp_path: Path) -> None:
    """detect_platforms always returns a PlatformSignals instance."""
    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert isinstance(result, PlatformSignals)
    assert isinstance(result.claude_score, int)
    assert isinstance(result.codex_score, int)
    assert isinstance(result.copilot_score, int)
    assert result.recommendation in {"claude", "codex", "copilot", "both"}


# ---------------------------------------------------------------------------
# Claude-only signals
# ---------------------------------------------------------------------------


def test_claude_only_project_files(tmp_path: Path) -> None:
    """Claude project files with no Codex signals → recommendation 'claude'."""
    _make_claude_project(tmp_path)

    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.claude_score > 0
    assert result.codex_score == 0
    assert result.recommendation == "claude"


def test_claude_only_command(tmp_path: Path) -> None:
    """'claude' command installed, no Codex signals → 'claude'."""

    def _which(cmd: str) -> str | None:
        return "/usr/local/bin/claude" if cmd == "claude" else None

    with (
        patch("clasi.platforms.detect.shutil.which", side_effect=_which),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.claude_score > 0
    assert result.codex_score == 0
    assert result.recommendation == "claude"


def test_claude_only_user_dir(tmp_path: Path) -> None:
    """~/.claude present, no Codex signals → 'claude'."""
    fake_home = tmp_path / "home"
    (fake_home / ".claude").mkdir(parents=True)

    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=fake_home),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.claude_score > 0
    assert result.codex_score == 0
    assert result.recommendation == "claude"


def test_claude_only_env_anthropic(tmp_path: Path) -> None:
    """ANTHROPIC_API_KEY in env (name only), no Codex signals → 'claude'."""
    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict(
            "os.environ",
            {"ANTHROPIC_API_KEY": "REDACTED"},
            clear=True,
        ),
    ):
        result = detect_platforms(tmp_path)

    assert result.claude_score > 0
    assert result.codex_score == 0
    assert result.recommendation == "claude"


def test_claude_only_env_prefix(tmp_path: Path) -> None:
    """CLAUDE_* env var present → counts as Claude signal."""
    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict(
            "os.environ",
            {"CLAUDE_API_VERSION": "2024-01"},
            clear=True,
        ),
    ):
        result = detect_platforms(tmp_path)

    assert result.claude_score > 0
    assert result.codex_score == 0
    assert result.recommendation == "claude"


# ---------------------------------------------------------------------------
# Codex-only signals
# ---------------------------------------------------------------------------


def test_codex_only_project_files(tmp_path: Path) -> None:
    """Codex project files with no Claude signals → recommendation 'codex'."""
    _make_codex_project(tmp_path)

    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.codex_score > 0
    assert result.claude_score == 0
    assert result.recommendation == "codex"


def test_codex_only_command(tmp_path: Path) -> None:
    """'codex' command installed, no Claude signals → 'codex'."""

    def _which(cmd: str) -> str | None:
        return "/usr/local/bin/codex" if cmd == "codex" else None

    with (
        patch("clasi.platforms.detect.shutil.which", side_effect=_which),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.codex_score > 0
    assert result.claude_score == 0
    assert result.recommendation == "codex"


def test_codex_only_user_dir(tmp_path: Path) -> None:
    """~/.codex present, no Claude signals → 'codex'."""
    fake_home = tmp_path / "home"
    (fake_home / ".codex").mkdir(parents=True)

    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=fake_home),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.codex_score > 0
    assert result.claude_score == 0
    assert result.recommendation == "codex"


def test_codex_only_env_openai(tmp_path: Path) -> None:
    """OPENAI_API_KEY in env (name only), no Claude signals → 'codex'."""
    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict(
            "os.environ",
            {"OPENAI_API_KEY": "REDACTED"},
            clear=True,
        ),
    ):
        result = detect_platforms(tmp_path)

    assert result.codex_score > 0
    assert result.claude_score == 0
    assert result.recommendation == "codex"


def test_codex_only_env_prefix(tmp_path: Path) -> None:
    """CODEX_* env var present → counts as Codex signal."""
    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict(
            "os.environ",
            {"CODEX_API_ENDPOINT": "https://example.com"},
            clear=True,
        ),
    ):
        result = detect_platforms(tmp_path)

    assert result.codex_score > 0
    assert result.claude_score == 0
    assert result.recommendation == "codex"


# ---------------------------------------------------------------------------
# Both signals present
# ---------------------------------------------------------------------------


def test_both_project_files(tmp_path: Path) -> None:
    """Claude and Codex project files both present → recommendation 'both'."""
    _make_claude_project(tmp_path)
    _make_codex_project(tmp_path)

    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.claude_score > 0
    assert result.codex_score > 0
    assert result.recommendation == "both"


def test_both_commands_installed(tmp_path: Path) -> None:
    """Both 'claude' and 'codex' commands installed → 'both'."""

    def _which(cmd: str) -> str | None:
        return f"/usr/local/bin/{cmd}" if cmd in {"claude", "codex"} else None

    with (
        patch("clasi.platforms.detect.shutil.which", side_effect=_which),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.claude_score > 0
    assert result.codex_score > 0
    assert result.recommendation == "both"


def test_both_env_vars(tmp_path: Path) -> None:
    """Both ANTHROPIC_API_KEY and OPENAI_API_KEY present by name → 'both'."""
    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict(
            "os.environ",
            {"ANTHROPIC_API_KEY": "REDACTED", "OPENAI_API_KEY": "REDACTED"},
            clear=True,
        ),
    ):
        result = detect_platforms(tmp_path)

    assert result.claude_score > 0
    assert result.codex_score > 0
    assert result.recommendation == "both"


# ---------------------------------------------------------------------------
# No signals
# ---------------------------------------------------------------------------


def test_no_signals_defaults_to_claude(tmp_path: Path) -> None:
    """No signals at all → safe default 'claude' (or 'both'), score may be 0."""
    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.recommendation in {"claude", "both"}


def test_no_signals_scores_are_zero(tmp_path: Path) -> None:
    """With no signals, both scores are 0."""
    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.claude_score == 0
    assert result.codex_score == 0


# ---------------------------------------------------------------------------
# Env var name detection — values never read
# ---------------------------------------------------------------------------


def test_env_name_detection_does_not_expose_values(tmp_path: Path) -> None:
    """Verify that env var names are used for scoring but values are opaque.

    We set a known env var and confirm the score is positive without the
    implementation needing to access (or test) the value.
    """
    sentinel_value = "super_secret_key_that_must_not_appear_in_recommendation"

    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict(
            "os.environ",
            {"ANTHROPIC_API_KEY": sentinel_value},
            clear=True,
        ),
    ):
        result = detect_platforms(tmp_path)

    # Score went up because the *name* was found
    assert result.claude_score > 0
    # The recommendation string must never contain the secret value
    assert sentinel_value not in result.recommendation


def test_multiple_claude_env_vars(tmp_path: Path) -> None:
    """Multiple CLAUDE_* env vars each contribute to claude_score."""
    env = {
        "CLAUDE_API_KEY": "REDACTED",
        "CLAUDE_MODEL": "claude-3",
        "CLAUDE_TIMEOUT": "30",
    }
    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", env, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.claude_score >= 3  # at least 3 env var hits
    assert result.codex_score == 0
    assert result.recommendation == "claude"


def test_multiple_codex_env_vars(tmp_path: Path) -> None:
    """Multiple CODEX_* env vars each contribute to codex_score."""
    env = {
        "CODEX_API_KEY": "REDACTED",
        "CODEX_MODEL": "gpt-4o",
    }
    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", env, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.codex_score >= 2
    assert result.claude_score == 0
    assert result.recommendation == "codex"


# ---------------------------------------------------------------------------
# Score additivity across signal types
# ---------------------------------------------------------------------------


def test_all_claude_signals_accumulate(tmp_path: Path) -> None:
    """All Claude signal types (files, command, user dir, env) sum correctly."""
    _make_claude_project(tmp_path)
    fake_home = tmp_path / "home"
    (fake_home / ".claude").mkdir(parents=True)

    def _which(cmd: str) -> str | None:
        return "/usr/local/bin/claude" if cmd == "claude" else None

    with (
        patch("clasi.platforms.detect.shutil.which", side_effect=_which),
        patch("clasi.platforms.detect.Path.home", return_value=fake_home),
        patch.dict("os.environ", {"ANTHROPIC_API_KEY": "REDACTED"}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    # .claude (+2) + CLAUDE.md (+2) + command (+1) + user dir (+1) + env (+1) = 7
    assert result.claude_score >= 7
    assert result.recommendation == "claude"


def test_all_codex_signals_accumulate(tmp_path: Path) -> None:
    """All Codex signal types accumulate into codex_score."""
    _make_codex_project(tmp_path)
    fake_home = tmp_path / "home"
    (fake_home / ".codex").mkdir(parents=True)

    def _which(cmd: str) -> str | None:
        return "/usr/local/bin/codex" if cmd == "codex" else None

    with (
        patch("clasi.platforms.detect.shutil.which", side_effect=_which),
        patch("clasi.platforms.detect.Path.home", return_value=fake_home),
        patch.dict("os.environ", {"OPENAI_API_KEY": "REDACTED"}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    # .codex (+2) + AGENTS.md (+2) + .agents/skills (+2) + command (+1) + user dir (+1) + env (+1) = 9
    assert result.codex_score >= 9
    assert result.recommendation == "codex"


# ---------------------------------------------------------------------------
# Copilot signals
# ---------------------------------------------------------------------------


def _make_copilot_project(tmp_path: Path) -> None:
    """Create Copilot project-level signal files in *tmp_path*."""
    github = tmp_path / ".github"
    github.mkdir()
    (github / "copilot-instructions.md").write_text("# Copilot\n")


def test_copilot_project_file_copilot_instructions(tmp_path: Path) -> None:
    """.github/copilot-instructions.md present → copilot signal."""
    _make_copilot_project(tmp_path)

    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.copilot_score > 0
    assert result.recommendation == "copilot"


def test_copilot_project_file_agents_dir(tmp_path: Path) -> None:
    """.github/agents/ present → copilot signal."""
    (tmp_path / ".github" / "agents").mkdir(parents=True)

    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.copilot_score > 0
    assert result.recommendation == "copilot"


def test_copilot_project_file_instructions_dir(tmp_path: Path) -> None:
    """.github/instructions/ present → copilot signal."""
    instructions = tmp_path / ".github" / "instructions"
    instructions.mkdir(parents=True)
    (instructions / "example.instructions.md").write_text("# Instructions\n")

    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.copilot_score > 0
    assert result.recommendation == "copilot"


def test_copilot_command_code(tmp_path: Path) -> None:
    """'code' binary on PATH → copilot advisory signal."""

    def _which(cmd: str) -> str | None:
        return "/usr/local/bin/code" if cmd == "code" else None

    with (
        patch("clasi.platforms.detect.shutil.which", side_effect=_which),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.copilot_score > 0
    assert result.recommendation == "copilot"


def test_copilot_command_gh(tmp_path: Path) -> None:
    """'gh' binary on PATH → copilot advisory signal."""

    def _which(cmd: str) -> str | None:
        return "/usr/local/bin/gh" if cmd == "gh" else None

    with (
        patch("clasi.platforms.detect.shutil.which", side_effect=_which),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.copilot_score > 0
    assert result.recommendation == "copilot"


def test_copilot_user_config_dir(tmp_path: Path) -> None:
    """~/.config/github-copilot/ present → copilot signal."""
    fake_home = tmp_path / "home"
    (fake_home / ".config" / "github-copilot").mkdir(parents=True)

    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=fake_home),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.copilot_score > 0
    assert result.recommendation == "copilot"


def test_copilot_env_var(tmp_path: Path) -> None:
    """GITHUB_COPILOT_* env var present → copilot signal."""
    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {"GITHUB_COPILOT_TOKEN": "REDACTED"}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.copilot_score > 0
    assert result.recommendation == "copilot"


def test_copilot_no_signals(tmp_path: Path) -> None:
    """No Copilot signals → copilot_score is 0."""
    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.copilot_score == 0


def test_copilot_and_claude_both_detected(tmp_path: Path) -> None:
    """Copilot and Claude signals both present → recommendation 'both'."""
    _make_claude_project(tmp_path)
    _make_copilot_project(tmp_path)

    with (
        patch("clasi.platforms.detect.shutil.which", return_value=None),
        patch("clasi.platforms.detect.Path.home", return_value=tmp_path / "fake_home"),
        patch.dict("os.environ", {}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    assert result.claude_score > 0
    assert result.copilot_score > 0
    assert result.recommendation == "both"


def test_all_copilot_signals_accumulate(tmp_path: Path) -> None:
    """All Copilot signal types accumulate into copilot_score."""
    _make_copilot_project(tmp_path)
    fake_home = tmp_path / "home"
    (fake_home / ".config" / "github-copilot").mkdir(parents=True)

    def _which(cmd: str) -> str | None:
        return f"/usr/local/bin/{cmd}" if cmd in {"code", "gh"} else None

    with (
        patch("clasi.platforms.detect.shutil.which", side_effect=_which),
        patch("clasi.platforms.detect.Path.home", return_value=fake_home),
        patch.dict("os.environ", {"GITHUB_COPILOT_TOKEN": "REDACTED"}, clear=True),
    ):
        result = detect_platforms(tmp_path)

    # copilot-instructions.md (+2) + code (+1) + gh (+1) + user dir (+1) + env (+1) = 6
    assert result.copilot_score >= 6
    assert result.recommendation == "copilot"
