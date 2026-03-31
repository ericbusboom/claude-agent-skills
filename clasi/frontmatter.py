"""
Utility for reading and writing YAML frontmatter in markdown files.

Frontmatter is delimited by --- lines at the top of a file:

    ---
    key: value
    ---

    Body content here.
"""

from pathlib import Path
from typing import Any

import yaml


def read_document(path: str | Path) -> tuple[dict[str, Any], str]:
    """Read a markdown file and return (frontmatter_dict, body_str).

    If the file has no frontmatter, returns ({}, full_content).
    """
    path = Path(path)
    content = path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return {}, content

    # Find the closing ---
    end = content.find("---", 3)
    if end == -1:
        return {}, content

    # Find the actual end of the closing --- line
    end_of_line = content.find("\n", end)
    if end_of_line == -1:
        end_of_line = len(content)

    yaml_str = content[3:end].strip()
    body = content[end_of_line + 1:]

    if not yaml_str:
        return {}, body

    frontmatter = yaml.safe_load(yaml_str)
    if not isinstance(frontmatter, dict):
        return {}, content

    return frontmatter, body


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

    yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False).strip()
    content = f"---\n{yaml_str}\n---\n{body}"
    path.write_text(content, encoding="utf-8")
