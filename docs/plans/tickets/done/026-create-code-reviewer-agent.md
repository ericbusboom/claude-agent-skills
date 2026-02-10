---
id: "026"
title: Create code-reviewer agent
status: done
use-cases: [UC-012]
depends-on: []
---

# Create Code Reviewer Agent

Create `agents/code-reviewer.md` — a dedicated agent for reviewing code
changes during ticket execution.

## Description

Currently code review is a self-review step in execute-ticket (the same
agent that wrote the code reviews it). This creates a dedicated reviewer
agent that can be delegated to, providing separation of concerns.

The code-reviewer reads changed files, the ticket plan, coding standards,
and testing instructions. It produces a pass/fail review with specific
findings. It does NOT fix issues — it reports them.

## Acceptance Criteria

- [ ] `agents/code-reviewer.md` exists with correct YAML frontmatter
- [ ] Agent has Read, Grep, Glob tools (read-only — does not edit)
- [ ] Agent knows to check: coding standards, security, test coverage,
      acceptance criteria
- [ ] Agent produces structured review output (pass/fail + findings)
- [ ] Agent includes SE Process Context section
- [ ] Agent has "What You Do Not Do" section (no implementing, no fixing)
