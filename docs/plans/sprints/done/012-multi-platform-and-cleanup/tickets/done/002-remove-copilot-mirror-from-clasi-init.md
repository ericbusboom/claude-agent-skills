---
id: '002'
title: Remove Copilot mirror from clasi init
status: done
use-cases:
- SUC-002
depends-on:
- '001'
---

# Remove Copilot mirror from clasi init

## Description

Remove the `.github/copilot/instructions/` mirror from `clasi init`.
Copilot will pick up instructions from `AGENTS.md` instead.

Delete the loop in `run_init` that copies rules to
`.github/copilot/instructions/` and update/remove the corresponding tests.

## Acceptance Criteria

- [ ] `clasi init` no longer creates `.github/copilot/instructions/`
- [ ] Copilot mirror tests removed or updated
- [ ] Existing non-copilot tests still pass

## Testing

- **Existing tests to run**: `uv run python -m pytest tests/unit/test_init_command.py`
- **New tests to write**: Negative test asserting `.github/copilot/instructions/` is NOT created
- **Verification command**: `uv run python -m pytest`
