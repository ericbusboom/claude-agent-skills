---
id: "004"
title: Frontmatter MCP tools
status: todo
use-cases: [SUC-004]
depends-on: ["001"]
---

# Frontmatter MCP tools

## Description

Add MCP tools wrapping `frontmatter.py` functions so agents can read and
write YAML frontmatter through the MCP interface. Uses `resolve_artifact_path`
from ticket 001.

### Implementation

1. `read_artifact_frontmatter(path)` — Resolve path, read frontmatter, return JSON.
2. `write_artifact_frontmatter(path, updates)` — Resolve path, merge updates
   into existing frontmatter.

## Acceptance Criteria

- [ ] `read_artifact_frontmatter` returns JSON dict of frontmatter
- [ ] `write_artifact_frontmatter` merges updates into existing frontmatter
- [ ] `write_artifact_frontmatter` creates frontmatter on a plain file
- [ ] Both tools use `resolve_artifact_path`
- [ ] Error on nonexistent file
- [ ] Unit tests for both tools
