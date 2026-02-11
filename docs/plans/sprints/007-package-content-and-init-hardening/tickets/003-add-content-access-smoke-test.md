---
id: "003"
title: Add content access smoke test
status: todo
use-cases: [SUC-003]
depends-on: ["001"]
---

# Add content access smoke test

## Description

Add a system test that calls actual MCP tool functions and verifies they
return real content. This would have caught the path resolution bug.

## Acceptance Criteria

- [ ] New test file `tests/system/test_content_smoke.py`
- [ ] Calls `list_agents()` and verifies non-empty JSON array
- [ ] Calls `get_instruction("coding-standards")` and verifies content returned
- [ ] Calls `list_skills()` and verifies non-empty JSON array
- [ ] Validates `content_path("agents")` directory exists with `.md` files
