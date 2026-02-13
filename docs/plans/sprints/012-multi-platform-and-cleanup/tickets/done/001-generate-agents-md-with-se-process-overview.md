---
id: '001'
title: Generate AGENTS.md with SE process overview
status: done
use-cases:
- SUC-001
depends-on: []
---

# Generate AGENTS.md with SE process overview

## Description

Add an `AGENTS.md` template to `clasi init` that gives any AI agent a
high-level overview of the CLASI SE process. The file should cover:

- Starting a project: use `/project-initiation` or `get_skill_definition("project-initiation")`
- Opening a sprint: use `create_sprint` and the plan-sprint workflow
- Working on a ticket: use `get_skill_definition("execute-ticket")`
- Closing a sprint: use `get_skill_definition("close-sprint")`
- Reporting issues: use `/report` or `/ghtodo`

The content should be detailed enough that an agent understands it needs
the SE process, but refer to MCP tools for the actual instructions.

## Acceptance Criteria

- [ ] `AGENTS.md` is written to project root by `clasi init`
- [ ] Content covers starting projects, sprints, tickets, and closing
- [ ] References MCP tools for detailed instructions
- [ ] Idempotent (unchanged on re-run)

## Testing

- **Existing tests to run**: `uv run python -m pytest tests/unit/test_init_command.py`
- **New tests to write**: Test AGENTS.md creation, content assertions, idempotency
- **Verification command**: `uv run python -m pytest`
