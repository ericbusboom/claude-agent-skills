---
id: '013'
title: Audit Test Suite and Add Coverage
status: done
branch: sprint/013-audit-test-suite-and-add-coverage
use-cases: []
---

# Sprint 013: Audit Test Suite and Add Coverage

## Goals

Audit the existing test suite for quality and gaps, add pytest-cov
infrastructure, fix shallow tests, fill critical coverage gaps, and enforce
a minimum coverage threshold going forward.

## Problem

The project has 168 tests across 12 files, but analysis reveals:

- **3 shallow test files** (test_mcp_server: 2 tests, test_frontmatter_tools:
  heavy mocking, test_github_issue: tests a stub)
- **0% CLI coverage** — no tests for `clasi init`, `clasi mcp`, or
  `clasi todo-split`
- **Critical untested paths** in artifact_tools.py: close_sprint() multi-step
  closure with versioning, insert_sprint() renumbering edge cases,
  move_ticket_to_done() with plan files
- **No coverage tooling** — no pytest-cov, no threshold, no CI enforcement
- **Weak assertions** in adequate tests — many use substring checks instead
  of structural validation

Estimated current coverage: ~70-75%. Well-tested modules (state_db,
frontmatter) sit at >90%, but CLI and MCP server core are ~20%.

## Solution

1. Add pytest-cov infrastructure and establish a coverage baseline
2. Replace shallow tests with real behavior tests
3. Add new test files for uncovered modules (CLI)
4. Strengthen tests for complex state-mutating operations
5. Set a minimum coverage threshold and add enforcement

## Success Criteria

- `uv run pytest --cov` passes with >=85% line coverage
- All 3 shallow test files rewritten with real behavior validation
- CLI commands have test coverage
- close_sprint(), insert_sprint(), and move_ticket_to_done() edge cases tested
- Coverage threshold enforced via pytest config (fail-under)

## Scope

### In Scope

- Add pytest-cov and configure coverage reporting
- Rewrite test_mcp_server.py, test_frontmatter_tools.py, test_github_issue.py
- Create test_cli.py for CLI command coverage
- Add tests for complex artifact operations (close_sprint, insert_sprint)
- Strengthen process_tools tests (use_case_coverage, activity guides)
- Set coverage threshold in pyproject.toml

### Out of Scope

- Performance/load testing
- Concurrency stress tests
- Integration tests against real GitHub API
- Windows/cross-platform path testing
- Refactoring source code (tests only)

## Test Strategy

This sprint IS the test strategy — every ticket directly adds or improves
tests. The meta-test-strategy: run the full suite after each ticket to
ensure no regressions, and verify the coverage number increases
monotonically.

## Architecture Notes

- All tests use pytest with tmp_path fixtures (no test pollution)
- System tests use real filesystem operations against temp directories
- Unit tests may mock external calls (subprocess, network) but should
  NOT mock internal module functions
- Coverage config lives in pyproject.toml under [tool.pytest.ini_options]

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, technical plan)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

| # | Title | Depends On |
|---|-------|------------|
| 001 | Add pytest-cov infrastructure and coverage configuration | — |
| 002 | Rewrite shallow test files (mcp_server, frontmatter_tools, github_issue) | 001 |
| 003 | Add CLI test coverage (test_cli.py) | 001 |
| 004 | Add tests for complex artifact operations (close_sprint, insert_sprint, move_ticket_to_done) | 001 |
| 005 | Strengthen process_tools tests and add use_case_coverage tests | 001 |
| 006 | Set coverage threshold and verify >=85% achieved | 001-005 |
