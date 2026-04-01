---
id: "023"
title: Integrate orphaned skills into workflow
status: done
use-cases: [UC-004, UC-006]
depends-on: []
---

# 023: Integrate Orphaned Skills into Workflow

## Description

`python-code-review` and `generate-documentation` skills exist but are not
referenced anywhere in the SE process. Wire them into the execute-ticket
workflow: the code review step should reference python-code-review, and the
documentation step should reference generate-documentation. Also list them
in the SE instructions skills section.

## Acceptance Criteria

- [x] `skills/execute-ticket.md` code review step references python-code-review skill
- [x] `skills/execute-ticket.md` documentation step references generate-documentation skill
- [x] `instructions/system-engineering.md` skills section lists all 7 skills
