---
status: draft
---

# Project Brief

## Project Name

claude-agent-skills

## Problem Statement

Developers using AI coding assistants (GitHub Copilot, Claude Code) need
shared, reusable agent definitions, skill definitions, and project instructions
across multiple repositories. Currently these must be manually copied into each
project, leading to drift, inconsistency, and maintenance burden.

## Proposed Solution

A pip-installable Python package that:

1. Stores canonical agent, skill, and instruction definitions in a single
   repository.
2. Provides a CLI command (`link-claude-agents`) that symlinks these
   definitions into any target repository, adapting the directory layout to
   each tool's conventions (GitHub Copilot and Claude Code).
3. Includes a system engineering process (instructions) that can be shared
   across projects to standardize planning workflows.

## Target Users

- Developers who use GitHub Copilot and/or Claude Code across multiple projects.
- Teams that want consistent AI assistant behavior and shared SE processes.

## Key Constraints

- Must work with editable pip installs (`pip install -e .`) so source changes
  propagate instantly.
- Must support both GitHub Copilot and Claude Code directory conventions.
- Symlinks must be idempotent (safe to re-run).

## Success Criteria

- Running `link-claude-agents` in a target repo creates working symlinks for
  agents, skills, and instructions for both Copilot and Claude Code.
- Changes to source definitions are immediately visible in all linked projects.
- The SE process instructions are discoverable by both AI tools.

## Out of Scope

- Runtime agent orchestration or execution.
- Per-project customization of shared definitions (projects that need
  customization should create their own local definitions).
