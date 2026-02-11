---
id: '001'
title: Scold detection and self-reflection
status: done
use-cases:
- SUC-001
depends-on: []
---

# Scold detection and self-reflection

## Description

Create two artifacts:

1. **Always-on instruction** at `.claude/rules/scold-detection.md` — tells
   the agent to watch for stakeholder corrections and invoke the
   self-reflection skill when detected.
2. **Self-reflection skill** at `claude_agent_skills/skills/self-reflect.md`
   — produces a structured reflection document in `docs/plans/reflections/`.
3. Create the `docs/plans/reflections/` directory (with `.gitkeep`).

## Acceptance Criteria

- [ ] `.claude/rules/scold-detection.md` exists with detection signals
- [ ] `claude_agent_skills/skills/self-reflect.md` exists with structured process
- [ ] `docs/plans/reflections/` directory exists
- [ ] Reflection template includes: what happened, what should have happened, root cause, proposed fix
- [ ] Skill specifies YAML frontmatter format (date, sprint, category)

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: None (content-only markdown/instruction changes)
- **Verification command**: `uv run pytest`
