"""
tests/clasr/test_links.py

Tests for clasr.links — symlink-with-copy-fallback helper.
"""

from __future__ import annotations

import os
import warnings
from pathlib import Path

import pytest

from clasr.links import link_or_copy, unlink_alias


# ---------------------------------------------------------------------------
# link_or_copy — symlink path
# ---------------------------------------------------------------------------


def test_link_or_copy_creates_symlink(tmp_path: Path) -> None:
    canonical = tmp_path / "source.txt"
    canonical.write_text("hello")

    alias = tmp_path / "alias.txt"
    result = link_or_copy(canonical, alias)

    assert result == "symlink"
    assert alias.is_symlink()
    assert alias.resolve() == canonical.resolve()


# ---------------------------------------------------------------------------
# link_or_copy — copy mode
# ---------------------------------------------------------------------------


def test_link_or_copy_copy_mode(tmp_path: Path) -> None:
    canonical = tmp_path / "source.txt"
    canonical.write_text("content")

    alias = tmp_path / "alias.txt"
    result = link_or_copy(canonical, alias, copy=True)

    assert result == "copy"
    assert alias.is_file()
    assert not alias.is_symlink()
    assert alias.read_text() == "content"


# ---------------------------------------------------------------------------
# link_or_copy — OSError fallback
# ---------------------------------------------------------------------------


def test_link_or_copy_oserror_fallback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    canonical = tmp_path / "source.txt"
    canonical.write_text("data")

    alias = tmp_path / "alias.txt"

    def failing_symlink(src: object, dst: object) -> None:
        raise OSError("symlinks not supported")

    monkeypatch.setattr(os, "symlink", failing_symlink)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = link_or_copy(canonical, alias)

    assert result == "copy"
    assert alias.is_file()
    assert alias.read_text() == "data"
    assert len(caught) == 1
    assert "falling back to copy" in str(caught[0].message)


# ---------------------------------------------------------------------------
# link_or_copy — creates parent directories
# ---------------------------------------------------------------------------


def test_link_or_copy_creates_parent_dirs(tmp_path: Path) -> None:
    canonical = tmp_path / "source.txt"
    canonical.write_text("x")

    alias = tmp_path / "deep" / "nested" / "alias.txt"
    result = link_or_copy(canonical, alias)

    assert result == "symlink"
    assert alias.is_symlink()
    assert (tmp_path / "deep" / "nested").is_dir()


# ---------------------------------------------------------------------------
# unlink_alias — symlink
# ---------------------------------------------------------------------------


def test_unlink_alias_symlink(tmp_path: Path) -> None:
    canonical = tmp_path / "source.txt"
    canonical.write_text("y")

    alias = tmp_path / "alias.txt"
    os.symlink(canonical, alias)
    assert alias.is_symlink()

    result = unlink_alias(alias)

    assert result is True
    assert not alias.exists()
    assert not alias.is_symlink()


# ---------------------------------------------------------------------------
# unlink_alias — regular file
# ---------------------------------------------------------------------------


def test_unlink_alias_regular_file(tmp_path: Path) -> None:
    regular = tmp_path / "regular.txt"
    regular.write_text("z")

    result = unlink_alias(regular)

    assert result is True
    assert not regular.exists()


# ---------------------------------------------------------------------------
# unlink_alias — not found
# ---------------------------------------------------------------------------


def test_unlink_alias_not_found(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist.txt"

    result = unlink_alias(missing)

    assert result is False
