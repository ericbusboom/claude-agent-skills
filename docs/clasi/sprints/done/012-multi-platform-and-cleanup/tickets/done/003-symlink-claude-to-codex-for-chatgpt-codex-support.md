---
id: '003'
title: Symlink .claude to .codex for ChatGPT Codex support
status: done
use-cases:
- SUC-003
depends-on: []
---

# Symlink .claude to .codex for ChatGPT Codex support

## Description

After `clasi init` creates the `.claude/` directory, create a `.codex`
symlink pointing to `.claude` so ChatGPT Codex picks up the same
skills, rules, and settings.

Use `Path.symlink_to()` with a relative target (`.claude`). Handle:
- Symlink already exists and points to correct target (no-op)
- Symlink exists but points elsewhere (warn and skip)
- Regular file/dir named `.codex` exists (warn and skip)

## Acceptance Criteria

- [ ] `.codex` symlink created pointing to `.claude`
- [ ] Idempotent on re-run
- [ ] Handles existing `.codex` file/dir gracefully

## Testing

- **Existing tests to run**: `uv run python -m pytest tests/unit/test_init_command.py`
- **New tests to write**: Test symlink creation, idempotency, existing file handling
- **Verification command**: `uv run python -m pytest`
