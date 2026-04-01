---
id: '002'
title: Add MCP permission allowlist to clasi init
status: done
use-cases:
- SUC-002
depends-on: []
---

# Add MCP permission allowlist to clasi init

## Description

Update `run_init()` to create/merge `.claude/settings.local.json` with
`{"permissions": {"allow": ["mcp__clasi__*"]}}`. Uses the same merge pattern
as `.mcp.json`.

## Acceptance Criteria

- [ ] `clasi init` creates `.claude/settings.local.json`
- [ ] File contains `{"permissions": {"allow": ["mcp__clasi__*"]}}`
- [ ] Merges with existing file if present (preserves other permissions)
- [ ] Idempotent (running twice produces same result)
- [ ] Test in `test_init_command.py` verifies creation and merge
