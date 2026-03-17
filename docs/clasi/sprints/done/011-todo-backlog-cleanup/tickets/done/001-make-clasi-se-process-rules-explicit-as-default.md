---
id: '001'
title: Make CLASI SE process rules explicit as default
status: done
use-cases:
- SUC-001
depends-on: []
---

# Make CLASI SE process rules explicit as default

## Description

Update `.claude/rules/clasi-se-process.md` to explicitly state that the CLASI SE
process is the **default process for all code change requests**. The agent must
follow this process unless the user explicitly opts out.

## Acceptance Criteria

- [ ] Rule file has a "Default Behavior" section stating CLASI SE is mandatory
- [ ] Opt-out phrases are listed: "out of process", "direct", "just do it" (skip process context)
- [ ] Language is direct and unambiguous

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: None (static content change)
- **Verification command**: `uv run pytest`
