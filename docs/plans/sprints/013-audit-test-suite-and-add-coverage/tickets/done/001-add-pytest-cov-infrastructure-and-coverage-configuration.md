---
id: '001'
title: Add pytest-cov infrastructure and coverage configuration
status: done
use-cases:
- SUC-001
- SUC-002
depends-on: []
---

# Add pytest-cov infrastructure and coverage configuration

## Description

Add pytest-cov as a dev dependency, configure coverage reporting in
pyproject.toml, and add htmlcov/ to .gitignore. This is the foundation
ticket that all other tickets in this sprint build on.

Do NOT set fail_under yet — that's ticket #006 after all coverage gaps
are filled.

## Tasks

1. Add `pytest-cov` to `[project.optional-dependencies]` dev group
2. Run `uv lock` and `uv sync --dev` to install
3. Add coverage configuration to pyproject.toml:
   - `[tool.pytest.ini_options]` addopts: `--cov=claude_agent_skills --cov-report=term-missing`
   - `[tool.coverage.run]` branch: true
   - `[tool.coverage.report]` show_missing, exclude_lines
4. Add `htmlcov/` to .gitignore
5. Run `uv run pytest` and record the baseline coverage number in the
   commit message

## Acceptance Criteria

- [ ] `pytest-cov` in dev dependencies and lockfile
- [ ] `uv run pytest` shows line-by-line coverage with missing lines
- [ ] Branch coverage enabled
- [ ] htmlcov/ in .gitignore
- [ ] Baseline coverage number documented

## Testing

- **Existing tests to run**: `uv run pytest` (all 168 tests still pass)
- **New tests to write**: None — this is configuration only
- **Verification command**: `uv run pytest --cov=claude_agent_skills --cov-report=term-missing`
