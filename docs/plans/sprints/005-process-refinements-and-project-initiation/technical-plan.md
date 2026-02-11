---
status: draft
---

# Sprint 005 Technical Plan

## Architecture Overview

This sprint has four independent workstreams that touch different parts of the
codebase. The rename (SUC-001) is a cross-cutting concern that should land
first since it changes file names and content that other workstreams reference.

## Component Design

### Component: Global Rename (SUC-001)

**Files to change:**

- `agents/systems-engineer.md` → `agents/technical-lead.md`
- `instructions/system-engineering.md` → `instructions/software-engineering.md`
  (file rename + content updates)
- `instructions/coding-standards.md` — check for agent references
- `skills/*.md` — update any agent references
- `claude_agent_skills/init_command.py` — update `INSTRUCTION_CONTENT`
- `claude_agent_skills/process_tools.py` — update all 6 ACTIVITY_GUIDES
  entries that reference `"system-engineering"` instruction name
- `agents/requirements-analyst.md`, `agents/project-manager.md`,
  `agents/python-expert.md`, `agents/code-reviewer.md`,
  `agents/documentation-expert.md`, `agents/architect.md`,
  `agents/architecture-reviewer.md` — update any SE process references
- `tests/` — update any test assertions that reference old names

**Approach:** Grep for `systems.engineer`, `Systems Engineering`, and
`system-engineering` across the repo, make all replacements, then verify
with a final grep that returns zero matches.

### Component: Project Initiation Workflow (SUC-002)

**New files:**

- `agents/product-manager.md` — agent definition for initiation interviews
- `skills/project-initiation.md` — skill definition for the interview workflow

**Modified files:**

- `claude_agent_skills/init_command.py` — update scaffolding to reference
  overview-based flow
- `claude_agent_skills/artifact_tools.py` — ensure `create_overview` tool
  is complete and produces the right template

**Design:** The product manager agent guides the stakeholder through a
structured interview using `AskUserQuestion`. The skill definition specifies
the question flow and how to synthesize answers into the overview format. The
overview template combines brief, use cases, and technical direction into
sections of a single document.

**Architecture review note:** The existing `requirements-analyst` agent
handles Stage 1a (elicit requirements). The new `product-manager` agent
focuses specifically on the initiation interview — a narrower, more
structured workflow. The `project-manager` agent delegates to
`product-manager` for initiation, just as it delegates to
`requirements-analyst` for detailed requirements elicitation.

### Component: TODO Frontmatter (SUC-003)

**Modified files:**

- `claude_agent_skills/artifact_tools.py` — update `move_todo_to_done` to
  accept `sprint_id` and `ticket_ids` parameters, write frontmatter
- `skills/todo.md` — update to add `status: pending` frontmatter on creation
- No changes needed in `mcp_server.py` — the `@server.tool()` decorator
  infers signatures from function parameters automatically

**Design:** Use the existing `write_artifact_frontmatter` helper to update
TODO files. The `move_todo_to_done` function gains optional `sprint_id` and
`ticket_ids` parameters. When provided, it writes them into the frontmatter
before moving the file.

### Component: Interactive Open Questions (SUC-004)

**Modified files:**

- `skills/plan-sprint.md` — add step to parse and present open questions
  before stakeholder approval

**Design:** The plan-sprint skill already has a stakeholder review step. We
add a sub-step that scans the technical plan for an `## Open Questions`
section, extracts each question (expected format: numbered list items), and
presents them via `AskUserQuestion`. Answers are written back into the
technical plan, replacing the open questions section with a "Decisions" section.

This is a skill-only change — no Python code needed, just updated instructions.

### Component: Harden Phase Gate Instructions (SUC-005)

**Modified files:**

- `skills/plan-sprint.md` — add explicit "DO NOT create tickets" warning
  during planning phases
- `instructions/system-engineering.md` (or renamed equivalent) — reinforce
  that ticket creation only happens after stakeholder approval advances
  the sprint to ticketing phase

**Also:**

- Add frontmatter to the 4 TODOs in `docs/plans/todo/done/` that were moved
  without it: `rename-process-and-agent.md`, `project-initiation-interview.md`,
  `todo-frontmatter-and-traceability.md`, `ask-open-questions-during-planning.md`

**Design:** The `create_ticket` MCP tool already enforces the phase gate at
the API level (it rejects ticket creation in planning-docs phase). But AI
agents attempt the call anyway because the skill instructions don't make the
prohibition clear enough. Add bold warnings in the plan-sprint skill at the
planning-docs and review phases saying tickets come later.

## Decisions (resolved at stakeholder review)

1. **Leave done/ archives as-is.** The rename only applies to active files.
   Done sprint archives are historical artifacts.
2. **Remove old tools.** Delete `create_brief`, `create_technical_plan`, and
   `create_use_cases` entirely. Only `create_overview` going forward.
3. **list_todos shows only pending.** Done TODOs are already in the `done/`
   directory; `list_todos` only scans the active directory.
