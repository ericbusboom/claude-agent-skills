"""
tests/clasr/test_manifest.py

Tests for clasr.manifest — per-platform per-provider manifest I/O.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from clasr.manifest import (
    delete_manifest,
    manifest_path,
    read_manifest,
    write_manifest,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_manifest(
    provider: str = "myprovider",
    platform: str = "claude",
    source: str = "/abs/path/to/asr",
    entries: list | None = None,
) -> dict:
    return {
        "version": 1,
        "provider": provider,
        "platform": platform,
        "source": source,
        "entries": entries or [],
    }


# ---------------------------------------------------------------------------
# manifest_path
# ---------------------------------------------------------------------------

class TestManifestPath:

    def test_manifest_path_returns_expected_path(self, tmp_path):
        """manifest_path returns <platform_dir>/.clasr-manifest/<provider>.json"""
        result = manifest_path(tmp_path, "myprovider")
        assert result == tmp_path / ".clasr-manifest" / "myprovider.json"

    def test_manifest_path_different_provider(self, tmp_path):
        """Each provider gets a unique filename."""
        p1 = manifest_path(tmp_path, "providerA")
        p2 = manifest_path(tmp_path, "providerB")
        assert p1 != p2
        assert p1.name == "providerA.json"
        assert p2.name == "providerB.json"

    def test_manifest_path_parent_is_dot_clasr_manifest(self, tmp_path):
        """Parent directory is always named .clasr-manifest."""
        result = manifest_path(tmp_path, "x")
        assert result.parent.name == ".clasr-manifest"
        assert result.parent.parent == tmp_path


# ---------------------------------------------------------------------------
# write_manifest + read_manifest
# ---------------------------------------------------------------------------

class TestWriteAndReadManifest:

    def test_write_and_read_round_trip(self, tmp_path):
        """Write a manifest then read it back; data is identical."""
        manifest = _make_manifest()
        write_manifest(tmp_path, "myprovider", manifest)
        result = read_manifest(tmp_path, "myprovider")
        assert result == manifest

    def test_write_creates_parent_directory(self, tmp_path):
        """.clasr-manifest/ is created automatically if it does not exist."""
        parent = tmp_path / ".clasr-manifest"
        assert not parent.exists()
        write_manifest(tmp_path, "myprovider", _make_manifest())
        assert parent.is_dir()

    def test_write_is_atomic_tmp_does_not_linger(self, tmp_path):
        """After a successful write, no .tmp file remains."""
        write_manifest(tmp_path, "myprovider", _make_manifest())
        tmp_file = manifest_path(tmp_path, "myprovider").with_suffix(".tmp")
        assert not tmp_file.exists()

    def test_write_is_atomic_tmp_used_as_intermediate(self, tmp_path):
        """os.replace is called with a .tmp source path."""
        captured: list[tuple] = []
        real_replace = os.replace

        def capturing_replace(src, dst):
            captured.append((src, dst))
            return real_replace(src, dst)

        with patch("clasr.manifest.os.replace", side_effect=capturing_replace):
            write_manifest(tmp_path, "myprovider", _make_manifest())

        assert len(captured) == 1
        src, dst = captured[0]
        assert str(src).endswith(".tmp")
        assert not str(dst).endswith(".tmp")

    def test_write_produces_valid_json(self, tmp_path):
        """The file on disk is valid, parseable JSON."""
        manifest = _make_manifest()
        write_manifest(tmp_path, "myprovider", manifest)
        path = manifest_path(tmp_path, "myprovider")
        parsed = json.loads(path.read_text(encoding="utf-8"))
        assert parsed == manifest

    def test_write_overwrites_existing_manifest(self, tmp_path):
        """A second write replaces the first."""
        write_manifest(tmp_path, "p", _make_manifest(platform="claude"))
        write_manifest(tmp_path, "p", _make_manifest(platform="codex"))
        result = read_manifest(tmp_path, "p")
        assert result["platform"] == "codex"


# ---------------------------------------------------------------------------
# read_manifest
# ---------------------------------------------------------------------------

class TestReadManifest:

    def test_read_manifest_not_found_returns_none(self, tmp_path):
        """read_manifest returns None when the manifest file does not exist."""
        result = read_manifest(tmp_path, "nonexistent")
        assert result is None

    def test_read_manifest_missing_directory_returns_none(self, tmp_path):
        """read_manifest returns None even when .clasr-manifest/ dir is absent."""
        assert not (tmp_path / ".clasr-manifest").exists()
        result = read_manifest(tmp_path, "anything")
        assert result is None


# ---------------------------------------------------------------------------
# delete_manifest
# ---------------------------------------------------------------------------

class TestDeleteManifest:

    def test_delete_manifest_returns_true_and_removes_file(self, tmp_path):
        """delete_manifest returns True and the file is gone afterwards."""
        write_manifest(tmp_path, "myprovider", _make_manifest())
        path = manifest_path(tmp_path, "myprovider")
        assert path.exists()

        result = delete_manifest(tmp_path, "myprovider")
        assert result is True
        assert not path.exists()

    def test_delete_manifest_not_found_returns_false(self, tmp_path):
        """delete_manifest returns False when the file does not exist."""
        result = delete_manifest(tmp_path, "nonexistent")
        assert result is False

    def test_delete_manifest_does_not_affect_other_providers(self, tmp_path):
        """Deleting one provider's manifest leaves others intact."""
        write_manifest(tmp_path, "provA", _make_manifest(provider="provA"))
        write_manifest(tmp_path, "provB", _make_manifest(provider="provB"))

        delete_manifest(tmp_path, "provA")

        assert read_manifest(tmp_path, "provA") is None
        assert read_manifest(tmp_path, "provB") is not None


