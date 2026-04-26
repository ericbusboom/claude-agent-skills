---
id: "006"
title: "Add interactive platform prompt to clasi init"
status: todo
use-cases:
  - SUC-006
depends-on:
  - "003"
  - "005"
github-issue: ""
todo: ""
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Add interactive platform prompt to clasi init

## Description

When `clasi init` is run interactively with no `--claude` or `--codex` flag, CLASI
should inspect platform signals and prompt the user to choose Claude, Codex, or both,
with a recommended default based on the detected signals.

Non-interactive mode (no tty, no flags) keeps the existing behavior: defaults to Claude
only without prompting.

This ticket wires the `detect.py` module (ticket 003) into the `init_command` interactive
path. Depends on tickets 003 and 005.

## Acceptance Criteria

- [ ] Interactive `clasi init` (no flags, tty attached) presents:
      "Install for: [1] Claude  [2] Codex  [3] Both  (recommended: X)".
- [ ] The user's selection determines which platform installer runs.
- [ ] Non-interactive `clasi init` (no flags, no tty) defaults to Claude only without
      prompting (SUC-001 preserved).
- [ ] The prompt never reads environment variable values — only names.
- [ ] The recommended option is driven by `detect_platforms(target)` from ticket 003.
- [ ] Tests in `tests/unit/test_init_interactive.py` cover:
  - Non-interactive path: no prompt called, Claude installed.
  - Interactive path with Claude recommendation: prompt presented, user selects 1.
  - Interactive path with Codex recommendation: prompt presented, user selects 2.
  - Interactive path with both: prompt presented, user selects 3.

## Implementation Plan

### Files to modify

- `clasi/init_command.py` — add interactive detection branch

### Files to create

- `tests/unit/test_init_interactive.py`

### Approach

In `run_init`, after determining that neither `claude` nor `codex` is set:

```python
import sys
interactive = sys.stdin.isatty() and sys.stdout.isatty()

if not claude and not codex:
    if interactive:
        from clasi.platforms.detect import detect_platforms
        signals = detect_platforms(target_path)
        rec = signals.recommendation
        choice = _prompt_platform(rec)
        claude = choice in ("claude", "both")
        codex = choice in ("codex", "both")
    else:
        claude = True  # non-interactive default
```

`_prompt_platform(recommendation: str) -> str` is a private helper in `init_command.py`
that uses `click.prompt` with a choice list:
- Displays `[1] Claude`, `[2] Codex`, `[3] Both`.
- Pre-selects the recommended option as the default.
- Returns `"claude"`, `"codex"`, or `"both"`.

### Testing plan

Use `CliRunner(mix_stderr=False)` with `input` to simulate user input. To test non-
interactive, run `run_init` directly with a non-tty stdin.

```
uv run pytest tests/unit/test_init_interactive.py -v
uv run pytest -x
```

### Documentation updates

Update `clasi init` docstring in `cli.py` to mention interactive behavior.
