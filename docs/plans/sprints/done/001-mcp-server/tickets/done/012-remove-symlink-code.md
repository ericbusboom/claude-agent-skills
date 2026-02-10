---
id: "012"
title: Remove symlink code
status: done
use-cases: []
depends-on: ["003"]
---

# Remove Symlink Code

Remove the old `link_agents.py` symlink functions and any references to
the symlink approach.

## Description

The MCP server replaces the symlink approach entirely. Remove the old code
and update any references.

## Acceptance Criteria

- [ ] `claude_agent_skills/link_agents.py` is deleted or gutted (the file
      may remain if `get_repo_root()` is reused by the MCP server — if so,
      extract that function to a shared utility and delete the rest)
- [ ] All symlink-related functions are removed (link_directory, link_file,
      link_claude_skills, link_agents_and_skills)
- [ ] No references to symlinks in the codebase
- [ ] `pip install -e .` still succeeds
