"""
Utility for reading and writing YAML frontmatter in markdown files.

Frontmatter is delimited by --- lines at the top of a file:

    ---
    key: value
    ---

    Body content here.

Implemented using the python-frontmatter package.
"""

from pathlib import Path
from typing import Any

import frontmatter as _fm
import yaml


def read_document(path: str | Path) -> tuple[dict[str, Any], str]:
    """Read a markdown file and return (frontmatter_dict, body_str).

    If the file has no frontmatter, returns ({}, full_content).
    """
    path = Path(path)
    content = path.read_text(encoding="utf-8")
    return _parse(content)


def _parse(content: str) -> tuple[dict[str, Any], str]:
    """Parse a string and return (frontmatter_dict, body_str).

    Preserves the exact body text as it appears in the file after the
    closing ``---`` delimiter.
    """
    if not content.startswith("---"):
        return {}, content

    # Use python-frontmatter to extract metadata
    post = _fm.loads(content)
    metadata = dict(post.metadata)

    if not metadata:
        # No frontmatter or empty frontmatter — fall back to raw parse
        # to return the full content as body (matching original behaviour).
        end = content.find("---", 3)
        if end == -1:
            return {}, content
        end_of_line = content.find("\n", end)
        if end_of_line == -1:
            end_of_line = len(content)
        body = content[end_of_line + 1:]
        return {}, body

    # Locate the body start in the raw content so we return exactly
    # what follows the closing ---, including any leading/trailing newlines.
    end = content.find("---", 3)
    if end == -1:
        return {}, content
    end_of_line = content.find("\n", end)
    if end_of_line == -1:
        end_of_line = len(content)
    body = content[end_of_line + 1:]

    return metadata, body


def read_frontmatter(path: str | Path) -> dict[str, Any]:
    """Read just the YAML frontmatter from a markdown file.

    Returns an empty dict if the file has no frontmatter.
    """
    fm, _ = read_document(path)
    return fm


def write_frontmatter(path: str | Path, data: dict[str, Any]) -> None:
    """Update the YAML frontmatter of a markdown file, preserving the body.

    If the file has no existing frontmatter, prepends it.
    """
    path = Path(path)

    if path.exists():
        _, body = read_document(path)
    else:
        body = ""

    _write_document(path, data, body)


def _write_document(path: Path, data: dict[str, Any], body: str) -> None:
    """Write frontmatter + body to path in the canonical format."""
    yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False).strip()
    content = f"---\n{yaml_str}\n---\n{body}"
    path.write_text(content, encoding="utf-8")
