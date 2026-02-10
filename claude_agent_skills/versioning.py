"""Versioning utilities for the CLASI project.

Version format: <major>.<YYYYMMDD>.<build>

- major: manually bumped for breaking changes (default 0)
- YYYYMMDD: date of the release
- build: auto-incremented within the same date, resets to 1 on new date
"""

import re
import subprocess
from datetime import date
from pathlib import Path


VERSION_PATTERN = re.compile(r"^v?(\d+)\.(\d{8})\.(\d+)$")


def _get_existing_tags() -> list[str]:
    """Return all git tags in the current repository."""
    result = subprocess.run(
        ["git", "tag", "-l"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def compute_next_version(major: int = 0) -> str:
    """Compute the next version string based on existing git tags.

    Scans git tags matching the version pattern, finds the highest build
    number for today's date (or 0 if none), and increments.
    """
    today = date.today().strftime("%Y%m%d")
    max_build = 0

    for tag in _get_existing_tags():
        m = VERSION_PATTERN.match(tag.lstrip("v"))
        if not m:
            continue
        tag_major, tag_date, tag_build = int(m.group(1)), m.group(2), int(m.group(3))
        if tag_major == major and tag_date == today:
            max_build = max(max_build, tag_build)

    return f"{major}.{today}.{max_build + 1}"


def update_pyproject_version(version: str, pyproject_path: Path) -> None:
    """Update the version field in pyproject.toml."""
    content = pyproject_path.read_text(encoding="utf-8")
    updated = re.sub(
        r'^version\s*=\s*"[^"]*"',
        f'version = "{version}"',
        content,
        count=1,
        flags=re.MULTILINE,
    )
    if updated == content:
        raise ValueError(f"Could not find version field in {pyproject_path}")
    pyproject_path.write_text(updated, encoding="utf-8")


def create_version_tag(version: str) -> None:
    """Create a git tag for the given version."""
    tag_name = f"v{version}"
    result = subprocess.run(
        ["git", "tag", tag_name],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to create tag {tag_name}: {result.stderr.strip()}")
