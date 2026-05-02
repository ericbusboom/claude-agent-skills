"""
tests/clasr/test_frontmatter.py

Tests for clasr.frontmatter — union frontmatter parser and projector.
"""

from __future__ import annotations

from pathlib import Path

import yaml
import pytest

from clasr.frontmatter import parse_union, project, render_file


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

UNION_SOURCE = """\
---
name: code-review
description: Review a pull request
claude:
  tools:
    - Read
    - Grep
    - Bash
copilot:
  applyTo: "**/*.ts"
codex:
  model: o3
---

# Body content

Some markdown here.
Another paragraph.
"""

NO_FM_SOURCE = """\
# No Frontmatter

Just body content.
No --- delimiters.
"""

ONLY_SHARED_SOURCE = """\
---
name: shared-only
description: No platform blocks
---

Body with no platform blocks.
"""

OVERRIDE_SOURCE = """\
---
name: base-name
description: shared description
claude:
  name: claude-override
  tools:
    - Read
---

Override body.
"""


def _write(tmp_path: Path, filename: str, content: str) -> Path:
    p = tmp_path / filename
    p.write_text(content, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# parse_union tests
# ---------------------------------------------------------------------------

class TestParseUnion:

    def test_parse_full_union(self, tmp_path):
        """All three platform blocks present; shared and full dicts correct."""
        src = _write(tmp_path, "agent.md", UNION_SOURCE)
        shared_fm, full_fm, body = parse_union(src)

        assert shared_fm == {"name": "code-review", "description": "Review a pull request"}
        assert "claude" in full_fm
        assert "copilot" in full_fm
        assert "codex" in full_fm
        assert full_fm["claude"]["tools"] == ["Read", "Grep", "Bash"]
        assert "name" in full_fm

    def test_body_verbatim(self, tmp_path):
        """Body is returned byte-for-byte after the closing ---."""
        src = _write(tmp_path, "agent.md", UNION_SOURCE)
        _shared_fm, _full_fm, body = parse_union(src)

        expected_body = "\n# Body content\n\nSome markdown here.\nAnother paragraph.\n"
        assert body == expected_body

    def test_parse_no_frontmatter(self, tmp_path):
        """File with no --- delimiters: empty dicts, full content as body."""
        src = _write(tmp_path, "nofm.md", NO_FM_SOURCE)
        shared_fm, full_fm, body = parse_union(src)

        assert shared_fm == {}
        assert full_fm == {}
        assert body == NO_FM_SOURCE

    def test_parse_shared_only(self, tmp_path):
        """Source with shared keys only (no platform blocks)."""
        src = _write(tmp_path, "shared.md", ONLY_SHARED_SOURCE)
        shared_fm, full_fm, body = parse_union(src)

        assert shared_fm == {"name": "shared-only", "description": "No platform blocks"}
        assert full_fm == shared_fm


# ---------------------------------------------------------------------------
# project tests
# ---------------------------------------------------------------------------

class TestProject:

    def _full_fm(self):
        return yaml.safe_load(UNION_SOURCE.split("---\n", 2)[1])

    def test_project_claude(self, tmp_path):
        """Project to claude: shared + claude-specific keys; no copilot/codex."""
        src = _write(tmp_path, "agent.md", UNION_SOURCE)
        _s, full_fm, body = parse_union(src)
        projected, out_body = project(full_fm, body, "claude")

        assert projected["name"] == "code-review"
        assert projected["description"] == "Review a pull request"
        assert projected["tools"] == ["Read", "Grep", "Bash"]
        assert "claude" not in projected
        assert "copilot" not in projected
        assert "codex" not in projected
        assert out_body is body  # same object (verbatim)

    def test_project_copilot(self, tmp_path):
        """Project to copilot: shared + copilot-specific keys; no claude/codex."""
        src = _write(tmp_path, "agent.md", UNION_SOURCE)
        _s, full_fm, body = parse_union(src)
        projected, _body = project(full_fm, body, "copilot")

        assert projected["name"] == "code-review"
        assert projected["description"] == "Review a pull request"
        assert projected["applyTo"] == "**/*.ts"
        assert "claude" not in projected
        assert "codex" not in projected
        assert "copilot" not in projected

    def test_project_codex(self, tmp_path):
        """Project to codex: shared + codex-specific keys; no claude/copilot."""
        src = _write(tmp_path, "agent.md", UNION_SOURCE)
        _s, full_fm, body = parse_union(src)
        projected, _body = project(full_fm, body, "codex")

        assert projected["name"] == "code-review"
        assert projected["model"] == "o3"
        assert "claude" not in projected
        assert "copilot" not in projected
        assert "codex" not in projected

    def test_project_absent_platform(self, tmp_path):
        """Platform key absent in source -> output equals shared fields only."""
        src = _write(tmp_path, "shared.md", ONLY_SHARED_SOURCE)
        _s, full_fm, body = parse_union(src)
        projected, _body = project(full_fm, body, "codex")

        assert projected == {"name": "shared-only", "description": "No platform blocks"}

    def test_project_override(self, tmp_path):
        """Platform-specific key overrides shared key with the same name."""
        src = _write(tmp_path, "override.md", OVERRIDE_SOURCE)
        _s, full_fm, body = parse_union(src)
        projected, _body = project(full_fm, body, "claude")

        # claude.name should override the shared name
        assert projected["name"] == "claude-override"
        assert projected["description"] == "shared description"
        assert projected["tools"] == ["Read"]
        assert "claude" not in projected


# ---------------------------------------------------------------------------
# render_file tests
# ---------------------------------------------------------------------------

class TestRenderFile:

    def test_render_file_round_trip(self, tmp_path):
        """render_file produces valid YAML frontmatter with correct projected fields."""
        src = _write(tmp_path, "agent.md", UNION_SOURCE)
        rendered = render_file(src, "claude")

        # Must start and end with --- delimiters
        assert rendered.startswith("---\n")
        parts = rendered.split("---\n", 2)
        # parts[0] == '', parts[1] == yaml block, parts[2] == rest (blank + body)
        assert len(parts) >= 3
        fm_dict = yaml.safe_load(parts[1])

        assert fm_dict["name"] == "code-review"
        assert fm_dict["tools"] == ["Read", "Grep", "Bash"]
        assert "claude" not in fm_dict
        assert "copilot" not in fm_dict

    def test_render_file_body_preserved(self, tmp_path):
        """Body content is byte-for-byte preserved in render_file output."""
        src = _write(tmp_path, "agent.md", UNION_SOURCE)
        rendered = render_file(src, "claude")

        expected_body = "\n# Body content\n\nSome markdown here.\nAnother paragraph.\n"
        # rendered ends with \n\n<body>; split after second ---
        after_fm = rendered.split("---\n", 2)[2]
        # after_fm starts with \n then the body
        assert after_fm == "\n" + expected_body

    def test_render_file_no_frontmatter_file(self, tmp_path):
        """Source with no frontmatter: render_file still returns delimited block."""
        src = _write(tmp_path, "nofm.md", NO_FM_SOURCE)
        rendered = render_file(src, "claude")

        assert rendered.startswith("---\n")
        # Empty FM -> yaml.dump({}) produces '{}\n' which is valid
        parts = rendered.split("---\n", 2)
        fm_dict = yaml.safe_load(parts[1]) or {}
        assert fm_dict == {}

    def test_render_file_valid_yaml_frontmatter(self, tmp_path):
        """render_file output can be re-parsed as YAML without errors."""
        src = _write(tmp_path, "agent.md", UNION_SOURCE)
        for platform in ("claude", "codex", "copilot"):
            rendered = render_file(src, platform)
            assert rendered.startswith("---\n")
            yaml_block = rendered.split("---\n", 2)[1]
            fm = yaml.safe_load(yaml_block)
            assert isinstance(fm, dict)
