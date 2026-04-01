---
id: '006'
title: Versioning system and tag_version MCP tool
status: done
use-cases:
- SUC-006
depends-on: []
---

# Versioning system and tag_version MCP tool

## Description

Implement `<major>.<isodate>.<build>` versioning. Create core module,
standalone MCP tool, and integrate into `close_sprint`.

### Implementation

1. Create `claude_agent_skills/versioning.py`:
   - `compute_next_version(major=0)` — Read git tags, compute next version.
   - `update_pyproject_version(version, pyproject_path)` — Update pyproject.toml.
   - `create_version_tag(version)` — Run `git tag v<version>`.
2. Add `tag_version` MCP tool to `artifact_tools.py`.
3. Integrate into `close_sprint` — auto-version after archiving.

## Acceptance Criteria

- [ ] Version format is `<major>.<YYYYMMDD>.<build>`
- [ ] Build increments within same date
- [ ] Build resets to 1 when date changes
- [ ] `update_pyproject_version` modifies pyproject.toml
- [ ] `tag_version` MCP tool works standalone
- [ ] `close_sprint` auto-versions
- [ ] Unit tests for versioning functions
