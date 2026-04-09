"""Convert a Claude Code plan file to a CLASI TODO."""

from pathlib import Path
from typing import Optional

from clasi.templates import slugify
from clasi.todo_split import _unique_path


def plan_to_todo(plans_dir: Path, todo_dir: Path) -> Optional[Path]:
    """Copy the most recent plan file to the TODO directory.

    Finds the newest .md in plans_dir, adds ``status: pending``
    frontmatter, writes it to todo_dir, and deletes the original.

    Returns the path of the created TODO file, or None if nothing
    was converted.
    """
    if not plans_dir.is_dir():
        return None

    plan_files = sorted(plans_dir.glob("*.md"), key=lambda p: p.stat().st_mtime)
    if not plan_files:
        return None

    plan_file = plan_files[-1]
    content = plan_file.read_text(encoding="utf-8").strip()
    if not content:
        return None

    # Strip existing frontmatter if present
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            body = parts[2].strip()

    # Extract title from first # heading
    title = None
    for line in body.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    slug = slugify(title) if title else slugify(plan_file.stem)
    if not slug:
        slug = "untitled-plan"

    todo_dir.mkdir(parents=True, exist_ok=True)
    out_path = _unique_path(todo_dir, slug)
    out_path.write_text(f"---\nstatus: pending\n---\n\n{body}\n", encoding="utf-8")

    plan_file.unlink()
    return out_path
