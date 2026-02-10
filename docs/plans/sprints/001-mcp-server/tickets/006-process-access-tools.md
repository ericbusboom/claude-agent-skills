---
id: "006"
title: SE Process Access tools
status: todo
use-cases: [SUC-002]
depends-on: ["005"]
---

# SE Process Access Tools

Create `claude_agent_skills/process_tools.py` — MCP tools that serve SE
process content from the installed package.

## Description

Read-only tools that serve agents, skills, and instructions on demand.
These replace the old symlink approach — instead of files being present
in the repo, the LLM calls MCP tools to get the content.

## Acceptance Criteria

- [ ] `get_se_overview` tool returns a curated SE process overview including
      stages, agents, skills, and MCP tool reference
- [ ] `list_agents` tool returns JSON array of {name, description} for all
      agents
- [ ] `list_skills` tool returns JSON array of {name, description} for all
      skills
- [ ] `list_instructions` tool returns JSON array of {name, description}
      for all instructions
- [ ] `get_agent_definition(name)` returns the full markdown content of
      the named agent
- [ ] `get_skill_definition(name)` returns the full markdown content of
      the named skill
- [ ] `get_instruction(name)` returns the full markdown content of the
      named instruction
- [ ] Tools return clear error messages for non-existent names
- [ ] Names and descriptions are parsed from YAML frontmatter
