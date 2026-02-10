---
id: '005'
title: Create overview document and MCP tool
status: done
use-cases:
- SUC-005
depends-on: []
---

# Create overview document and MCP tool

## Description

Create an `OVERVIEW_TEMPLATE` in `templates.py` for `docs/plans/overview.md`
that replaces the three separate top-level documents (brief, use cases,
technical plan) with a single lightweight overview.

Add a `create_overview` MCP tool in `artifact_tools.py`. Keep the existing
`create_brief`, `create_technical_plan`, and `create_use_cases` tools but
mark them as deprecated in their docstrings.

Update `skills/elicit-requirements.md` to produce the overview doc instead of
separate brief + use cases.

Update `instructions/system-engineering.md` Stage 1a/1b to reference the
overview document workflow.

### Overview template sections

- Project Name
- Problem Statement
- Target Users
- Key Constraints
- High-Level Requirements / Key Scenarios
- Technology Stack
- Sprint Roadmap
- Out of Scope

## Acceptance Criteria

- [x] `OVERVIEW_TEMPLATE` exists in `templates.py`
- [x] `create_overview` MCP tool creates `docs/plans/overview.md`
- [x] Old tools (`create_brief`, `create_technical_plan`, `create_use_cases`)
      still work but docstrings note deprecation
- [x] `skills/elicit-requirements.md` updated for overview workflow
- [x] `instructions/system-engineering.md` updated for overview-based startup
- [x] Unit tests for `create_overview`
