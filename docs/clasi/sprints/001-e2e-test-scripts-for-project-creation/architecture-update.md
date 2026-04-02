---
sprint: "001"
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Architecture Update -- Sprint 001: E2E Test Scripts for Project Creation

## What Changed

Added two shell scripts to `tests/e2e/`:
- `run_project_init.sh` — Bootstraps a test project and runs Claude Code to initialize CLASI SE artifacts from the guessing-game spec.
- `run_sprint.sh` — Runs Claude Code to plan and execute a sprint on the test project.

## Why

The TODO `e2e-test-scripts-for-project-creation.md` calls for automated scripts to exercise the full CLASI project lifecycle via Claude Code. The existing `setup_project.py` handles directory setup but doesn't invoke Claude Code.

## Impact on Existing Components

No impact. These are new test scripts in `tests/e2e/`. They use the existing `setup_project.py` and the `claude` CLI. No source code or configuration changes.

## Migration Concerns

None.
