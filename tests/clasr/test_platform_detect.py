"""
tests/clasr/test_platform_detect.py

Tests for clasr.platforms.detect.detect().
"""

from __future__ import annotations

from pathlib import Path

import pytest

from clasr.platforms.detect import detect


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_manifest(target: Path, platform_dir: str, provider: str) -> None:
    """Create a minimal manifest JSON file for *provider* under *platform_dir*."""
    manifest_dir = target / platform_dir / ".clasr-manifest"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / f"{provider}.json").write_text(
        '{"version": 1, "provider": "' + provider + '", "entries": []}',
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_detect_empty(tmp_path: Path) -> None:
    """Target has no platform dirs — all three lists must be empty."""
    result = detect(tmp_path)
    assert result == {"claude": [], "codex": [], "copilot": []}


def test_detect_claude_one_provider(tmp_path: Path) -> None:
    """Single manifest under .claude → one provider in the claude list."""
    _make_manifest(tmp_path, ".claude", "myprov")
    result = detect(tmp_path)
    assert result["claude"] == ["myprov"]
    assert result["codex"] == []
    assert result["copilot"] == []


def test_detect_multiple_providers(tmp_path: Path) -> None:
    """Two manifest files under .claude — both providers appear, sorted."""
    _make_manifest(tmp_path, ".claude", "beta")
    _make_manifest(tmp_path, ".claude", "alpha")
    result = detect(tmp_path)
    assert result["claude"] == ["alpha", "beta"]


def test_detect_mixed(tmp_path: Path) -> None:
    """Claude has one provider, copilot has two, codex has none."""
    _make_manifest(tmp_path, ".claude", "league")
    _make_manifest(tmp_path, ".github", "zoo")
    _make_manifest(tmp_path, ".github", "abc")
    result = detect(tmp_path)
    assert result["claude"] == ["league"]
    assert result["codex"] == []
    assert result["copilot"] == ["abc", "zoo"]


def test_detect_always_returns_all_keys(tmp_path: Path) -> None:
    """Result always contains all three platform keys regardless of what exists."""
    result = detect(tmp_path)
    assert set(result.keys()) == {"claude", "codex", "copilot"}


def test_detect_no_clasi_imports() -> None:
    """Verify clasr.platforms.detect has no 'from clasi' or 'import clasi' imports."""
    module_path = (
        Path(__file__).parent.parent.parent / "clasr" / "platforms" / "detect.py"
    )
    source = module_path.read_text(encoding="utf-8")
    for line in source.splitlines():
        stripped = line.strip()
        assert not (
            stripped.startswith("from clasi") or stripped.startswith("import clasi")
        ), f"Found clasi import: {line!r}"
