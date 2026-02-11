---
id: "002"
title: Remove deprecated create_brief, create_technical_plan, create_use_cases tools
status: todo
use-cases: [SUC-002]
depends-on: ["001"]
---

# Remove deprecated create_brief, create_technical_plan, create_use_cases tools

## Description

Delete the three legacy MCP tools (`create_brief`, `create_technical_plan`,
`create_use_cases`) from `artifact_tools.py`. Only `create_overview` remains
as the way to start a new project. Update the SE instruction and
`init_command.py` INSTRUCTION_CONTENT to remove references to these tools.

## Acceptance Criteria

- [ ] `create_brief` MCP tool removed from `artifact_tools.py`
- [ ] `create_technical_plan` MCP tool removed from `artifact_tools.py`
- [ ] `create_use_cases` MCP tool removed from `artifact_tools.py`
- [ ] Any associated templates removed if no longer needed
- [ ] SE instruction updated to remove references to deprecated tools
- [ ] `init_command.py` INSTRUCTION_CONTENT updated
- [ ] Tests updated (remove tests for deleted tools, verify they don't appear)
- [ ] All tests pass
