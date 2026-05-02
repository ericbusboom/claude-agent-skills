---
id: '011'
title: Wire CLI install/uninstall to platform modules
status: done
use-cases:
- SUC-001
- SUC-003
- SUC-004
- SUC-005
depends-on:
- '007'
- 008
- 009
github-issue: ''
todo: ''
completes_todo: false
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Wire CLI install/uninstall to platform modules

## Description

Connect `clasr/cli.py`'s `install` and `uninstall` subcommands to the real platform
modules (`claude.py`, `codex.py`, `copilot.py`). Replace the stub dispatch with actual
calls to `platform.install(source, target, provider, copy)` and
`platform.uninstall(target, provider)`. After this ticket, the end-to-end flow works:
`clasr install --source ./asr --provider test --claude --codex --copilot` installs all
three platforms correctly.

Also write `tests/clasr/test_cli.py` covering the CLI integration paths.

## Acceptance Criteria

- [x] `clasr install --source <path> --provider <name> --claude` installs the Claude
      platform: skills symlinked, agents rendered, marker blocks written, manifest created
- [x] `clasr install --source <path> --provider <name> --codex` installs Codex similarly
- [x] `clasr install --source <path> --provider <name> --copilot` installs Copilot similarly
- [x] `clasr install ... --claude --codex --copilot` installs all three in sequence
- [x] `clasr uninstall --provider <name> --claude` reads the Claude manifest and removes
      all Claude entries for that provider
- [x] `clasr install --copy ...` passes `copy=True` to platform modules
- [x] Error exit (code 1) with message if no platform flag is given to install or uninstall
- [x] Error exit (code 1) with message if `--provider` is missing
- [x] All existing `clasi` tests still pass: `uv run pytest tests/unit/`

## Implementation Plan

### Approach

Replace stub dispatch in `cli.py` with:
```python
from clasr.platforms import claude, codex, copilot
```
For each selected platform flag, call the corresponding `install()` or `uninstall()`.
Thread `copy` and `target` through.

Validate that at least one platform flag is given; validate `--provider` is present.

### Files to Modify

- `clasr/cli.py`

### Files to Create

- `tests/clasr/test_cli.py`

### Testing Plan

`tests/clasr/test_cli.py` using `subprocess.run` or monkeypatching `sys.argv`:
- `test_install_claude_end_to_end`: create fixture `asr/` in tmpdir; run `main()` with
  `install --source ... --provider test --claude`; assert manifest exists and is valid
- `test_install_no_platform_flag`: assert exits with code 1
- `test_install_no_provider`: assert exits with code 1
- `test_uninstall_after_install`: install then uninstall via CLI; assert manifest deleted
- `test_instructions_flag`: capture stdout; assert non-empty Markdown content printed
