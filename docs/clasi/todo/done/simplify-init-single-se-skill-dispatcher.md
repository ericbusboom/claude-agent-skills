---
status: done
sprint: '014'
---

# Simplify init: single /se skill dispatcher, minimal file writes

Major re-architecture of `clasi init` and how CLASI integrates with
target projects.

## Problem

The current `clasi init` overwrites files like AGENTS.md, appends to
.gitignore, and assumes it owns everything it touches. This is wrong
when initializing in a repo that already has these files with user
content. Init should be additive, not destructive.

## What changes

### 1. Replace all skill stubs with a single `/se` dispatcher

Instead of writing 6 separate skill stubs (todo, next, status,
project-initiation, report, ghtodo), write a single `/se` skill
that dispatches to the MCP server. This is the only skill file
init writes.

All of the skills that are currently written to the skills files will instead be
available through the MCP server. 

### 2. Stop taking over .claude/ and .codex/

Init no longer creates or manages .claude/ or .codex/ directories
wholesale. It only writes the `/se` skill into the appropriate
skills directory (e.g., `.claude/skills/se/SKILL.md`), leaving
everything else that's already there untouched.

### 3. Stop modifying .gitignore

Init no longer appends a CLASI block to .gitignore. The user
decides what to track.

### 4. AGENTS.md: append, don't replace

Instead of overwriting AGENTS.md, init appends a "CLASI SE Process"
section to whatever is already there. If the section already exists,
update it in place.

### 5. Consolidate rules into AGENTS.md

- Merge scold-detection.md into clasi-se-process.md
- Condense the SE process description
- The consolidated content goes into the AGENTS.md section
  (not separate rule files)
- No more writing to .claude/rules/

### 6. Move auto-approve into mcp_server.py

auto-approve.md becomes a skill served via the MCP server (like
the other non-slash-command skills), not a rule file written to
the target project.

## Summary of init behavior after this change

`clasi init` will:
1. Write `.claude/skills/se/SKILL.md` (the single dispatcher)
2. Append a CLASI section to AGENTS.md (or create it)
3. Write/merge `.mcp.json` with the clasi server config
4. Write `.claude/settings.local.json` with MCP permissions

That's it. No .gitignore modification, no rule files, no .codex
symlink, no wholesale directory creation.
