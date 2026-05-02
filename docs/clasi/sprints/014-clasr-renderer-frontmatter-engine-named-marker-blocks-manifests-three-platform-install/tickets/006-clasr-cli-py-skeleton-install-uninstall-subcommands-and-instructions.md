---
id: '006'
title: "clasr/cli.py skeleton \u2014 install/uninstall subcommands and --instructions"
status: done
use-cases:
- SUC-001
- SUC-002
- SUC-003
- SUC-004
- SUC-005
depends-on:
- '001'
github-issue: ''
todo: ''
completes_todo: false
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# clasr/cli.py skeleton — install/uninstall subcommands and --instructions

## Description

Build out `clasr/cli.py` with full argument parsing for all supported flags, and implement
the `--instructions` flag completely. The `install` and `uninstall` subcommands will have
all their arguments defined but will dispatch to platform modules that are stubs until
tickets 007-009. Platform wiring is completed in ticket 011.

The CLI uses `argparse` (NOT `click`) to maintain the one-way dependency rule. `clasr`
must not import `clasi`, and `click` is tightly associated with the `clasi` dependency set.

## Acceptance Criteria

- [x] `clasr/cli.py` implements `main()` with `argparse` (no `click`)
- [x] `clasr --instructions` prints the content of `clasr/instructions.md` loaded via
      `importlib.resources`, then exits 0
- [x] `clasr install --help` shows: `--source`, `--provider`, `--claude`, `--codex`,
      `--copilot`, `--copy`, `--target` (defaults to cwd)
- [x] `clasr uninstall --help` shows: `--provider`, `--claude`, `--codex`, `--copilot`,
      `--target`
- [x] `clasr install --source ./asr --provider test --claude` runs without error
      (dispatches to stub platform module; does not crash)
- [x] `clasr uninstall --provider test --claude` runs without error (stub)
- [x] At least one of `--claude`, `--codex`, `--copilot` is required for both subcommands
      (argparse should enforce this or the function should validate and exit 1 with message)
- [x] `--provider` is required for both subcommands
- [x] `--source` is required for `install`; defaults to resolving the asr/ dir
- [x] Module has NO imports from `clasi`

## Implementation Plan

### Approach

Build a complete `argparse`-based CLI. Structure:
1. Top-level parser with `--instructions` flag.
2. Subparsers for `install` and `uninstall`.
3. `install`: `--source PATH`, `--provider NAME`, `--target PATH` (default `.`),
   `--claude`, `--codex`, `--copilot`, `--copy`.
4. `uninstall`: `--provider NAME`, `--target PATH` (default `.`),
   `--claude`, `--codex`, `--copilot`.
5. `--instructions` check happens before subcommand dispatch.

For `importlib.resources` loading: use `importlib.resources.files("clasr").joinpath("instructions.md").read_text()`.

Platform dispatch calls stubbed functions (or prints "not yet implemented") until
ticket 011 wires the real platform modules.

### Files to Modify

- `clasr/cli.py` (expand from stub)

### Testing Plan

Tests can be added to `tests/clasr/test_cli.py` (new file) or deferred to ticket 011
when the platform modules are wired. At minimum, manually verify:
- `clasr --instructions` prints non-empty content
- `clasr install --help` shows all flags
- `clasr install --source /tmp/test --provider x --claude` does not crash
