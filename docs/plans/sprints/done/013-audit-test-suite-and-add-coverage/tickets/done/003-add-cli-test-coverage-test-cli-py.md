---
id: '003'
title: Add CLI test coverage (test_cli.py)
status: done
use-cases:
- SUC-004
depends-on:
- '001'
---

# Add CLI test coverage (test_cli.py)

## Description

The CLI module (cli.py) has 0% test coverage. It exposes three commands
via Click: `init`, `mcp`, and `todo-split`. Create a new test file using
Click's CliRunner to exercise all three commands.

## Tasks

1. Create tests/unit/test_cli.py (or tests/system/ depending on I/O needs)
2. Import CliRunner and the Click app from cli.py
3. Test `clasi init`:
   - Happy path: invoke in tmp_path, verify files created
   - Verify exit code 0
   - Verify output mentions created files
4. Test `clasi mcp`:
   - Mock run_server to prevent actual stdio server start
   - Verify it calls run_server
5. Test `clasi todo-split`:
   - Create a multi-heading .md file in tmp_path todo directory
   - Invoke todo-split
   - Verify files are split
   - Verify exit code 0
6. Test error cases:
   - `clasi init` with --target pointing to nonexistent directory
   - `clasi todo-split` with --directory pointing to nonexistent path

## Acceptance Criteria

- [ ] tests/unit/test_cli.py exists with >= 8 tests
- [ ] All three CLI commands tested (init, mcp, todo-split)
- [ ] Exit codes validated (0 for success)
- [ ] Error cases tested with appropriate exit codes
- [ ] All tests pass

## Testing

- **Existing tests to run**: Full suite
- **New tests to write**: tests/unit/test_cli.py
- **Verification command**: `uv run pytest -v tests/unit/test_cli.py`
