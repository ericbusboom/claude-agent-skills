---
name: testing
description: Instructions for testing conventions and practices
---

# Testing Instructions

## General Principles

- Every ticket should include acceptance criteria that map to tests.
- Tests should be written before or alongside implementation, not after.
- Prefer unit tests for pure logic, integration tests for I/O boundaries.

## Test Organization

- Tests live in a `tests/` directory mirroring the source structure.
- Test file names follow the pattern `test_<module>.py`.
- Use pytest as the default test runner.

## Running Tests

```bash
# Full suite
pytest

# Specific file
pytest tests/test_<module>.py

# With coverage
pytest --cov=src

# Verbose output
pytest -v
```

## When to Run Tests

- Before committing: run the full test suite.
- After completing a ticket: verify all acceptance criteria pass.
- During code review: CI should run tests automatically.

## Relationship to Tickets

- Each ticket's acceptance criteria should have corresponding test cases.
- When marking a ticket as done, all its tests must pass.
- If a test cannot be written for a criterion, document why in the ticket.
