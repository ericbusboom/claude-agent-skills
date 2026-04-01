---
id: "001"
title: Frontmatter parser module
status: done
use-cases: [SUC-005, SUC-006]
depends-on: []
---

# Frontmatter Parser Module

Create `claude_agent_skills/frontmatter.py` — a utility for reading and
writing YAML frontmatter in markdown files.

## Description

Many MCP tools need to read and update YAML frontmatter in markdown files
(tickets, sprints, briefs). This module provides the shared functionality.

## Acceptance Criteria

- [ ] `read_frontmatter(path)` returns a dict of frontmatter fields
- [ ] `write_frontmatter(path, data)` updates frontmatter without changing
      the markdown body
- [ ] `read_document(path)` returns (frontmatter_dict, body_str)
- [ ] Handles files with no frontmatter gracefully (returns empty dict)
- [ ] Handles `---` delimiters correctly
- [ ] Uses `pyyaml` for YAML parsing
- [ ] Unit tests cover read, write, round-trip, and edge cases
