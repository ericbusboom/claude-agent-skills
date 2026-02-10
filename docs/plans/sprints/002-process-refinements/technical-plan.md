---
status: draft
---

# Sprint 002 Technical Plan

## Architecture Overview

This sprint is primarily about process and instruction changes, with two
areas of code change: the TODO cleanup CLI command and per-language MCP
tools. The existing package structure from sprint 001 is extended, not
reorganized.

```
claude-agent-skills/
├── instructions/
│   ├── system-engineering.md      # Updated: TODO dir, overview doc, scenarios
│   ├── coding-standards.md        # Unchanged
│   ├── testing.md                 # Updated: reference sprint test strategy
│   ├── git-workflow.md            # Unchanged
│   └── languages/                 # NEW: per-language instructions
│       └── python.md
├── claude_agent_skills/
│   ├── cli.py                     # Updated: add todo-split command
│   ├── todo_split.py              # NEW: TODO cleanup logic
│   ├── mcp_server.py              # Updated: register language tools
│   ├── process_tools.py           # Updated: language instruction tools
│   └── templates.py               # Updated: new sprint template, overview
├── skills/
│   ├── plan-sprint.md             # Updated: TODO mining step
│   ├── elicit-requirements.md     # Updated: overview doc workflow
│   └── create-technical-plan.md   # Updated: Mermaid guidance
├── agents/                        # Minimal changes (reference updates)
└── docs/plans/
    ├── overview.md                # NEW: replaces brief + usecases + tech-plan
    └── todo/
        └── done/                  # NEW: consumed TODOs go here
```

## Component Design

### Component: TODO Split Command (`todo_split.py`)

**Use Cases**: SUC-002

A CLI command `clasi todo-split` that normalizes the TODO directory by
splitting files with multiple level-1 headings into individual files.

**Algorithm**:
1. Scan `docs/plans/todo/` for `.md` files (excluding `done/` subdir).
2. For each file, parse for level-1 headings (`# Heading`).
3. If the file has 0 or 1 headings, skip it.
4. If the file has 2+ headings, extract each section (heading + content
   until the next heading or EOF).
5. For each section, create a new file named from the heading text
   (slugified: lowercase, spaces to hyphens, strip special chars).
6. Delete the original file.
7. Report actions taken.

**Edge cases**:
- Content before the first heading: prepend to the first section.
- Heading text collisions: append a number suffix.
- Empty sections: still create the file (heading only).

**Integration**: Registered as a `click` command in `cli.py`, alongside
`init` and `mcp`.

### Component: Per-Language Instructions (`instructions/languages/`)

**Use Cases**: SUC-008

A subdirectory of `instructions/` containing one markdown file per
language or environment. Each file provides language-specific coding
conventions that complement the general `coding-standards.md`.

**Initial file**: `python.md` covering:
- Python-specific style conventions (beyond PEP 8 basics already in
  coding-standards.md)
- Virtual environment and dependency management patterns
- Common Python project structures
- Python-specific testing patterns (pytest conventions, fixtures)

Files use the same frontmatter format as other instructions:
```yaml
---
name: Python
description: Python-specific coding conventions
---
```

### Component: Language Instruction MCP Tools (`process_tools.py`)

**Use Cases**: SUC-008

Two new tools added to the SE Process Access group:

| Tool | Description | Returns |
|------|-------------|---------|
| `list_language_instructions` | List available language instructions | [{name, description}] |
| `get_language_instruction(language)` | Get full language instruction | Markdown text |

These follow the same pattern as `list_instructions` / `get_instruction`
but scoped to the `instructions/languages/` subdirectory.

### Component: Updated Sprint Template (`templates.py`)

**Use Cases**: SUC-004

The `SPRINT_TEMPLATE` is updated to include:
- Problem and solution sections (from the removed brief.md)
- Test strategy section
- Source TODOs section (tracking which TODOs were consumed)

The `SPRINT_BRIEF_TEMPLATE` is removed (or deprecated).

### Component: Overview Document Template (`templates.py`)

**Use Cases**: SUC-005

A new `OVERVIEW_TEMPLATE` for `docs/plans/overview.md`:
- Project name and description
- High-level requirements
- Target users
- Technology stack and key constraints
- Key scenarios (high-level, not detailed)
- Sprint roadmap (rough sequence of planned sprints)
- Out of scope

This replaces `BRIEF_TEMPLATE`, `USE_CASES_TEMPLATE`, and
`TECHNICAL_PLAN_TEMPLATE` for top-level project planning.

### Component: Updated Instructions

**Use Cases**: SUC-001, SUC-003, SUC-005, SUC-006, SUC-007

Changes to `instructions/system-engineering.md`:
- Add TODO directory section (format, lifecycle, directory layout)
- Replace Stage 1a/1b with a single "Project Setup" stage using
  the overview document
- Rename "use cases" to "scenarios" throughout
- Update directory layout to show `todo/`, `todo/done/`, and
  `overview.md`
- Reference per-language instructions

Changes to `instructions/testing.md`:
- Reference the sprint-level test strategy section

### Component: Updated Skills

**Use Cases**: SUC-003, SUC-005, SUC-007

Changes to `skills/plan-sprint.md`:
- Add step: scan TODO directory for relevant ideas
- Add step: discuss relevant TODOs with stakeholder
- Add step: move consumed TODOs to done

Changes to `skills/elicit-requirements.md`:
- Update to produce an overview document instead of separate brief
  and use cases

Changes to `skills/create-technical-plan.md`:
- Add Mermaid diagram guidance
- Reference the sprint-level technical plan (not top-level)

## Dependencies on Sprint 001

Several tickets depend on sprint 001's MCP server and CLI being
functional:

- **Ticket 002** (TODO cleanup command): Needs the `click`-based CLI from
  sprint 001 ticket 003.
- **Ticket 010** (language MCP tools): Needs the MCP server and
  `process_tools.py` from sprint 001 tickets 005-006.
- **Tickets 004, 005, 007** (template changes): Need `templates.py` from
  sprint 001 ticket 002.

Tickets that are pure instruction/process changes (001, 003, 006, 008)
have no sprint 001 dependencies and can begin immediately.

## Resolved Decisions

- **Merge vs. remove brief.md**: Merge content into sprint.md. Do not
  create a brief.md at all in the new template.
- **Overview document name**: `overview.md` (not `brief.md` or
  `project.md`).
- **Scenario vs. use case**: Use "scenario" everywhere. Identifier prefix
  changes from `UC-` / `SUC-` to `SC-` / `SSC-` (Sprint Scenario).
- **Language instruction location**: `instructions/languages/` (not a
  separate top-level directory).
- **TODO done directory**: `docs/plans/todo/done/` (parallel to ticket
  and sprint done directories).

## Open Questions

- Should the overview document have a section for architectural decision
  records (ADRs), or should those remain ad-hoc in sprint technical plans?
- Should per-language instructions also include linting/formatting tool
  configuration (e.g., ruff, black, mypy settings)?
