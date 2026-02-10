"""Tests for claude_agent_skills.frontmatter module."""

import pytest
from pathlib import Path

from claude_agent_skills.frontmatter import read_document, read_frontmatter, write_frontmatter


@pytest.fixture
def tmp_md(tmp_path):
    """Return a helper that writes content to a temp .md file and returns its path."""
    def _write(content: str) -> Path:
        p = tmp_path / "test.md"
        p.write_text(content, encoding="utf-8")
        return p
    return _write


class TestReadDocument:
    def test_basic(self, tmp_md):
        p = tmp_md("---\ntitle: Hello\nstatus: draft\n---\nBody text.\n")
        fm, body = read_document(p)
        assert fm == {"title": "Hello", "status": "draft"}
        assert body == "Body text.\n"

    def test_no_frontmatter(self, tmp_md):
        p = tmp_md("Just a plain file.\n")
        fm, body = read_document(p)
        assert fm == {}
        assert body == "Just a plain file.\n"

    def test_empty_frontmatter(self, tmp_md):
        p = tmp_md("---\n---\nBody only.\n")
        fm, body = read_document(p)
        assert fm == {}
        assert body == "Body only.\n"

    def test_no_closing_delimiter(self, tmp_md):
        p = tmp_md("---\ntitle: oops\nno closing\n")
        fm, body = read_document(p)
        assert fm == {}
        assert body == "---\ntitle: oops\nno closing\n"

    def test_list_in_frontmatter(self, tmp_md):
        p = tmp_md("---\nid: \"001\"\nuse-cases: [UC-001, UC-002]\n---\n# Title\n")
        fm, body = read_document(p)
        assert fm["id"] == "001"
        assert fm["use-cases"] == ["UC-001", "UC-002"]
        assert body == "# Title\n"

    def test_multiline_body(self, tmp_md):
        content = "---\nk: v\n---\nLine 1\nLine 2\nLine 3\n"
        p = tmp_md(content)
        fm, body = read_document(p)
        assert fm == {"k": "v"}
        assert body == "Line 1\nLine 2\nLine 3\n"


class TestReadFrontmatter:
    def test_returns_dict(self, tmp_md):
        p = tmp_md("---\nstatus: todo\n---\n# Heading\n")
        assert read_frontmatter(p) == {"status": "todo"}

    def test_no_frontmatter(self, tmp_md):
        p = tmp_md("No front matter here.\n")
        assert read_frontmatter(p) == {}


class TestWriteFrontmatter:
    def test_update_existing(self, tmp_md):
        p = tmp_md("---\nstatus: todo\n---\n# My Doc\n\nBody.\n")
        write_frontmatter(p, {"status": "done", "title": "My Doc"})
        fm, body = read_document(p)
        assert fm["status"] == "done"
        assert fm["title"] == "My Doc"
        assert "# My Doc" in body
        assert "Body." in body

    def test_create_new_file(self, tmp_path):
        p = tmp_path / "new.md"
        write_frontmatter(p, {"id": "001", "title": "New"})
        fm, body = read_document(p)
        assert fm == {"id": "001", "title": "New"}
        assert body == ""

    def test_round_trip(self, tmp_md):
        original_body = "# Sprint 001\n\nSome content here.\n"
        p = tmp_md(f"---\nid: \"001\"\ntitle: Test Sprint\nstatus: planning\n---\n{original_body}")
        fm, body = read_document(p)
        assert body == original_body
        fm["status"] = "active"
        write_frontmatter(p, fm)
        fm2, body2 = read_document(p)
        assert fm2["status"] == "active"
        assert fm2["id"] == "001"
        assert body2 == original_body

    def test_prepend_to_plain_file(self, tmp_md):
        p = tmp_md("Plain content.\n")
        write_frontmatter(p, {"status": "new"})
        fm, body = read_document(p)
        assert fm == {"status": "new"}
        assert body == "Plain content.\n"
