---
id: "003"
title: "Add clasi/platforms/detect.py — advisory platform detection"
status: todo
use-cases:
  - SUC-006
  - SUC-009
depends-on: []
github-issue: ""
todo: ""
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Add clasi/platforms/detect.py — advisory platform detection

## Description

Add a new module `clasi/platforms/detect.py` that inspects advisory signals to recommend
a platform (Claude, Codex, or both) without making any irreversible decisions. The module
is read-only and has no side effects. It is used by the interactive branch of `clasi init`
(ticket 005) and `clasi uninstall` (ticket 007) to present a recommendation to the user.

This ticket can run in parallel with ticket 002 since it creates a new file only.

## Acceptance Criteria

- [ ] `clasi/platforms/detect.py` exists.
- [ ] The module defines a `PlatformSignals` dataclass with at least:
      `claude_score: int`, `codex_score: int`, `recommendation: str`
      (values: `"claude"`, `"codex"`, or `"both"`).
- [ ] `detect_platforms(target: Path) -> PlatformSignals` is the public function.
- [ ] Detection inspects:
  - Project files: presence of `.claude/`, `CLAUDE.md`, `.codex/`, `.agents/skills/`,
    `AGENTS.md` under `target`.
  - Installed commands: `claude`, `codex` (via `shutil.which`).
  - User config directories: `~/.claude`, `~/.codex`.
  - Environment variable names only: `ANTHROPIC_API_KEY`, `CLAUDE_*`, `OPENAI_API_KEY`,
    `CODEX_*`. Values are never read or printed.
- [ ] `detect_platforms` is side-effect-free (read-only, no file writes, no network calls,
      no running subprocesses beyond `shutil.which`).
- [ ] Tests in `tests/unit/test_platform_detect.py` cover:
  - Claude-only signals → `recommendation == "claude"`.
  - Codex-only signals → `recommendation == "codex"`.
  - Both signals → `recommendation == "both"`.
  - No signals → either `"claude"` (safe default) or `"both"` (per spec fallback).
  - Env var name detection without reading values (mock `os.environ` keys only).

## Implementation Plan

### Files to create

- `clasi/platforms/detect.py`
- `tests/unit/test_platform_detect.py`

### Approach

Recommendation algorithm:
- Each detected Claude signal adds 1 to `claude_score`. Each Codex signal adds 1 to
  `codex_score`.
- Priority: project-configured platform wins if one side has project files and the other
  does not.
- If both have project files: recommend `"both"`.
- If neither has project files but user-level signals exist: use scores.
- If both scores are zero: default to `"claude"` (backward compat).

Signal weights (suggested, implementer may adjust):
- Project-level file present: +2
- Installed command: +1
- User config directory: +1
- Env var name present: +1

Recommendation thresholds:
- If `claude_score > 0` and `codex_score == 0`: `"claude"`.
- If `codex_score > 0` and `claude_score == 0`: `"codex"`.
- If both > 0: `"both"`.
- If both == 0: `"claude"`.

### Testing plan

Use `tmp_path` fixtures to create project files. Mock `shutil.which` for command
detection. Mock `os.environ` (keys only) for env var detection. Mock `Path.home()`
for user config dirs.

```
uv run pytest tests/unit/test_platform_detect.py -v
uv run pytest -x
```

### Documentation updates

None — internal module, not user-facing beyond the CLI prompt behavior in ticket 006.
