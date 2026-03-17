---
id: "033"
title: Update execute-ticket to use code-reviewer agent
status: done
use-cases: [UC-012]
depends-on: ["026"]
---

# Update Execute-Ticket to Use Code-Reviewer Agent

Update `skills/execute-ticket.md` to delegate the code review step to the
code-reviewer agent instead of self-review.

## Description

Currently step 7 of execute-ticket says to use the python-code-review skill
(which is a self-review). With the new code-reviewer agent, this step should
delegate to code-reviewer for an independent review.

## Acceptance Criteria

- [ ] execute-ticket step 7 delegates to code-reviewer agent
- [ ] The old self-review reference (python-code-review skill) is replaced
- [ ] Review is pass/fail — implementation resumes only after pass
- [ ] Commit message format in the skill includes sprint reference
