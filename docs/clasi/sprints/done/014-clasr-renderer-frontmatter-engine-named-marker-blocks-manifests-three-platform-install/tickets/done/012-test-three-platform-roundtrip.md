---
id: '012'
title: 'Test: three-platform roundtrip'
status: done
use-cases:
- SUC-003
- SUC-004
- SUC-005
depends-on:
- '011'
github-issue: ''
todo: ''
completes_todo: false
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Test: three-platform roundtrip

## Description

Write `tests/clasr/test_three_platform_roundtrip.py` — an integration test that installs
all three platforms from a single fixture `asr/` directory, verifies the outputs, then
uninstalls one platform and verifies the other two are intact.

This test validates the complete install/uninstall lifecycle across all three platforms
and confirms there is no cross-contamination between platform installs.

## Acceptance Criteria

- [x] `tests/clasr/test_three_platform_roundtrip.py` exists and passes
- [x] Fixture `asr/` contains: at least one skill, one agent (with union frontmatter),
      one rule, and `asr/AGENTS.md` with content
- [x] `install --claude --codex --copilot` against fixture populates all three platform dirs
- [x] All three `.clasr-manifest/<provider>.json` files exist after install
- [x] AGENTS.md contains the named marker block (written by both Claude and Codex)
- [x] CLAUDE.md contains the named marker block
- [x] `.github/copilot-instructions.md` contains the named marker block
- [x] Symlinks in `.claude/skills/` and `.agents/skills/` resolve to fixture `asr/` files
- [x] Uninstall Claude: `.claude/` entries removed, Claude manifest deleted
- [x] After Claude uninstall: Codex and Copilot manifests still exist; their files intact
- [x] AGENTS.md marker block is stripped after Claude uninstall (if Codex writes its own
      block, Codex's block must survive; if only Claude wrote to AGENTS.md, the block
      is stripped)
- [x] `asr/` source dir is byte-identical before and after the full install+uninstall cycle
- [x] All existing `clasi` tests still pass: `uv run pytest tests/unit/`

## Implementation Plan

### Approach

Create a shared `asr/` fixture (as a pytest fixture or tmp_path subtree). Call the
platform module `install()` functions directly (not via CLI). Run assertions. Then call
`claude.uninstall()`. Run post-uninstall assertions.

### Files to Create

- `tests/clasr/test_three_platform_roundtrip.py`
- A fixture helper in `tests/clasr/conftest.py` for creating a standard `asr/` directory
