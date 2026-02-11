---
id: '001'
title: Add Testing section to ticket template
status: done
use-cases:
- SUC-001
depends-on: []
---

# Add Testing section to ticket template

## Description

Add a `## Testing` section to `TICKET_TEMPLATE` in
`claude_agent_skills/templates.py` so every new ticket created via
`create_ticket` includes placeholder guidance for testing. The section
should appear after `## Acceptance Criteria` and contain structured
placeholders for existing tests to run, new tests to write, and the
verification command.

## Acceptance Criteria

- [ ] `TICKET_TEMPLATE` in `templates.py` includes a `## Testing` section
- [ ] The section contains placeholders: "Existing tests to run", "New tests
      to write", "Verification command"
- [ ] Default verification command is `uv run pytest`
- [ ] A test in `tests/system/test_artifact_tools.py` verifies created
      tickets include the Testing section with expected placeholders
- [ ] All existing tests still pass

## Testing

- **Existing tests to run**: `tests/system/test_artifact_tools.py`,
  `tests/unit/test_init_command.py` (template-related)
- **New tests to write**: `test_ticket_template_includes_testing_section`
  in `tests/system/test_artifact_tools.py` — create a ticket, verify
  content includes `## Testing`, "Existing tests to run", "New tests to
  write", "Verification command"
- **Verification command**: `uv run pytest`
