"""
clasr/platforms/detect.py

Read-only detection of which clasr-managed platforms and providers are
installed in a target directory.

Public API:
    detect(target: Path) -> dict[str, list[str]]

Detection rules:
    - Claude:  target/.claude/.clasr-manifest/*.json  → stems = providers
    - Codex:   target/.codex/.clasr-manifest/*.json   → stems = providers
    - Copilot: target/.github/.clasr-manifest/*.json  → stems = providers

Missing platform directories result in an empty list for that platform.
Lists are sorted for determinism.

No imports from clasi.
"""

from __future__ import annotations

from pathlib import Path

# Map of platform name → platform directory name (relative to target).
_PLATFORM_DIRS: dict[str, str] = {
    "claude": ".claude",
    "codex": ".codex",
    "copilot": ".github",
}


def detect(target: Path) -> dict[str, list[str]]:
    """Detect which clasr-managed providers are installed in *target*.

    Parameters
    ----------
    target:
        The project root to inspect.

    Returns
    -------
    dict[str, list[str]]
        A dict with keys ``"claude"``, ``"codex"``, and ``"copilot"``.
        Each value is a sorted list of provider names (manifest file stems)
        found under ``<platform_dir>/.clasr-manifest/``.  An absent
        platform directory yields an empty list — never raises.
    """
    result: dict[str, list[str]] = {}

    for platform, dir_name in _PLATFORM_DIRS.items():
        manifest_dir = target / dir_name / ".clasr-manifest"
        if manifest_dir.is_dir():
            providers = sorted(
                p.stem for p in manifest_dir.glob("*.json") if p.is_file()
            )
        else:
            providers = []
        result[platform] = providers

    return result
