---
id: 009
title: "clasr/platforms/copilot.py \u2014 Copilot platform installer"
status: done
use-cases:
- SUC-003
- SUC-004
- SUC-005
- SUC-006
- SUC-007
- SUC-009
- SUC-010
depends-on:
- '002'
- '003'
- '004'
- '005'
- '006'
- '014'
github-issue: ''
todo: ''
completes_todo: false
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# clasr/platforms/copilot.py — Copilot platform installer

## Description

Create `clasr/platforms/copilot.py` — the GitHub Copilot platform installer. Given an
`asr/` source directory, installs rendered content into `.github/`. Skills are aliased as
a directory-level symlink `.github/skills/ -> .agents/skills/`.

**Marker block target (confirmed):** Write `source/AGENTS.md` as a named marker block into
`.github/copilot-instructions.md` ONLY. Do NOT write to root `AGENTS.md`. This matches
sprint 013's `copilot.py` behavior (Q1, resolved by stakeholder).

This module is ENTIRELY SEPARATE from `clasi/platforms/copilot.py`. It must NOT import
from `clasi`.

## Acceptance Criteria

- [x] `clasr/platforms/copilot.py` exports `install(source: Path, target: Path, provider: str, copy: bool = False) -> None`
- [x] `install` creates `.github/skills/` as a directory-level symlink to `.agents/skills/`
      (or copies the directory tree if `copy=True` or `OSError`)
- [x] `install` renders each `source/agents/<n>.md` with `platform="copilot"` and writes
      to `.github/agents/<n>.agent.md`
- [x] `install` renders each `source/rules/<n>.md` with `platform="copilot"` and writes
      to `.github/instructions/<n>.instructions.md` (preserving `applyTo:` from projected frontmatter)
- [x] `install` copies `source/copilot/` contents to `.github/` preserving directory structure
- [x] For JSON passthrough files (`.json` extension): if destination exists, call
      `clasr.merge.merge_json_files`; record `kind: "json-merged"` with `"keys"` list
- [x] For non-JSON passthrough files: if destination exists and NOT in provider's existing
      manifest, raise an error naming both providers
- [x] `install` writes `source/AGENTS.md` content as named marker block into
      `.github/copilot-instructions.md` ONLY (NOT root `AGENTS.md`);
      uses `clasr.markers.write_block`
- [x] `install` writes manifest to `.github/.clasr-manifest/<provider>.json`
- [x] `clasr/platforms/copilot.py` exports `uninstall(target: Path, provider: str) -> None`
- [x] `uninstall` reads manifest, removes each entry by kind, strips marker block from
      `.github/copilot-instructions.md`, deletes manifest file
- [x] `uninstall` for `json-merged` entries: removes provider's contributed keys;
      deletes file if empty after removal
- [x] Module has NO imports from `clasi`
- [x] `tests/clasr/test_platform_copilot.py` passes

## Implementation Plan

### Approach

Similar structure to `claude.py`. Key differences:
- Skills: directory-level symlink `.github/skills/ -> .agents/skills/` (not per-file).
  For `copy=True`: `shutil.copytree`. Record in manifest as single `kind: "symlink"` entry
  for the directory.
- Agents: rendered to `.github/agents/<n>.agent.md`.
- Rules: rendered to `.github/instructions/<n>.instructions.md`; preserve `applyTo:` from
  projected frontmatter as a frontmatter field in the output file.
- Passthrough: use `merge.is_json_passthrough` to route `.json` files through
  `merge.merge_json_files`; non-JSON collisions are errors.
- Marker block: `.github/copilot-instructions.md` ONLY. No write to root `AGENTS.md`.
  This matches sprint 013 `copilot.py` behavior (Q1 confirmed).

### Files to Create

- `clasr/platforms/copilot.py`
- `tests/clasr/test_platform_copilot.py`

### Testing Plan

`tests/clasr/test_platform_copilot.py`:
- `test_install_creates_skills_symlink`: assert `.github/skills` is a symlink to `.agents/skills`
- `test_install_renders_agents`: renders to `.github/agents/<n>.agent.md`
- `test_install_renders_rules`: renders to `.github/instructions/<n>.instructions.md` with
  `applyTo:` frontmatter field
- `test_install_writes_copilot_instructions_block`: `copilot-instructions.md` contains
  `<!-- BEGIN clasr:<provider> -->` block
- `test_install_writes_manifest`: manifest exists and is valid
- `test_uninstall_removes_all`: install then uninstall; all files removed; manifest deleted
- `test_copy_mode`: `copy=True`; assert `.github/skills` is a directory (not symlink)