# ---------------------------------------------------------------------------
# Entry kind coverage
# ---------------------------------------------------------------------------

class TestEntryKinds:
    """At least one test per entry kind in the schema."""

    def _write_and_read(self, tmp_path: Path, entries: list) -> list:
        manifest = _make_manifest(entries=entries)
        write_manifest(tmp_path, "p", manifest)
        return read_manifest(tmp_path, "p")["entries"]

    def test_entry_kind_symlink(self, tmp_path):
        entries = [
            {"path": ".claude/skills/foo/SKILL.md", "kind": "symlink", "target": "/abs/src/SKILL.md"}
        ]
        result = self._write_and_read(tmp_path, entries)
        assert result[0]["kind"] == "symlink"
        assert result[0]["target"] == "/abs/src/SKILL.md"

    def test_entry_kind_copy(self, tmp_path):
        entries = [
            {"path": ".claude/settings.json", "kind": "copy", "from": "/abs/src/settings.json"}
        ]
        result = self._write_and_read(tmp_path, entries)
        assert result[0]["kind"] == "copy"
        assert result[0]["from"] == "/abs/src/settings.json"

    def test_entry_kind_rendered(self, tmp_path):
        entries = [
            {"path": ".claude/agents/bar.md", "kind": "rendered", "from": "/abs/src/bar.md"}
        ]
        result = self._write_and_read(tmp_path, entries)
        assert result[0]["kind"] == "rendered"
        assert result[0]["from"] == "/abs/src/bar.md"

    def test_entry_kind_marker_block(self, tmp_path):
        entries = [
            {"path": "AGENTS.md", "kind": "marker-block", "block": "clasr:myprovider"}
        ]
        result = self._write_and_read(tmp_path, entries)
        assert result[0]["kind"] == "marker-block"
        assert result[0]["block"] == "clasr:myprovider"

    def test_entry_kind_json_merged_with_keys(self, tmp_path):
        entries = [
            {
                "path": ".claude/settings.json",
                "kind": "json-merged",
                "keys": ["permissions", "tools"],
            }
        ]
        result = self._write_and_read(tmp_path, entries)
        assert result[0]["kind"] == "json-merged"
        assert result[0]["keys"] == ["permissions", "tools"]

    def test_manifest_with_all_entry_kinds(self, tmp_path):
        """A manifest containing all five entry kinds round-trips correctly."""
        entries = [
            {"path": "a", "kind": "symlink", "target": "/t"},
            {"path": "b", "kind": "copy", "from": "/s"},
            {"path": "c", "kind": "rendered", "from": "/r"},
            {"path": "d", "kind": "marker-block", "block": "clasr:p"},
            {"path": "e", "kind": "json-merged", "keys": ["k1", "k2"]},
        ]
        result = self._write_and_read(tmp_path, entries)
        kinds = [e["kind"] for e in result]
        assert kinds == ["symlink", "copy", "rendered", "marker-block", "json-merged"]
