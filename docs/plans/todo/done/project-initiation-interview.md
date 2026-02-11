# Project Initiation Interview

When starting a new project, the current process creates separate brief,
technical plan, and use cases documents. This should be streamlined into a
single **Project Overview** document and a guided interview workflow.

## Key Ideas

### Combined Project Overview

Replace the separate `brief.md`, `technical-plan.md`, and `usecases.md` with
a single `overview.md` that contains all three concerns. The `create_overview`
MCP tool already exists as a starting point.

### Initiation Interview Workflow

The project overview should be created through a guided interview:

1. The human provides a narration describing what they want to build
2. A "product manager" agent asks clarifying questions (architecture,
   constraints, priorities, scope)
3. The agent synthesizes answers into the Project Overview document

### Product Manager Agent

Create a new agent definition (`product-manager.md`) that specializes in:

- Eliciting requirements from stakeholder narration
- Asking targeted follow-up questions
- Structuring responses into the Project Overview format

### IDE Integration

After the Project Overview is created:

- Link it into `.claude/rules/` so Claude Code sees it
- Link it into `.github/copilot/instructions/` for GitHub Copilot
- Create/update `CLAUDE.md` at the project root referencing the SE process
  and the Project Overview

### Updates to `clasi init`

The init command should set up the scaffolding for this workflow,
potentially triggering the initiation interview on first run.
