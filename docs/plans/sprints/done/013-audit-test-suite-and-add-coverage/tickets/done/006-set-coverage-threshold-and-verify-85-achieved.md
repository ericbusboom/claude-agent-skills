---
id: '006'
title: Set coverage threshold and verify >=85% achieved
status: done
use-cases:
- SUC-002
depends-on:
- '001'
- '002'
- '003'
- '004'
- '005'
---

# Set coverage threshold and verify >=85% achieved

## Description

This is the final ticket in the sprint. After all coverage gaps have been
filled by tickets 002-005, enable the fail_under threshold to enforce
coverage going forward.

If coverage is below 85% after all other tickets, identify remaining
gaps and add targeted tests to close them before setting the threshold.

## Tasks

1. Run `uv run pytest --cov=claude_agent_skills --cov-report=term-missing`
   and record the current coverage percentage
2. If coverage >= 85%:
   - Add `fail_under = 85` to `[tool.coverage.report]` in pyproject.toml
3. If coverage < 85%:
   - Review the term-missing output for the largest uncovered modules
   - Add targeted tests to close the gap
   - Repeat until >= 85%
4. Run full suite one final time to confirm it passes with threshold
5. Verify that removing a test file would cause coverage to drop below
   threshold (sanity check)

## Acceptance Criteria

- [ ] `[tool.coverage.report]` has `fail_under = 85` (or higher)
- [ ] `uv run pytest` passes (exit code 0) with threshold enforced
- [ ] Coverage report shows >= 85% line coverage
- [ ] Branch coverage reported (may be lower than line, that's OK)

## Testing

- **Existing tests to run**: Full suite
- **New tests to write**: Any gap-filling tests needed to reach 85%
- **Verification command**: `uv run pytest --cov=claude_agent_skills --cov-report=term-missing`
