---
status: done
sprint: 008
---

# Ticket Testing Section

Tickets should include a **Testing** section that describes what tests should
be run after the ticket work is complete. This ensures that:

1. The implementer knows which tests to run before marking a ticket done
2. Test expectations are documented alongside the work description
3. Both existing tests (regression) and new tests (for the change) are covered

## Proposed changes

- Update the ticket template (in `create_ticket`) to include a `## Testing`
  section placeholder
- Update the `execute-ticket` skill to reference the ticket's testing section
  when running verification
- Consider whether the testing section should list:
  - Specific test files/classes to run
  - New tests that need to be written
  - Manual verification steps (if any)
  - The full test suite command (`uv run pytest`)
