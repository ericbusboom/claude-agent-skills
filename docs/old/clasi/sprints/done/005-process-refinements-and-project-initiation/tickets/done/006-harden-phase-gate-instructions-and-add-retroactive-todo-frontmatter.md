---
id: '006'
title: Harden phase gate instructions and add retroactive TODO frontmatter
status: done
use-cases:
- SUC-005
depends-on:
- '004'
---

# Harden phase gate instructions and add retroactive TODO frontmatter

## Description

Add explicit "DO NOT create tickets" warnings to `plan-sprint.md` during the
planning-docs, architecture-review, and stakeholder-review phases. Reinforce
in the SE instruction that ticket creation only happens after stakeholder
approval advances the sprint to ticketing phase.

Also add retroactive frontmatter to the 5 TODOs in `docs/plans/todo/done/`
that were moved without it during Sprint 005 planning.

## Acceptance Criteria

- [ ] `plan-sprint.md` has explicit warnings against premature ticket creation
- [ ] SE instruction (renamed) reinforces phase ordering for tickets
- [ ] `docs/plans/todo/done/rename-process-and-agent.md` has frontmatter with sprint: "005"
- [ ] `docs/plans/todo/done/project-initiation-interview.md` has frontmatter with sprint: "005"
- [ ] `docs/plans/todo/done/todo-frontmatter-and-traceability.md` has frontmatter with sprint: "005"
- [ ] `docs/plans/todo/done/ask-open-questions-during-planning.md` has frontmatter with sprint: "005"
- [ ] `docs/plans/todo/done/no_tickets_yet.md` has frontmatter with sprint: "005"
