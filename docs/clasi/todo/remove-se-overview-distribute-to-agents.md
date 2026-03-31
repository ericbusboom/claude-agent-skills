---
status: pending
---

# Remove get_se_overview and distribute process knowledge to individual agents

The `get_se_overview` MCP tool and the `se-overview-template.md` template should be
removed. Currently they provide a top-level view of the entire SE process, but this
is counterproductive — agents should only know about their own responsibilities, not
the full process.

## What needs to happen

1. **Remove `get_se_overview()`** — Delete the MCP tool and the
   `se-overview-template.md` template it renders.

2. **Distribute process knowledge into agent definitions** — Each agent file should
   contain the process steps and context relevant to that agent's role, and nothing
   else. An agent should understand what it is allowed to do and how, without seeing
   the full orchestration picture.

3. **Update CLAUDE.md** — Remove the mandatory "call `get_se_overview()`" instructions
   and the `UserPromptSubmit` hook that enforces it. Replace with guidance to call
   `get_agent_definition()` for the relevant role.

4. **Update any skills or instructions** that reference `get_se_overview()` to point
   to the appropriate agent definition instead.

## Why

Having a god's-eye view of the process encourages agents to act outside their lane.
Each agent should be scoped to its own responsibilities. This also reduces context
window waste — agents currently load a large overview they mostly don't need.
