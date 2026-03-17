---
status: done
sprint: '013'
---

# Audit Test Suite and Add Coverage Requirements

The project currently reports 208 tests passing in ~1 second. This speed
suggests many tests may be trivial or not exercising real application
behavior. Two actions are needed:

## 1. Audit Existing Tests

Review the full test suite to identify:

- **Redundant tests**: tests that overlap significantly with others
- **Trivial tests**: tests that only check boilerplate (e.g., template
  strings exist) without testing behavior
- **Missing coverage**: important code paths that have no test at all
- **Fast-but-shallow tests**: tests that mock too aggressively and
  don't validate real behavior

## 2. Add Coverage Enforcement

- Add `pytest-cov` to dev dependencies
- Configure a minimum coverage threshold (e.g., 80-90%)
- Require that new functionality is provably covered by a test:
  - PRs that add code without corresponding coverage should fail CI
  - The `execute-ticket` skill should include a coverage check step
- Add a coverage report to the test command (e.g., `uv run pytest --cov`)

## Goal

Every MCP tool, every state_db function, and every artifact operation
should have at least one test that exercises its real behavior end-to-end,
not just checks that a string exists in a template.
