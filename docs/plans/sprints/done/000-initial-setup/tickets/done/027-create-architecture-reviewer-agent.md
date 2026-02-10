---
id: "027"
title: Create architecture-reviewer agent
status: done
use-cases: [UC-011]
depends-on: []
---

# Create Architecture Reviewer Agent

Create `agents/architecture-reviewer.md` — an agent that reviews sprint
plans and architectural decisions against the existing codebase and
technical plan.

## Description

The architecture-reviewer validates sprint plans before work begins. It
reads the sprint plan, technical plan, and relevant existing code to check
for consistency, conflicts, risks, and missing considerations. It produces
a review report but does not implement or create tickets.

## Acceptance Criteria

- [ ] `agents/architecture-reviewer.md` exists with correct YAML frontmatter
- [ ] Agent has Read, Grep, Glob, Bash tools
- [ ] Agent knows to check: architectural consistency, conflicts with
      existing components, risks, scalability
- [ ] Agent produces structured review output (findings + recommendations)
- [ ] Agent includes SE Process Context section
- [ ] Agent has "What You Do Not Do" section (no implementing, no ticketing)
