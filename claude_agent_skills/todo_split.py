"""TODO file splitting logic for the clasi CLI.

Splits markdown files in docs/plans/todo/ that contain multiple level-1
headings into individual files, one per heading.
"""

import re
from pathlib import Path

from claude_agent_skills.templates import slugify


def _parse_sections(content: str) -> list[tuple[str, str]]:
    """Parse markdown content into sections split by level-1 headings.

    Returns a list of (heading, body) tuples. Content before the first
    heading is prepended to the first section's body.
    """
    lines = content.split("\n")
    sections: list[tuple[str, str]] = []
    current_heading = ""
    current_lines: list[str] = []
    preamble_lines: list[str] = []

    for line in lines:
        if re.match(r"^# ", line):
            if current_heading:
                sections.append((current_heading, "\n".join(current_lines)))
            current_heading = line
            current_lines = []
        elif current_heading:
            current_lines.append(line)
        else:
            preamble_lines.append(line)

    # Flush last section
    if current_heading:
        sections.append((current_heading, "\n".join(current_lines)))

    # Prepend preamble to first section's body
    if preamble_lines and sections:
        preamble = "\n".join(preamble_lines)
        heading, body = sections[0]
        sections[0] = (heading, preamble + "\n" + body if body else preamble)

    return sections


def _unique_path(directory: Path, slug: str) -> Path:
    """Return a unique .md path in directory, appending a number if needed."""
    candidate = directory / f"{slug}.md"
    if not candidate.exists():
        return candidate
    n = 2
    while True:
        candidate = directory / f"{slug}-{n}.md"
        if not candidate.exists():
            return candidate
        n += 1


def split_todo_files(todo_dir: Path) -> list[str]:
    """Split multi-heading TODO files into individual files.

    Args:
        todo_dir: Path to the docs/plans/todo/ directory.

    Returns:
        List of action messages describing what was done.
    """
    actions: list[str] = []

    if not todo_dir.exists():
        return actions

    for md_file in sorted(todo_dir.glob("*.md")):
        # Skip files in subdirectories (e.g., done/)
        if md_file.parent != todo_dir:
            continue

        content = md_file.read_text(encoding="utf-8")
        sections = _parse_sections(content)

        if len(sections) <= 1:
            continue

        # Split into individual files
        for heading, body in sections:
            title = heading.lstrip("# ").strip()
            slug = slugify(title)
            if not slug:
                slug = "untitled"
            out_path = _unique_path(todo_dir, slug)
            out_content = heading + "\n" + body
            # Strip trailing whitespace but ensure final newline
            out_content = out_content.rstrip() + "\n"
            out_path.write_text(out_content, encoding="utf-8")
            actions.append(f"  Created: {out_path.name} ({title})")

        md_file.unlink()
        actions.append(f"  Deleted: {md_file.name} (split into {len(sections)} files)")

    return actions
