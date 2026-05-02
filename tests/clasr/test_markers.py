"""
tests/clasr/test_markers.py

Tests for clasr.markers — named provider-scoped marker block writer and stripper.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from clasr.markers import write_block, strip_block


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _begin(provider: str) -> str:
    return f"<!-- BEGIN clasr:{provider} -->"


def _end(provider: str) -> str:
    return f"<!-- END clasr:{provider} -->"


def _block(provider: str, content: str) -> str:
    return f"{_begin(provider)}\n{content}\n{_end(provider)}"


# ---------------------------------------------------------------------------
# write_block — creates file when it does not exist
# ---------------------------------------------------------------------------


def test_write_block_creates_file(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    assert not target.exists()

    result = write_block(target, "claude", "hello world")

    assert result is True
    assert target.exists()
    text = target.read_text()
    assert _begin("claude") in text
    assert "hello world" in text
    assert _end("claude") in text


def test_write_block_creates_parent_dirs(tmp_path: Path) -> None:
    target = tmp_path / "deep" / "nested" / "AGENTS.md"
    result = write_block(target, "claude", "content")

    assert result is True
    assert target.exists()
    assert (tmp_path / "deep" / "nested").is_dir()


# ---------------------------------------------------------------------------
# write_block — replaces existing block in place
# ---------------------------------------------------------------------------


def test_write_block_replaces_existing(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    preamble = "# Agents\n\n"
    postscript = "\n## Footer\n"
    initial_block = _block("claude", "old content")
    target.write_text(preamble + initial_block + postscript, encoding="utf-8")

    result = write_block(target, "claude", "new content")

    assert result is True
    text = target.read_text()
    # Updated content
    assert "new content" in text
    assert "old content" not in text
    # Surrounding content preserved
    assert text.startswith(preamble)
    assert postscript in text
    # Exactly one BEGIN and one END
    assert text.count(_begin("claude")) == 1
    assert text.count(_end("claude")) == 1


# ---------------------------------------------------------------------------
# write_block — appends block when file exists without that provider's block
# ---------------------------------------------------------------------------


def test_write_block_appends(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    existing_text = "# Existing content\n"
    target.write_text(existing_text, encoding="utf-8")

    result = write_block(target, "claude", "appended content")

    assert result is True
    text = target.read_text()
    assert text.startswith(existing_text)
    assert "appended content" in text
    assert _begin("claude") in text
    assert _end("claude") in text


def test_write_block_appends_no_double_newline(tmp_path: Path) -> None:
    """File ending without newline should not produce double blank line."""
    target = tmp_path / "AGENTS.md"
    target.write_text("no trailing newline", encoding="utf-8")

    write_block(target, "claude", "content")
    text = target.read_text()
    # There should be exactly one newline separating old text from block.
    assert "no trailing newline\n" + _begin("claude") in text


# ---------------------------------------------------------------------------
# write_block — returns False when content is unchanged
# ---------------------------------------------------------------------------


def test_write_block_unchanged(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    write_block(target, "claude", "same content")
    # Second call with identical content.
    result = write_block(target, "claude", "same content")

    assert result is False


# ---------------------------------------------------------------------------
# write_block — preserves other providers' blocks
# ---------------------------------------------------------------------------


def test_write_block_two_providers(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    write_block(target, "claude", "claude content")
    write_block(target, "copilot", "copilot content")

    text = target.read_text()
    assert _begin("claude") in text
    assert "claude content" in text
    assert _begin("copilot") in text
    assert "copilot content" in text

    # Re-write one provider; other must be untouched.
    write_block(target, "claude", "updated claude")
    text = target.read_text()
    assert "updated claude" in text
    assert "copilot content" in text
    assert _begin("copilot") in text
    assert _end("copilot") in text


def test_write_block_preserves_other_providers(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    # Pre-populate with two blocks.
    initial = (
        _block("claude", "c content")
        + "\n"
        + _block("codex", "x content")
        + "\n"
    )
    target.write_text(initial, encoding="utf-8")

    write_block(target, "claude", "c updated")
    text = target.read_text()

    assert "c updated" in text
    assert "x content" in text
    assert _begin("codex") in text
    assert _end("codex") in text


# ---------------------------------------------------------------------------
# strip_block — removes only the named block
# ---------------------------------------------------------------------------


def test_strip_block_removes(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    content = "before\n" + _block("claude", "content") + "\nafter\n"
    target.write_text(content, encoding="utf-8")

    result = strip_block(target, "claude")

    assert result is True
    text = target.read_text()
    assert _begin("claude") not in text
    assert _end("claude") not in text
    assert "content" not in text
    assert "before" in text
    assert "after" in text


# ---------------------------------------------------------------------------
# strip_block — no-op when block not present
# ---------------------------------------------------------------------------


def test_strip_block_not_found(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    original = "some text\n"
    target.write_text(original, encoding="utf-8")

    result = strip_block(target, "claude")

    assert result is False
    assert target.read_text() == original


def test_strip_block_missing_file(tmp_path: Path) -> None:
    target = tmp_path / "missing.md"
    result = strip_block(target, "claude")
    assert result is False


# ---------------------------------------------------------------------------
# strip_block — deletes file when empty after stripping
# ---------------------------------------------------------------------------


def test_strip_block_deletes_empty_file(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    # Block is the entire file content.
    write_block(target, "claude", "only content")
    assert target.exists()

    result = strip_block(target, "claude")

    assert result is True
    assert not target.exists()


def test_strip_block_deletes_whitespace_only_file(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    target.write_text("\n" + _block("claude", "x") + "\n", encoding="utf-8")

    result = strip_block(target, "claude")

    assert result is True
    assert not target.exists()


# ---------------------------------------------------------------------------
# strip_block — multi-provider coexistence
# ---------------------------------------------------------------------------


def test_multi_provider_coexistence(tmp_path: Path) -> None:
    """Strip one provider's block; the other must survive intact."""
    target = tmp_path / "AGENTS.md"
    write_block(target, "claude", "claude stuff")
    write_block(target, "codex", "codex stuff")

    result = strip_block(target, "claude")

    assert result is True
    assert target.exists()
    text = target.read_text()
    assert _begin("claude") not in text
    assert _end("claude") not in text
    assert "claude stuff" not in text
    # Codex block fully intact.
    assert _begin("codex") in text
    assert _end("codex") in text
    assert "codex stuff" in text


def test_strip_block_preserves_regular_text_and_other_blocks(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    body = (
        "# Header\n\n"
        + _block("claude", "claude block")
        + "\n\n"
        + "Some plain text.\n\n"
        + _block("copilot", "copilot block")
        + "\n"
    )
    target.write_text(body, encoding="utf-8")

    strip_block(target, "claude")
    text = target.read_text()

    assert "# Header" in text
    assert "Some plain text." in text
    assert _begin("copilot") in text
    assert "copilot block" in text
    assert _end("copilot") in text
    assert _begin("claude") not in text
    assert "claude block" not in text
