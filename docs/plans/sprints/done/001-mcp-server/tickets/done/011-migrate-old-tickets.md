---
id: "011"
title: Migrate old tickets to sprint 000
status: done
use-cases: []
depends-on: []
---

# Migrate Old Tickets to Sprint 000

Move existing tickets (001-034) from `docs/plans/tickets/done/` into a
retroactive `docs/plans/sprints/done/000-initial-setup/`.

## Description

Unify all artifacts under the sprint-directory model. The old tickets were
created before the sprint concept existed. We create a retroactive sprint
000 and move them there.

## Acceptance Criteria

- [ ] `docs/plans/sprints/done/000-initial-setup/` directory exists
- [ ] `docs/plans/sprints/done/000-initial-setup/sprint.md` exists with
      appropriate retroactive frontmatter (id: "000", status: done)
- [ ] All ticket files from `docs/plans/tickets/done/` are moved to
      `docs/plans/sprints/done/000-initial-setup/tickets/done/`
- [ ] `docs/plans/tickets/` directory is removed (or left empty)
- [ ] No broken references in other files
