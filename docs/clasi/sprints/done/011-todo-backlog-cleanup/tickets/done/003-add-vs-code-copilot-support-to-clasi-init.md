---
id: '003'
title: Add VS Code Copilot support to clasi init
status: done
use-cases:
- SUC-003
depends-on: []
---

# Add VS Code Copilot support to clasi init

## Description

Extend `clasi init` to generate VS Code Copilot configuration files alongside
the existing Claude Code configuration. This means generating
`.github/copilot-instructions.md` (or equivalent) with project-relevant
instructions.

## Acceptance Criteria

- [ ] `clasi init` generates `.github/copilot-instructions.md`
- [ ] Copilot instructions include the CLASI SE process reference
- [ ] Existing Claude Code config generation is unchanged
- [ ] Init works correctly when `.github/` directory already exists

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: Test that init creates Copilot config files
- **Verification command**: `uv run pytest`
