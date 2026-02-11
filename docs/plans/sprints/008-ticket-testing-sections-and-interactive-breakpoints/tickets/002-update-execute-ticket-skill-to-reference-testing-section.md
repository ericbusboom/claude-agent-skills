---
id: "002"
title: Update execute-ticket skill to reference Testing section
status: todo
use-cases: [SUC-002]
depends-on: ["001"]
---

# Update execute-ticket skill to reference Testing section

## Description

Update steps 5 and 6 of `claude_agent_skills/skills/execute-ticket.md` to
explicitly instruct the agent to read the ticket's `## Testing` section for
guidance on which tests to write and run. Currently these steps say "Create
tests as specified in the plan" and "Verify all tests pass" without
referencing the ticket's testing section.

## Acceptance Criteria

- [ ] Step 5 instructs the agent to read the ticket's `## Testing` section
      for guidance on new tests to write and placement
- [ ] Step 6 instructs the agent to run the verification command from the
      Testing section and any existing tests listed there
- [ ] The skill still references the testing instructions for directory
      placement (unit/, system/, dev/)

## Testing

- **Existing tests to run**: `uv run pytest` (full suite — skill content
  changes don't have dedicated tests but shouldn't break anything)
- **New tests to write**: None (content-only markdown change)
- **Verification command**: `uv run pytest`
