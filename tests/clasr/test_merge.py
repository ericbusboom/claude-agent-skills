"""
tests/clasr/test_merge.py

Tests for clasr.merge — JSON deep-merge for multi-provider passthrough.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from clasr.merge import is_json_passthrough, merge_json_files


# ---------------------------------------------------------------------------
# is_json_passthrough
# ---------------------------------------------------------------------------


def test_is_json_passthrough_true():
    assert is_json_passthrough(Path("settings.json")) is True


def test_is_json_passthrough_false_md():
    assert is_json_passthrough(Path("README.md")) is False


def test_is_json_passthrough_false_toml():
    assert is_json_passthrough(Path("pyproject.toml")) is False


def test_is_json_passthrough_false_txt():
    assert is_json_passthrough(Path("notes.txt")) is False


# ---------------------------------------------------------------------------
# merge_json_files — basic / no conflict
# ---------------------------------------------------------------------------


def test_merge_json_files_missing_existing_raises(tmp_path):
    """FileNotFoundError when existing path does not exist."""
    missing = tmp_path / "nonexistent.json"
    with pytest.raises(FileNotFoundError):
        merge_json_files(missing, {"key": "val"}, "providerA", "providerB")


def test_merge_json_files_basic(tmp_path):
    """No conflicts: merged dict has all keys; keys_contributed == incoming keys."""
    existing = tmp_path / "settings.json"
    existing.write_text(json.dumps({"alpha": 1}))

    incoming = {"beta": 2, "gamma": 3}
    merged, contributed = merge_json_files(existing, incoming, "provA", "provB")

    assert merged == {"alpha": 1, "beta": 2, "gamma": 3}
    assert contributed == ["beta", "gamma"]


def test_merge_json_files_returns_contributed_keys(tmp_path):
    """keys_contributed contains only the incoming top-level keys."""
    existing = tmp_path / "s.json"
    existing.write_text(json.dumps({"existing_key": True}))

    incoming = {"mcpServers": {"my-server": {}}}
    _, contributed = merge_json_files(existing, incoming, "provA", "provB")

    assert contributed == ["mcpServers"]


# ---------------------------------------------------------------------------
# merge_json_files — conflicts
# ---------------------------------------------------------------------------


def test_merge_json_files_conflict_warning(tmp_path, capsys):
    """A top-level key conflict emits a WARNING to stderr naming both providers."""
    existing = tmp_path / "settings.json"
    existing.write_text(json.dumps({"foo": "old"}))

    merge_json_files(existing, {"foo": "new"}, "providerNew", "providerOld")

    captured = capsys.readouterr()
    assert "WARNING" in captured.err
    assert "providerNew" in captured.err
    assert "providerOld" in captured.err
    assert "foo" in captured.err


def test_merge_json_files_conflict_incoming_wins(tmp_path):
    """On conflict at the top level the incoming (provider) value wins."""
    existing = tmp_path / "settings.json"
    existing.write_text(json.dumps({"foo": "old_value"}))

    merged, _ = merge_json_files(
        existing, {"foo": "new_value"}, "providerNew", "providerOld"
    )

    assert merged["foo"] == "new_value"


# ---------------------------------------------------------------------------
# merge_json_files — deep merge
# ---------------------------------------------------------------------------


def test_merge_json_files_deep_merge(tmp_path):
    """Nested dicts are merged recursively rather than replaced."""
    existing = tmp_path / "settings.json"
    existing.write_text(json.dumps({"servers": {"a": 1}}))

    merged, _ = merge_json_files(
        existing, {"servers": {"b": 2}}, "provA", "provB"
    )

    assert merged == {"servers": {"a": 1, "b": 2}}


def test_merge_json_files_non_dict_deeper_level_incoming_wins(tmp_path):
    """When base value is not a dict but overlay is (or vice-versa), overlay wins."""
    existing = tmp_path / "settings.json"
    existing.write_text(json.dumps({"key": "scalar"}))

    merged, _ = merge_json_files(
        existing, {"key": {"nested": True}}, "provA", "provB"
    )

    assert merged["key"] == {"nested": True}
