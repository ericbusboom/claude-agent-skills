---
status: draft
sprint: "003"
---

# Sprint 003 Technical Plan

## Architecture Overview

This sprint is primarily about process and instruction changes, with two
areas of code change: the TODO cleanup CLI command and per-language MCP tools.
The existing package structure from sprint 001 is extended, not reorganized.

```
claude-agent-skills/
├── instructions/
│   ├── system-engineering.md      # Updated: TODO dir, overview doc
│   ├── coding-standards.md        # Unchanged
│   ├── testing.md                 # Updated: reference sprint test strategy
│   ├── git-workflow.md            # Unchanged
│   └── languages/                 # NEW: per-language instructions
│       └── python.md
├── claude_agent_skills/
│   ├── cli.py                     # Updated: add todo-split command
│   ├── todo_split.py              # NEW: TODO cleanup logic
│   ├── process_tools.py           # Updated: language instruction tools
│   └── templates.py               # Updated: merged sprint template, overview
├── skills/
│   ├── plan-sprint.md             # Updated: TODO mining step
│   ├── close-sprint.md            # Unchanged
│   ├── elicit-requirements.md     # Updated: overview doc workflow
│   └── create-technical-plan.md   # Updated: Mermaid guidance
├── agents/                        # Minimal changes (reference updates)
└── docs/plans/
    ├── overview.md                # NEW: replaces brief + usecases + tech-plan
    └── todo/
        └── done/                  # NEW: consumed TODOs go here
```

## Component Design

### Component: TODO Split Command (`claude_agent_skills/todo_split.py`)

**Use Cases**: SUC-002

A CLI command `clasi todo-split` that normalizes the TODO directory by
splitting files with multiple level-1 headings into individual files.

**Algorithm**:
1. Scan `docs/plans/todo/` for `.md` files (exclude `done/` subdir).
2. For each file, parse for level-1 headings (`# Heading`).
3. If 0 or 1 headings, skip.
4. If 2+ headings, extract each section (heading + content until next
   heading or EOF).
5. Create new file named from heading (slugified).
6. Delete original file.
7. Report actions.

**Edge cases**:
- Content before first heading: prepend to first section.
- Heading collisions: append number suffix.
- Empty sections: still create file (heading only).

**Integration**: Registered as `click` command in `cli.py`.

### Component: Per-Language Instructions (`instructions/languages/`)

**Use Cases**: SUC-007

Subdirectory with one markdown file per language. Same frontmatter format
as other instructions.

**Initial file**: `python.md` covering virtual environments, pyproject.toml,
type hints, pytest patterns, Python idioms.

### Component: Language Instruction MCP Tools (`process_tools.py`)

**Use Cases**: SUC-007

Two new tools following the `list_instructions`/`get_instruction` pattern:

| Tool | Description |
|------|-------------|
| `list_language_instructions` | List available language instructions |
| `get_language_instruction(language)` | Get full language instruction content |

### Component: Updated Sprint Template (`templates.py`)

**Use Cases**: SUC-004

The `SPRINT_TEMPLATE` merges in brief content (problem, solution, success
criteria) and adds a test strategy section. `SPRINT_BRIEF_TEMPLATE` is
removed from the `create_sprint` tool output.

### Component: Overview Document Template (`templates.py`)

**Use Cases**: SUC-005

New `OVERVIEW_TEMPLATE` for `docs/plans/overview.md`. Replaces
`BRIEF_TEMPLATE`, `USE_CASES_TEMPLATE`, `TECHNICAL_PLAN_TEMPLATE` for
top-level project planning.

A new MCP tool `create_overview` replaces `create_brief`,
`create_technical_plan`, and `create_use_cases`.

### Component: Updated Instructions

**Use Cases**: SUC-001, SUC-003, SUC-005, SUC-006

Changes to `instructions/system-engineering.md`:
- Add TODO directory section (format, lifecycle, layout)
- Replace Stage 1a/1b with single "Project Setup" using overview doc
- Update directory layout diagram
- Reference per-language instructions

Changes to `instructions/testing.md`:
- Reference sprint-level test strategy section

### Component: Updated Skills

**Use Cases**: SUC-003, SUC-005, SUC-006

Changes to `skills/plan-sprint.md`:
- Add step: scan TODO directory
- Add step: discuss TODOs with stakeholder
- Add step: move consumed TODOs to done

Changes to `skills/elicit-requirements.md`:
- Update to produce overview doc instead of separate brief + use cases

Changes to `skills/create-technical-plan.md`:
- Add Mermaid diagram guidance reference

## Dependencies

- Sprint 002 (Process Hardening) should ideally be done first so that this
  sprint benefits from the enforced review gates. However, this sprint has
  no hard code dependency on sprint 002's database.
- Per-language MCP tools depend on sprint 001's `process_tools.py`.
- TODO split depends on sprint 001's `click`-based CLI.
- Template changes depend on sprint 001's `templates.py`.

## Open Questions

None — all design decisions are resolved in this plan.
