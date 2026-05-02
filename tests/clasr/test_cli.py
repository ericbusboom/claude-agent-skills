"""
tests/clasr/test_cli.py

Tests for clasr.cli — argument parsing, --instructions flag, and validation.
"""

from __future__ import annotations

import subprocess
import sys

import pytest

from clasr.cli import main


# ---------------------------------------------------------------------------
# --instructions
# ---------------------------------------------------------------------------


def test_instructions_prints_nonempty_content(capsys: pytest.CaptureFixture[str]) -> None:
    """--instructions should print non-empty content and return 0."""
    rc = main(["--instructions"])
    captured = capsys.readouterr()
    assert rc == 0
    assert len(captured.out) > 0
    # Should contain something recognisable from instructions.md
    assert "clasr" in captured.out.lower()


def test_instructions_via_subprocess() -> None:
    """Verify --instructions works end-to-end through the installed entry point."""
    result = subprocess.run(
        [sys.executable, "-m", "clasr.cli", "--instructions"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert len(result.stdout) > 0


# ---------------------------------------------------------------------------
# install --help
# ---------------------------------------------------------------------------


def test_install_help_shows_all_flags() -> None:
    """clasr install --help should list all documented flags."""
    result = subprocess.run(
        [sys.executable, "-m", "clasr.cli", "install", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    help_text = result.stdout
    for flag in ("--source", "--provider", "--claude", "--codex", "--copilot", "--copy", "--target"):
        assert flag in help_text, f"Expected {flag!r} in install --help output"


# ---------------------------------------------------------------------------
# uninstall --help
# ---------------------------------------------------------------------------


def test_uninstall_help_shows_all_flags() -> None:
    """clasr uninstall --help should list all documented flags."""
    result = subprocess.run(
        [sys.executable, "-m", "clasr.cli", "uninstall", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    help_text = result.stdout
    for flag in ("--provider", "--claude", "--codex", "--copilot", "--target"):
        assert flag in help_text, f"Expected {flag!r} in uninstall --help output"


# ---------------------------------------------------------------------------
# install validation
# ---------------------------------------------------------------------------


def test_install_no_platform_flag_exits_nonzero(capsys: pytest.CaptureFixture[str]) -> None:
    """install with no platform flag should exit non-zero with a clear message."""
    with pytest.raises(SystemExit) as exc_info:
        main(["install", "--source", "/tmp/asr", "--provider", "test"])
    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "claude" in captured.err.lower() or "platform" in captured.err.lower()


def test_install_no_provider_exits_nonzero(capsys: pytest.CaptureFixture[str]) -> None:
    """install without --provider should exit non-zero with an error message."""
    with pytest.raises(SystemExit) as exc_info:
        main(["install", "--source", "/tmp/asr", "--claude"])
    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "provider" in captured.err.lower()


def test_install_no_source_exits_nonzero(capsys: pytest.CaptureFixture[str]) -> None:
    """install without --source should exit non-zero with an error message."""
    with pytest.raises(SystemExit) as exc_info:
        main(["install", "--provider", "test", "--claude"])
    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "source" in captured.err.lower()


def test_install_valid_args_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    """install with all required args should exit 0 (stub)."""
    rc = main(["install", "--source", "/tmp/asr", "--provider", "test", "--claude"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "not yet implemented" in captured.out


# ---------------------------------------------------------------------------
# uninstall validation
# ---------------------------------------------------------------------------


def test_uninstall_no_platform_flag_exits_nonzero(capsys: pytest.CaptureFixture[str]) -> None:
    """uninstall with no platform flag should exit non-zero with a clear message."""
    with pytest.raises(SystemExit) as exc_info:
        main(["uninstall", "--provider", "test"])
    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "claude" in captured.err.lower() or "platform" in captured.err.lower()


def test_uninstall_no_provider_exits_nonzero(capsys: pytest.CaptureFixture[str]) -> None:
    """uninstall without --provider should exit non-zero with an error message."""
    with pytest.raises(SystemExit) as exc_info:
        main(["uninstall", "--claude"])
    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "provider" in captured.err.lower()


def test_uninstall_valid_args_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    """uninstall with all required args should exit 0 (stub)."""
    rc = main(["uninstall", "--provider", "test", "--claude"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "not yet implemented" in captured.out


# ---------------------------------------------------------------------------
# No imports from clasi (static check)
# ---------------------------------------------------------------------------


def test_no_imports_from_clasi() -> None:
    """clasr/cli.py must not import anything from the clasi package."""
    import importlib.resources
    package_ref = importlib.resources.files("clasr")
    cli_path = package_ref / "cli.py"
    source = cli_path.read_text(encoding="utf-8")
    assert "from clasi" not in source, "clasr/cli.py must not import from clasi"
    assert "import clasi" not in source, "clasr/cli.py must not import clasi"
