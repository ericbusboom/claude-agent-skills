---
id: '001'
title: Extract rule content into shared _rules.py module
status: done
use-cases:
  - SUC-004
depends-on: []
github-issue: ''
todo:
  - codex-install-rules-coverage-gap.md
  - plan-make-uninstall-delete-only-what-install-copied-no-whole-directory-deletes.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Extract rule content into shared _rules.py module

## Description

Currently, the five CLASI path-scoped rule bodies are hardcoded as strings inside
`clasi/platforms/claude.py`'s `RULES` dict. The Codex installer has its own partial
duplicate strings in `_DOCS_CLASI_RULES` and `_CLASI_SRC_RULES`. This ticket creates
a new `clasi/platforms/_rules.py` module that holds all five rule bodies as named
constants, then refactors `claude.py` to import from it.

This is a pure refactor on the Claude side — no behavioral change to the installed
`.claude/rules/*.md` files. The Codex installer is updated in tickets 006 and 007.

## Acceptance Criteria

- [x] `clasi/platforms/_rules.py` exists and exports constants for all five rule bodies:
      `MCP_REQUIRED_BODY`, `CLASI_ARTIFACTS_BODY`, `SOURCE_CODE_BODY`,
      `TODO_DIR_BODY`, `GIT_COMMITS_BODY` (names may vary; must be unambiguous).
- [x] `_rules.py` has no imports from other CLASI modules (data-only leaf module).
- [x] `claude.py`'s `RULES` dict is refactored to compose values using the constants
      from `_rules.py`. The YAML frontmatter (`paths:`) wrapper stays in `claude.py`.
- [x] The installed `.claude/rules/*.md` file content is byte-for-byte identical before
      and after this refactor. (Verify by reading the old strings and new rendered values
      in a test or by inspection.)
- [x] `_DOCS_CLASI_RULES` and `_CLASI_SRC_RULES` constants in `codex.py` are updated
      to import from `_rules.py`. (Partial alignment — full Codex content update is
      tickets 007.)
- [x] All existing tests pass.

## Implementation Plan

### Approach

1. Create `clasi/platforms/_rules.py` with five string constants, one per rule body.
   Copy the body text verbatim from the current `RULES` dict in `claude.py` (the portion
   after the `---\npaths: ...\n---\n` frontmatter header).
2. In `claude.py`, import the constants and replace the inline strings in `RULES`:
   ```python
   from clasi.platforms._rules import (
       MCP_REQUIRED_BODY, CLASI_ARTIFACTS_BODY, SOURCE_CODE_BODY,
       TODO_DIR_BODY, GIT_COMMITS_BODY,
   )
   RULES = {
       "mcp-required.md": f'---\npaths:\n  - "**"\n---\n\n{MCP_REQUIRED_BODY}',
       # ... etc.
   }
   ```
3. In `codex.py`, replace the `_DOCS_CLASI_RULES` and `_CLASI_SRC_RULES` inline strings
   with imports from `_rules.py`. (The content may change in ticket 007 but the import
   structure is set up here.)

### Files to create

- `clasi/platforms/_rules.py`

### Files to modify

- `clasi/platforms/claude.py` — `RULES` dict refactored to import from `_rules.py`
- `clasi/platforms/codex.py` — `_DOCS_CLASI_RULES`, `_CLASI_SRC_RULES` import from `_rules.py`

### Testing plan

- Run the full test suite: `uv run pytest`. Existing tests that assert installed rule
  file content will catch any inadvertent text changes.
- If no existing test asserts the full content of an installed `.claude/rules/` file,
  add a spot-check assertion in `tests/unit/test_init_command.py`:
  verify that the installed `mcp-required.md` contains the canonical body text
  (imported from `_rules.py`) after a `claude.install()` call.

### Documentation updates

None required — this is an internal refactor with no user-visible change.
