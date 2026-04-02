---
id: "001"
title: "E2E Test Scripts for Project Creation"
status: planning
branch: sprint/001-e2e-test-scripts-for-project-creation
use-cases: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 001: E2E Test Scripts for Project Creation

## Goals

Create E2E test scripts that automate project creation and Claude Code invocation for the guessing-game test project.

## Problem

There are no automated scripts to kick off a full CLASI project lifecycle via Claude Code. The existing `setup_project.py` creates the project directory but doesn't invoke Claude Code to run the SE process.

## Solution

Add two new scripts to `tests/e2e/`:
1. `run_project_init.sh` — Invokes Claude Code with `--print` to run `/se init` on a freshly created project, feeding the guessing-game spec as the stakeholder specification.
2. `run_sprint.sh` — Invokes Claude Code with `--print` to plan and execute a sprint on the initialized project.

Both scripts use `claude -p` (non-interactive print mode) with `--dangerously-skip-permissions` for unattended execution.

## Success Criteria

- `run_project_init.sh` creates a project and produces CLASI overview/specification artifacts
- `run_sprint.sh` kicks off a sprint planning + execution cycle
- Scripts are executable and document their usage

## Scope

### In Scope

- Shell scripts for project init and sprint execution via Claude Code CLI
- Using existing `setup_project.py` for project bootstrapping
- Non-interactive `claude -p` invocation

### Out of Scope

- Automated assertion/validation of generated artifacts
- CI integration
- Claude Agent SDK programmatic invocation

## Test Strategy

These are test infrastructure scripts, not unit-testable code. Validation is manual: run the scripts and confirm Claude Code produces expected artifacts.

## Architecture Notes

- Scripts live in `tests/e2e/` alongside existing `setup_project.py`
- They use the `claude` CLI in print mode (`-p`) for non-interactive execution
- The project directory is `tests/e2e/project/` (same as existing)

## GitHub Issues

None.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
