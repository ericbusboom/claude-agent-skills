---
status: done
sprint: '011'
tickets:
- '003'
---

# Add VS Code Copilot support to `clasi init`

The `clasi init` command currently generates skills and rules for Claude Code
(e.g., `.claude/` directory structure), but does not generate equivalent
configuration for VS Code Copilot.

This should be extended so that `clasi init` also produces the appropriate
Copilot-compatible files (e.g., `.github/copilot-instructions.md` or similar)
to support teams using VS Code Copilot as their AI coding assistant.
