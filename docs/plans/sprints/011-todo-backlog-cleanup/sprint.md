---
id: "011"
title: TODO Backlog Cleanup
status: planning
branch: sprint/011-todo-backlog-cleanup
use-cases: [SUC-001, SUC-002, SUC-003]
---

# Sprint 011: TODO Backlog Cleanup

## Goals

Clear the pending TODO backlog by implementing three improvements:
1. Make CLASI SE process rules explicit as the default for code changes
2. Ensure GitHub API skills use direct access with GITHUB_TOKEN
3. Add VS Code Copilot support to `clasi init`

## Problem

Three pending TODOs have accumulated that need to be addressed:
- The CLASI SE process rule is ambiguous about when it applies
- The `/report` and `/ghtodo` skills may not be using direct GitHub API auth
- `clasi init` only generates Claude Code configuration, not Copilot

## Solution

Address each TODO as an individual ticket within this sprint.

## Success Criteria

- `.claude/rules/clasi-se-process.md` explicitly states CLASI SE is the default process with opt-out phrases
- `/report` and `/ghtodo` skills verified to use `GITHUB_TOKEN` for direct API access
- `clasi init` generates Copilot-compatible configuration files alongside Claude Code files

## Scope

### In Scope

- Updating the CLASI SE process rule file
- Auditing and updating GitHub API auth in `/report` and `/ghtodo`
- Adding Copilot output to `clasi init`

### Out of Scope

- Other IDE integrations beyond Copilot
- Refactoring the entire init system

## Test Strategy

- Manual verification that the updated rule file reads correctly
- Test that `create_github_issue` MCP tool uses GITHUB_TOKEN
- Test that `clasi init` produces Copilot config files in a temp directory

## Architecture Notes

These are independent, small changes with no cross-dependencies.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, technical plan)
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
