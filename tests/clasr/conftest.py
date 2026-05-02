"""
tests/clasr/conftest.py

Shared fixture helpers for clasr platform tests.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

#: Sentinel meaning "use the default settings.json content".
_DEFAULT_SETTINGS = object()


def make_asr_dir(
    tmp_path: Path,
    provider: str = "testprov",
    skill_names: Sequence[str] = ("foo",),
    settings_keys: dict | None | object = _DEFAULT_SETTINGS,
    extra_passthrough: dict[str, str] | None = None,
) -> Path:
    """Create a complete fixture asr/ directory under *tmp_path* and return its path.

    Layout created:
        asr/AGENTS.md
        asr/skills/<name>/SKILL.md          — one per skill_names
        asr/agents/code-review.md           — union frontmatter (claude + codex + copilot)
        asr/rules/lint.md                   — union frontmatter (claude + codex + copilot)
        asr/claude/settings.json            — parameterized by settings_keys (see below)
        asr/codex/something.md              — passthrough file
        asr/copilot/something.md            — passthrough file

    Args:
        tmp_path:          Base directory under which asr/ is created.
        provider:          Provider name (used in AGENTS.md preamble text).
        skill_names:       Names of skill directories to create under skills/.
        settings_keys:     Controls claude/settings.json:
                           - omitted (default): write {"model": "sonnet", "permissions": ["read"]}
                           - dict: write exactly this dict as the settings file content
                           - None: do NOT create settings.json at all
        extra_passthrough: Optional extra files to create relative to the asr/ source root.
                           Keys are paths relative to ``asr/`` (e.g. ``"claude/commands/foo.md"``),
                           values are the file content strings.
    """
    src = tmp_path / "asr"
    src.mkdir(parents=True, exist_ok=True)

    # AGENTS.md — content that all platforms will embed in their marker blocks
    (src / "AGENTS.md").write_text(
        f"Use clasr to manage multi-platform AI agent configurations.\n"
        f"Provider: {provider}\n",
        encoding="utf-8",
    )

    # skills/<name>/SKILL.md
    for name in skill_names:
        skill_dir = src / "skills" / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"# {name}\nDoes stuff for {name}.\n",
            encoding="utf-8",
        )

    # agents/code-review.md — union frontmatter for all three platforms
    agents_dir = src / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / "code-review.md").write_text(
        "---\n"
        "name: code-review\n"
        "description: Review a PR\n"
        "claude:\n"
        "  tools: [Read, Bash]\n"
        "codex: {}\n"
        "copilot: {}\n"
        "---\n\n"
        "Review the pull request carefully.\n",
        encoding="utf-8",
    )

    # rules/lint.md — union frontmatter for all three platforms
    rules_dir = src / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    (rules_dir / "lint.md").write_text(
        "---\n"
        "description: Lint rules\n"
        "claude: {}\n"
        "codex: {}\n"
        "copilot:\n"
        "  applyTo: '**'\n"
        "---\n\n"
        "Always write clean code.\n",
        encoding="utf-8",
    )

    # claude/settings.json — passthrough for Claude platform
    claude_pass = src / "claude"
    claude_pass.mkdir(parents=True, exist_ok=True)
    if settings_keys is _DEFAULT_SETTINGS:
        # Backward-compatible default: write base settings.
        content: dict = {"model": "sonnet", "permissions": ["read"]}
        (claude_pass / "settings.json").write_text(json.dumps(content), encoding="utf-8")
    elif settings_keys is None:
        # Caller explicitly requested no settings.json.
        pass
    else:
        # Caller provided an exact dict — write it verbatim.
        (claude_pass / "settings.json").write_text(
            json.dumps(settings_keys),  # type: ignore[arg-type]
            encoding="utf-8",
        )

    # codex/something.md — passthrough file for Codex platform
    codex_pass = src / "codex"
    codex_pass.mkdir(parents=True, exist_ok=True)
    (codex_pass / "something.md").write_text(
        "# Codex passthrough\nThis file is passed through to .codex/.\n",
        encoding="utf-8",
    )

    # copilot/something.md — passthrough file for Copilot platform
    copilot_pass = src / "copilot"
    copilot_pass.mkdir(parents=True, exist_ok=True)
    (copilot_pass / "something.md").write_text(
        "# Copilot passthrough\nThis file is passed through to .github/.\n",
        encoding="utf-8",
    )

    # Extra passthrough files (e.g. claude/commands/foo.md).
    if extra_passthrough:
        for rel_path, file_content in extra_passthrough.items():
            dest = src / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(file_content, encoding="utf-8")

    return src
