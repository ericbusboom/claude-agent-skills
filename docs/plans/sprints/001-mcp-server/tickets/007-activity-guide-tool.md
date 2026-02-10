---
id: "007"
title: Activity guide tool
status: todo
use-cases: [SUC-002]
depends-on: ["006"]
---

# Activity Guide Tool

Add `get_activity_guide(activity)` to `process_tools.py` — a tool that
returns tailored guidance for a specific SE activity.

## Description

Each activity (requirements, architecture, ticketing, implementation,
testing, code-review, sprint-planning, sprint-closing) has a relevant
combination of agent, skill, and instruction. This tool assembles them
into a single curated response so the LLM doesn't need multiple calls.

## Acceptance Criteria

- [ ] `get_activity_guide(activity)` tool is registered on the MCP server
- [ ] Supports activities: `requirements`, `architecture`, `ticketing`,
      `implementation`, `testing`, `code-review`, `sprint-planning`,
      `sprint-closing`
- [ ] Each activity response includes the relevant agent definition, skill
      workflow, and applicable instructions
- [ ] Response is formatted as coherent markdown (not just concatenated files)
- [ ] Returns a clear error for unknown activity names
- [ ] Activity list is discoverable (included in `get_se_overview` output)
