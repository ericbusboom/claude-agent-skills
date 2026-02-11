---
id: '001'
title: Rename systems-engineer to technical-lead and Systems Engineering to Software
  Engineering
status: in-progress
use-cases:
- SUC-001
depends-on: []
---

# Rename systems-engineer to technical-lead and Systems Engineering to Software Engineering

## Description

Global rename across the codebase. "Systems Engineering" becomes "Software
Engineering" and the `systems-engineer` agent becomes `technical-lead`.
Leave done/ archives untouched (stakeholder decision).

### Files to change

- `agents/systems-engineer.md` → `agents/technical-lead.md`
- `instructions/system-engineering.md` → `instructions/software-engineering.md`
- `claude_agent_skills/process_tools.py` — 6 ACTIVITY_GUIDES entries reference
  `"system-engineering"`
- `tests/system/test_process_tools.py` — update assertions
- `skills/create-technical-plan.md` — references systems-engineer agent
- All 7 other agent files — update SE process references
- `claude_agent_skills/init_command.py` — update INSTRUCTION_CONTENT
- `docs/plans/brief.md`, `docs/plans/technical-plan.md` — top-level docs

### Approach

1. Rename agent file and instruction file
2. Grep for `systems.engineer`, `Systems Engineering`, `system-engineering`
3. Replace all matches in active files (skip `done/` archives)
4. Verify with final grep returning zero matches

## Acceptance Criteria

- [ ] `agents/technical-lead.md` exists with updated content
- [ ] `agents/systems-engineer.md` no longer exists
- [ ] `instructions/software-engineering.md` exists with updated content
- [ ] `instructions/system-engineering.md` no longer exists
- [ ] `process_tools.py` ACTIVITY_GUIDES references `"software-engineering"`
- [ ] Grep for `systems.engineer` in active files returns zero matches
- [ ] All tests pass
