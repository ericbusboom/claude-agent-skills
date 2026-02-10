---
id: "005"
title: Add test strategy section to sprint template
status: todo
use-cases: [SUC-004]
depends-on: ["004"]
---

# Add Test Strategy Section to Sprint Template

## Description

Each sprint should include a test strategy that describes the overall
testing approach for that sprint's work. This goes beyond individual
ticket-level test plans — it covers the sprint-wide testing philosophy,
what types of tests are needed, and any cross-cutting test concerns.

## Changes Required

1. Update `claude_agent_skills/templates.py`:
   - Add a "Test Strategy" section to the sprint template (after
     Architecture Notes, before Tickets).

2. Update `instructions/system-engineering.md`:
   - In the Sprint section, note that each sprint includes a test
     strategy.

3. Update `instructions/testing.md`:
   - Add a reference to the sprint-level test strategy and how it
     relates to ticket-level test plans.

## Test Strategy Section Template

```markdown
## Test Strategy

Describe the overall testing approach for this sprint:

- **Test types needed**: Which of unit, system, dev tests apply?
- **Key test scenarios**: What are the most important things to verify?
- **Cross-cutting concerns**: Shared fixtures, test data, or setup
  needed across multiple tickets.
- **Verification approach**: Simple assertions, golden file comparison,
  or visual comparison? (See testing instructions.)
```

## Acceptance Criteria

- [ ] Sprint template includes a "Test Strategy" section
- [ ] Section provides prompts for test types, scenarios, and approach
- [ ] SE instructions reference the test strategy section
- [ ] Testing instructions reference the sprint-level strategy
