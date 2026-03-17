---
status: draft
---

# Technical Plan

## Architecture Overview

A single Python package (`claude-agent-skills`) containing:

```
claude-agent-skills/
├── agents/              # Agent definitions (shared)
├── skills/              # Skill definitions (shared)
├── instructions/        # SE process & testing instructions (shared)
├── docs/plans/          # SE artifacts for THIS project (not shared)
├── claude_agent_skills/ # Python package with linking script
│   ├── __init__.py
│   └── link_agents.py
└── pyproject.toml       # Package metadata & entry point
```

The CLI command `link-claude-agents` is the sole entry point. It reads source
directories from the installed package location and creates symlinks in a
target repository.

## Technology Stack

- Python 3.7+
- setuptools (build system)
- No runtime dependencies beyond the standard library

## Component Design

### Component: Linking Script (`link_agents.py`)

**Purpose**: Create symlinks from a target repo to the shared definitions in
this repo.

**Use Cases Addressed**: UC-001, UC-002, UC-003, UC-004

**Key Functions**:
- `get_repo_root()` — Locates the source repo via `__file__`
- `link_directory()` — Creates a directory symlink, replacing stale links
- `link_file()` — Creates a file symlink, replacing stale links
- `link_claude_skills()` — Handles Claude's `<name>/SKILL.md` structure
- `link_agents_and_skills()` — Orchestrates all linking for both tools

**Target Layout per Tool**:

| Source | Copilot Target | Claude Code Target |
|--------|---------------|-------------------|
| `agents/` | `.github/copilot/agents/` (dir symlink) | `.claude/agents/` (dir symlink) |
| `skills/` | `.github/copilot/skills/` (dir symlink) | `.claude/skills/<name>/SKILL.md` (file symlinks) |
| `instructions/` | `.github/copilot/instructions/` (dir symlink) | `.claude/rules/` (dir symlink) |

### Component: Agent Definitions (`agents/`)

Markdown files with YAML frontmatter (`name`, `description`, `tools`).
Identical format works for both Copilot and Claude Code agents.

### Component: Skill Definitions (`skills/`)

Markdown files with YAML frontmatter (`name`, `description`). For Copilot,
linked as-is. For Claude Code, each file is symlinked as
`<skill-name>/SKILL.md` to match Claude's expected structure.

### Component: Instructions (`instructions/`)

Markdown files with YAML frontmatter (`name`, `description`). Linked as
`.claude/rules/` for Claude Code and `.github/copilot/instructions/` for
Copilot. Both tools auto-discover markdown files in these directories.

## Deployment Strategy

Installed via pip or pipx:

```bash
# Development (editable)
pip install -e .

# Or via pipx for isolated install
pipx install .
```

The `link-claude-agents` command is registered as a console script entry
point in `pyproject.toml`.

## Component: Git Workflow Instruction (`instructions/git-workflow.md`)

**Purpose**: Define when and how agents commit, branch, and write commit
messages during ticket execution.

**Use Cases Addressed**: UC-005

**Contents**:
- Commit timing (commit at ticket completion, optionally at milestones)
- Commit message format (conventional commits referencing ticket IDs)
- Branch strategy (feature branches per ticket, or work on main — project choice)
- Rules for agents: always commit before marking done, never force-push

## Component: Coding Standards Instruction (`instructions/coding-standards.md`)

**Purpose**: Shared coding conventions that all dev agents follow.

**Use Cases Addressed**: UC-006, UC-007

**Contents**:
- Project structure conventions
- Error handling patterns
- Logging approach
- Import ordering
- Configuration management

## Component: Updated Agent Definitions

**Purpose**: Ground dev agents in the SE process so they know about tickets,
plans, instructions, and acceptance criteria.

**Use Cases Addressed**: UC-007

**Changes**:
- `agents/python-expert.md` — Add SE process awareness: read ticket plan,
  follow testing and coding standards instructions, satisfy acceptance criteria.
- `agents/documentation-expert.md` — Add `Write` and `Edit` tools. Add SE
  process awareness.

## Component: Updated SE Instructions (`instructions/software-engineering.md`)

**Purpose**: Add review gates, error recovery, code review step, and
definition of done to the SE workflow.

**Use Cases Addressed**: UC-006, UC-008, UC-009

**Changes**:
- Add stakeholder review gates between phases (pause for approval)
- Add error recovery patterns (test failures, plan gaps, ticket splitting)
- Add code review step to ticket execution lifecycle
- Add definition of done (beyond acceptance criteria)
- Reference new instructions (git-workflow, coding-standards)

## Component: Updated Execute-Ticket Skill (`skills/execute-ticket.md`)

**Purpose**: Add code review step and git commit step to the ticket lifecycle.

**Use Cases Addressed**: UC-005, UC-006

**Changes**:
- Add review step between testing and documentation
- Add git commit step at ticket completion
- Reference error recovery patterns

## Component: Updated Project-Manager Agent (`agents/project-manager.md`)

