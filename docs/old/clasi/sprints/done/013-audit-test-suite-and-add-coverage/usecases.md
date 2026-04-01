---
status: draft
---

# Sprint 013 Use Cases

## SUC-001: Developer runs coverage report
Parent: None

- **Actor**: Developer
- **Preconditions**: pytest-cov is installed and configured
- **Main Flow**:
  1. Developer runs `uv run pytest --cov`
  2. Terminal displays line-by-line coverage with missing lines highlighted
  3. HTML report is generated in htmlcov/
- **Postconditions**: Coverage percentage is visible; uncovered lines identified
- **Acceptance Criteria**:
  - [ ] `pytest-cov` in dev dependencies
  - [ ] `--cov` flags configured in pyproject.toml addopts
  - [ ] HTML and term-missing reports generated
  - [ ] htmlcov/ added to .gitignore

## SUC-002: CI blocks PR with insufficient coverage
Parent: None

- **Actor**: CI pipeline / developer submitting PR
- **Preconditions**: Coverage threshold configured in pyproject.toml
- **Main Flow**:
  1. Developer pushes code with insufficient test coverage
  2. pytest runs with --cov-fail-under threshold
  3. Test run fails with coverage below threshold
- **Postconditions**: PR cannot merge until coverage meets threshold
- **Acceptance Criteria**:
  - [ ] fail_under configured in pyproject.toml (>=85%)
  - [ ] Failing coverage causes non-zero exit code

## SUC-003: Developer validates MCP tool registration
Parent: None

- **Actor**: Developer
- **Preconditions**: Tests exist for MCP server tool registration
- **Main Flow**:
  1. Developer runs test suite
  2. Tests verify all expected MCP tools are registered
  3. Tests verify tool invocation returns expected types
- **Postconditions**: Confidence that MCP server exposes correct tool set
- **Acceptance Criteria**:
  - [ ] test_mcp_server.py has 10+ tests
  - [ ] All 33 MCP tools verified as registered
  - [ ] At least one invocation test per tool category

## SUC-004: Developer validates CLI commands
Parent: None

- **Actor**: Developer
- **Preconditions**: CLI test file exists
- **Main Flow**:
  1. Developer runs test suite
  2. CLI tests exercise init, mcp, and todo-split commands
  3. Exit codes and output validated
- **Postconditions**: CLI entry points have test coverage
- **Acceptance Criteria**:
  - [ ] test_cli.py created with tests for each CLI command
  - [ ] Exit codes tested (success and error cases)
  - [ ] Output content validated

## SUC-005: Developer validates complex artifact operations
Parent: None

- **Actor**: Developer
- **Preconditions**: Tests exist for close_sprint, insert_sprint, move_ticket_to_done
- **Main Flow**:
  1. Developer runs test suite
  2. Tests exercise multi-step operations with edge cases
  3. State consistency validated after each operation
- **Postconditions**: Complex state-mutating operations proven correct
- **Acceptance Criteria**:
  - [ ] close_sprint tested with versioning integration
  - [ ] insert_sprint tested with 3+ sprint renumbering
  - [ ] move_ticket_to_done tested with associated plan files
  - [ ] Error/recovery paths tested
