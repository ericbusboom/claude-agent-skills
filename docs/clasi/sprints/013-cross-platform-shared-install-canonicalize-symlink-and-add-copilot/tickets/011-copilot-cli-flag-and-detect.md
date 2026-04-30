---
id: "013-011"
title: "Wire --copilot flag into CLI and update detect.py"
status: todo
sprint: "013"
use-cases:
  - SUC-005
  - SUC-006
depends-on:
  - "013-006"
---

# 013-011: Wire `--copilot` flag into CLI and update `detect.py`

## Description

Complete the end-to-end wiring so `clasi init --copilot` and `clasi uninstall
--copilot` fully dispatch to `copilot.install` and `copilot.uninstall`.

Also update `detect.py` to recognize Copilot signals, and update the interactive
platform prompt to offer Copilot as a fourth option.

## Acceptance Criteria

- [ ] `clasi init --copilot` runs `copilot.install(target, mcp_config, copy=copy)`.
- [ ] `clasi uninstall --copilot` runs `copilot.uninstall(target)`.
- [ ] `clasi init --claude --codex --copilot` runs all three installers in order.
- [ ] `--copilot` is accepted as a standalone flag (no other platform flags required).
- [ ] Interactive prompt (TTY) offers Copilot as a fourth choice alongside Claude, Codex.
      Recommended default is updated based on `detect.py` Copilot signal.
- [ ] `detect.py` recognizes Copilot signals:
  - `.github/copilot-instructions.md` exists → copilot signal.
  - `.github/agents/` exists → copilot signal.
  - `.github/instructions/` exists (with `*.instructions.md` files) → copilot signal.
  - `code` or `gh` binary on PATH → advisory (not definitive).
- [ ] `PlatformSignals` dataclass (or equivalent) gains a `copilot: bool` field.
- [ ] `detect.py` `recommend_platforms` (or equivalent function) returns `"copilot"`
      in its output when Copilot signals are detected.
- [ ] Detection tests in `tests/unit/test_platform_detect.py` cover Copilot signals.
- [ ] CLI tests confirm `--copilot` is accepted and wired correctly.
- [ ] `python -m pytest --no-cov` green.

## Implementation Plan

### Files to Modify

- `clasi/init_command.py` — add `--copilot / --no-copilot` Click option; update the
  orchestration block to call `copilot.install` when `copilot=True`; update the
  interactive prompt.
- `clasi/uninstall_command.py` — add `--copilot / --no-copilot`; call
  `copilot.uninstall` when set.
- `clasi/cli.py` — add the option at the command decorator if flags are defined there.
- `clasi/platforms/detect.py` — add Copilot signal detection; update `PlatformSignals`.
- `tests/unit/test_init_command.py` — add `--copilot` invocation test.
- `tests/unit/test_platform_detect.py` — add Copilot detection tests.

### Testing Plan

For detection: create a `tmp_path` with `.github/copilot-instructions.md` present;
assert `detect.PlatformSignals(target).copilot is True`. Also test the negative case
(no Copilot files → `copilot is False`).

For CLI: run `clasi init --copilot` in a `tmp_path` and assert `copilot.install` was
called (can use monkeypatch or check for a known output file like
`.github/copilot-instructions.md`).

### Documentation Updates

None — README updated in ticket 012.
