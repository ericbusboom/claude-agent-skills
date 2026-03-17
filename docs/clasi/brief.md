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
3. Includes a system engineering process (instructions, agents, skills) that
   can be shared across projects to standardize planning workflows.
4. Provides a robust, agent-driven SE process where agents are grounded in
   the process, follow git conventions, perform code review, handle errors
   gracefully, and gate progress on stakeholder approval.
5. Supports sprint-based work organization: after initial project setup (brief,
   use cases, technical plan), all work is grouped into numbered sprints with
   their own lifecycle, branch, review gates, and ticket sets.

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
- Agents follow a defined git workflow (commit per ticket, meaningful messages).
- Code review is a required gate before any ticket is marked done.
- Dev agents (python-expert, documentation-expert) are grounded in the SE
  process — they know about tickets, ticket plans, testing instructions, and
  acceptance criteria.
- The process includes stakeholder review gates between stages.
- Error recovery patterns guide agents when tests fail, plans have gaps, or
  tickets need splitting.
- A coding standards instruction provides consistent conventions across agents.
- After initial project setup, all work is organized into numbered sprints.
- Each sprint has its own branch (`sprint/NNN-slug`), merged on completion.
- An architecture reviewer validates sprint plans against the existing codebase.
- A code reviewer validates implementations during ticket execution.
- Sprint lifecycle (plan → architecture review → stakeholder approval → tickets
  → execute → validate → close) is fully defined and skill-driven.

## Out of Scope

- Runtime agent orchestration or execution engine.
- Per-project customization of shared definitions (projects that need
  customization should create their own local definitions).
- CI/CD pipeline integration (instructions describe local workflow only).
- Language-specific agents beyond Python (future expansion).
