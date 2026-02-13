# CLASI SE Process

This project uses the CLASI (Claude Agent Skills Instructions) software
engineering process, served via MCP tools.

## Default Behavior

**The CLASI SE process is the default process for ALL requests to implement
code changes.** When the stakeholder asks you to build a feature, fix a bug,
refactor code, or make any other code change, you MUST follow this process
(create or use a sprint, write tickets, execute through the lifecycle).

**The only exception** is when the stakeholder explicitly opts out using
phrases like:

- "out of process"
- "direct"
- "direct change"
- "skip the process"
- "just make the change"

If you are unsure whether a request is in-process or out-of-process, default
to following the process.

## Process Overview

The SE process has four stages:

1. **Stage 1a — Requirements**: Elicit requirements, produce brief and use cases
2. **Stage 1b — Architecture**: Produce technical plan from brief and use cases
3. **Stage 2 — Ticketing**: Break technical plan into actionable tickets
4. **Stage 3 — Implementation**: Execute tickets in sprints

Work is organized into **sprints** — each sprint is a directory containing
planning documents and tickets.

## MCP Tools Reference

Use these MCP tools (provided by the `clasi` server) to interact with the
SE process:

### SE Process Access

| Tool | Description |
|------|-------------|
| `get_se_overview` | High-level SE process description |
| `get_activity_guide(activity)` | Tailored guidance for an activity |
| `list_agents` | List available agent definitions |
| `list_skills` | List available skill definitions |
| `list_instructions` | List available instruction files |
| `get_agent_definition(name)` | Full agent definition |
| `get_skill_definition(name)` | Full skill definition |
| `get_instruction(name)` | Full instruction content |

### Artifact Management

| Tool | Description |
|------|-------------|
| `create_overview()` | Create project overview document |
| `create_sprint(title)` | Create a new sprint directory |
| `create_ticket(sprint_id, title)` | Create a ticket in a sprint |
| `list_sprints(status?)` | List sprints |
| `list_tickets(sprint_id?, status?)` | List tickets |
| `get_sprint_status(sprint_id)` | Sprint summary with ticket counts |
| `update_ticket_status(path, status)` | Update ticket status |
| `move_ticket_to_done(path)` | Move completed ticket to done/ |
| `close_sprint(sprint_id)` | Close and archive a sprint |

## Getting Started

1. Use `get_se_overview` to understand the full process
2. Use `get_activity_guide("requirements")` when starting a new project
3. Use `create_sprint(title)` to begin a new sprint
