"""
tests/unit/test_links.py

Unit tests for clasi/platforms/_links.py.

Uses real filesystem operations via the ``tmp_path`` pytest fixture.
The OSError fallback path is exercised with ``monkeypatch``.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from clasi.platforms._links import link_or_copy, migrate_to_symlink, unlink_alias


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write(path: Path, content: bytes = b"hello") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


# ---------------------------------------------------------------------------
# link_or_copy — symlink path
# ---------------------------------------------------------------------------


def test_link_or_copy_symlink(tmp_path: Path) -> None:
    canonical = _write(tmp_path / "canonical.txt")
    alias = tmp_path / "subdir" / "alias.txt"

    result = link_or_copy(canonical, alias)

    assert result == "symlink"
    assert alias.is_symlink()
    assert alias.resolve() == canonical.resolve()


def test_link_or_copy_creates_parent_dir(tmp_path: Path) -> None:
    canonical = _write(tmp_path / "canonical.txt")
    alias = tmp_path / "a" / "b" / "c" / "alias.txt"

    link_or_copy(canonical, alias)

    assert alias.parent.is_dir()
    assert alias.is_symlink()


# ---------------------------------------------------------------------------
# link_or_copy — copy path (copy=True)
# ---------------------------------------------------------------------------


def test_link_or_copy_copy_flag(tmp_path: Path) -> None:
    content = b"copy me"
    canonical = _write(tmp_path / "canonical.txt", content)
    alias = tmp_path / "alias.txt"

    result = link_or_copy(canonical, alias, copy=True)

    assert result == "copy"
    assert not alias.is_symlink()
    assert alias.read_bytes() == content


def test_link_or_copy_copy_flag_creates_parent_dir(tmp_path: Path) -> None:
    canonical = _write(tmp_path / "canonical.txt")
    alias = tmp_path / "deep" / "alias.txt"

    link_or_copy(canonical, alias, copy=True)

    assert alias.parent.is_dir()
    assert alias.read_bytes() == canonical.read_bytes()


# ---------------------------------------------------------------------------
# link_or_copy — fallback path (OSError on os.symlink)
# ---------------------------------------------------------------------------


def test_link_or_copy_fallback_on_oserror(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    content = b"fallback content"
    canonical = _write(tmp_path / "canonical.txt", content)
    alias = tmp_path / "alias.txt"

    def _raise(*args: object, **kwargs: object) -> None:
        raise OSError("symlinks not permitted in this environment")

    monkeypatch.setattr(os, "symlink", _raise)

    with pytest.warns(UserWarning, match="falling back to copy"):
        result = link_or_copy(canonical, alias)

    assert result == "copy"
    assert not alias.is_symlink()
    assert alias.read_bytes() == content


# ---------------------------------------------------------------------------
# unlink_alias — symlink removal
# ---------------------------------------------------------------------------


def test_unlink_alias_removes_symlink(tmp_path: Path) -> None:
    canonical = _write(tmp_path / "canonical.txt")
    alias = tmp_path / "alias.txt"
    os.symlink(canonical, alias)

    result = unlink_alias(alias)

    assert result is True
    assert not alias.exists()
    # canonical must be untouched
    assert canonical.exists()


def test_unlink_alias_removes_regular_file(tmp_path: Path) -> None:
    canonical = _write(tmp_path / "canonical.txt")
    alias = _write(tmp_path / "alias.txt", b"copy content")

    result = unlink_alias(alias)

    assert result is True
    assert not alias.exists()
    # canonical must be untouched
    assert canonical.exists()


def test_unlink_alias_returns_false_when_not_found(tmp_path: Path) -> None:
    alias = tmp_path / "nonexistent.txt"

    result = unlink_alias(alias)

    assert result is False


# ---------------------------------------------------------------------------
# migrate_to_symlink — all four return values
# ---------------------------------------------------------------------------


def test_migrate_already_symlink(tmp_path: Path) -> None:
    canonical = _write(tmp_path / "canonical.txt")
    alias = tmp_path / "alias.txt"
    os.symlink(canonical, alias)

    result = migrate_to_symlink(canonical, alias)

    assert result == "already-symlink"
    # still a symlink, still points at canonical
    assert alias.is_symlink()
    assert alias.resolve() == canonical.resolve()


def test_migrate_content_matching_file(tmp_path: Path) -> None:
    content = b"shared content"
    canonical = _write(tmp_path / "canonical.txt", content)
    alias = _write(tmp_path / "alias.txt", content)

    result = migrate_to_symlink(canonical, alias)

    assert result == "migrated"
    assert alias.is_symlink()
    assert alias.resolve() == canonical.resolve()


def test_migrate_conflict(tmp_path: Path) -> None:
    canonical = _write(tmp_path / "canonical.txt", b"canonical content")
    alias = _write(tmp_path / "alias.txt", b"different content")

    result = migrate_to_symlink(canonical, alias)

    assert result == "conflict"
    # alias must be untouched
    assert alias.read_bytes() == b"different content"
    assert not alias.is_symlink()


def test_migrate_not_found(tmp_path: Path) -> None:
    canonical = _write(tmp_path / "canonical.txt")
    alias = tmp_path / "nonexistent.txt"

    result = migrate_to_symlink(canonical, alias)

    assert result == "not-found"
