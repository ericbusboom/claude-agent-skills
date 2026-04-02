---
id: '001'
title: Create E2E test scripts for project init and sprint execution
status: in-progress
use-cases: []
depends-on: []
github-issue: ''
todo: e2e-test-scripts-for-project-creation.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Create E2E test scripts for project init and sprint execution

## Description

Create shell scripts in `tests/e2e/` that invoke Claude Code CLI to:
1. Initialize a CLASI project from the guessing-game spec
2. Plan and execute a sprint on the initialized project

## Acceptance Criteria

- [ ] `run_project_init.sh` exists, is executable, and invokes `claude -p` to run project initiation
- [ ] `run_sprint.sh` exists, is executable, and invokes `claude -p` to plan/execute a sprint
- [ ] Both scripts have usage documentation in comments
- [ ] Existing tests still pass

## Testing

- **Existing tests to run**: `uv run pytest` (ensure no regressions)
- **New tests to write**: None — these are test infrastructure scripts, manually validated
- **Verification command**: `uv run pytest`
