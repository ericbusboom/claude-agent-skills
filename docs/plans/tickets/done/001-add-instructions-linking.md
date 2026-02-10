---
id: "001"
title: Add instructions linking to link_agents.py
status: done
use-cases: [UC-004]
depends-on: []
---

# 001: Add Instructions Linking to link_agents.py

## Description

Update the linking script to also symlink the `instructions/` directory into
target repos for both GitHub Copilot and Claude Code.

## Acceptance Criteria

- [x] `link_agents.py` links `instructions/` as `.github/copilot/instructions/`
- [x] `link_agents.py` links `instructions/` as `.claude/rules/`
- [x] Module docstring updated to document the new content type
- [x] Dry run shows instructions linking
- [x] Missing `instructions/` directory does not cause an error

## Implementation Notes

- Use existing `link_directory()` function — no new linking logic needed.
- Guard with `source_instructions.exists()` check.
- Update argparse description and final "Done!" message.