**Purpose**: Add stakeholder review gates and decision heuristics.

**Use Cases Addressed**: UC-008, UC-009

**Changes**:
- Add review gates: pause for stakeholder approval after each phase
- Add decision heuristics for ticket prioritization, blockers, scope creep
- Add escalation rules

## Component: Sprint Documents (`docs/plans/sprints/`)

**Purpose**: Introduce a sprint layer above tickets. After initial project
setup, all work is organized into numbered sprints with their own lifecycle.

**Use Cases Addressed**: UC-010, UC-013

**Sprint Document Format** (`docs/plans/sprints/NNN-slug.md`):
```yaml
---
id: "NNN"
title: Sprint title
status: planning | active | done
branch: sprint/NNN-slug
use-cases: [UC-XXX, ...]
---
```
Followed by: goals, scope description, relevant architecture notes, and
a list of tickets created for this sprint.

**Directory Layout**:
```
docs/plans/sprints/
├── 001-initial-setup.md      # Active sprint
└── done/                     # Completed sprints
    └── ...
```

**Lifecycle**: conversation → plan document → architecture review →
stakeholder approval → create tickets → execute tickets → validate →
close sprint → merge branch → move to done/.

## Component: Architecture Reviewer Agent (`agents/architecture-reviewer.md`)

**Purpose**: Reviews sprint plans and architectural decisions against the
existing codebase and technical plan.

**Use Cases Addressed**: UC-011

**Tools**: Read, Grep, Glob, Bash

**Responsibilities**:
- Review sprint plans for architectural consistency
- Identify conflicts with existing components
- Flag risks, missing considerations, and scalability issues
- Validate that the sprint plan aligns with the technical plan
- Does NOT implement, does NOT create tickets

## Component: Code Reviewer Agent (`agents/code-reviewer.md`)

**Purpose**: Reviews code changes during ticket execution for quality,
standards compliance, and security.

**Use Cases Addressed**: UC-012

**Tools**: Read, Grep, Glob

**Responsibilities**:
- Review changed files against coding standards
- Check for security vulnerabilities
- Verify test coverage and acceptance criteria
- Produce pass/fail review with specific findings
- Replaces the self-review step currently in execute-ticket
- Does NOT implement, does NOT fix issues (reports them)

## Component: Plan Sprint Skill (`skills/plan-sprint.md`)

**Purpose**: Workflow skill for creating a sprint from a stakeholder
conversation.

**Use Cases Addressed**: UC-010, UC-011

**Workflow**:
1. Capture stakeholder goals and scope
2. Create sprint document with goals, scope, and use case references
3. Create sprint branch (`sprint/NNN-slug`)
4. Delegate architecture review to architecture-reviewer
5. Present sprint plan to stakeholder for approval
6. On approval, delegate ticket creation to technical-lead

## Component: Close Sprint Skill (`skills/close-sprint.md`)

**Purpose**: Workflow skill for closing a completed sprint.

**Use Cases Addressed**: UC-013

**Workflow**:
1. Verify all sprint tickets satisfy Definition of Done
2. Set sprint document status to `done`
3. Merge sprint branch to main
4. Move sprint document to `docs/plans/sprints/done/`
5. Report sprint completion

## Component: Updated Git Workflow (`instructions/git-workflow.md`)

**Purpose**: Add sprint branching to the git workflow instruction.

**Use Cases Addressed**: UC-014

**Changes**:
- Add sprint branch naming convention: `sprint/NNN-slug`
- Branch created at sprint start, merged at sprint close
- All ticket commits happen on the sprint branch
- Commit message format: `<type>: <summary> (#NNN, sprint NNN)`
- No feature branches within sprints (tickets commit directly to sprint branch)

## Component: Updated SE Instructions (`instructions/software-engineering.md`)

**Purpose**: Integrate sprints into the SE workflow. Rename "phases" to
"stages" to free the term. Add sprint as the default working mode after
initial setup.

**Use Cases Addressed**: UC-010, UC-011, UC-012, UC-013, UC-014

**Changes**:
- Rename "Phase" to "Stage" throughout (Stage 1a, 1b, 2, 3, 4)
- Add sprint concept: after Stage 1b, all work happens in sprints
- Add sprint lifecycle to workflow section
- Reference new agents (architecture-reviewer, code-reviewer)
- Reference new skills (plan-sprint, close-sprint)
- Update directory layout to include `docs/plans/sprints/`

## Component: Updated Project Manager (`agents/project-manager.md`)

**Purpose**: Add sprint coordination to the project-manager agent.

**Use Cases Addressed**: UC-010, UC-013

**Changes**:
- Add sprint state tracking (check for active sprints)
- Add sprint lifecycle coordination (plan → execute → close)
- Delegate architecture review to architecture-reviewer
- Delegate code review to code-reviewer (replacing self-review)
- Update delegation map with new agents

## Open Questions

- Should the script also update target `.gitignore` to exclude symlinked
  directories?
- Should there be an `unlink` command to remove symlinks?
