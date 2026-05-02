---
id: 008
title: "clasr/platforms/codex.py \u2014 Codex platform installer"
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

# clasr/platforms/codex.py — Codex platform installer

## Description

Create `clasr/platforms/codex.py` — the Codex platform installer. Given an `asr/`
source directory, installs rendered content into `.codex/` and `.agents/` in the target.
Codex has no path-scoped rule mechanism; rules are rendered as nested `AGENTS.md` files.

This module is ENTIRELY SEPARATE from `clasi/platforms/codex.py`. It must NOT import
from `clasi`.

## Acceptance Criteria

- [x] `clasr/platforms/codex.py` exports `install(source: Path, target: Path, provider: str, copy: bool = False) -> None`
- [x] `install` symlinks (or copies) each `source/skills/<n>/SKILL.md` to
      `.agents/skills/<n>/SKILL.md`
- [x] `install` renders each `source/agents/<n>.md` with `platform="codex"` and writes
      to `.codex/agents/<n>.md` (using filename `<n>.md`, not `.toml`)
- [x] `install` renders each `source/rules/<n>.md` with `platform="codex"`:
      - If the projected frontmatter has an `applyTo` or `paths` field, write the rendered
        body as a nested `AGENTS.md` at the corresponding subdirectory root
        (e.g. `applyTo: "docs/clasi/**"` → `target/docs/clasi/AGENTS.md`).
        Record `kind: "rendered"` in manifest.
      - If `applyTo`/`paths` is absent (unscoped rule), inject the rule body into the
        root `AGENTS.md` marker block content (included in the string passed to
        `markers.write_block`). Tracked via the existing `kind: "marker-block"` entry.
- [x] `install` copies `source/codex/` contents to `.codex/` preserving directory structure
- [x] For JSON passthrough files (`.json` extension): if destination exists, call
      `clasr.merge.merge_json_files`; record `kind: "json-merged"` with `"keys"` list
- [x] For non-JSON passthrough files: if destination exists and NOT in provider's existing
      manifest, raise an error naming both providers
- [x] `install` writes `source/AGENTS.md` content (plus unscoped rule bodies) as named
      marker block into root `AGENTS.md`; uses `clasr.markers.write_block`
- [x] `install` writes manifest to `.codex/.clasr-manifest/<provider>.json`
- [x] `clasr/platforms/codex.py` exports `uninstall(target: Path, provider: str) -> None`
- [x] `uninstall` reads manifest, removes each entry by kind, deletes manifest file
- [x] `uninstall` for `json-merged` entries: removes provider's contributed keys;
      deletes file if empty after removal
- [x] Module has NO imports from `clasi`
- [x] `tests/clasr/test_platform_codex.py` passes

## Implementation Plan

### Approach

Similar structure to `claude.py`. Key differences:
- Skills go to `.agents/skills/`; agents go to `.codex/agents/`.
- Rules: project frontmatter with `platform="codex"`. If `applyTo` present, write rendered
  body as nested `AGENTS.md` at the target subdirectory; record `kind: "rendered"`. If
  `applyTo` absent (confirmed by stakeholder: Q3), include the rule body in the content
  string passed to `markers.write_block` for root `AGENTS.md`; no additional manifest entry.
- Passthrough: use `merge.is_json_passthrough` to route `.json` files through
  `merge.merge_json_files`; non-JSON collisions are errors.

For uninstall: dispatch by `kind`. For `json-merged`: remove contributed keys, delete file
if empty.

### Files to Create

- `clasr/platforms/codex.py`
- `tests/clasr/test_platform_codex.py`

### Testing Plan

`tests/clasr/test_platform_codex.py`:
- `test_install_creates_agent_files`: renders agents to `.codex/agents/`
- `test_install_skills`: skills symlinked to `.agents/skills/`
- `test_install_writes_agents_md_block`: root `AGENTS.md` gets named marker block
- `test_install_writes_manifest`: manifest exists and is valid
- `test_uninstall_removes_all`: install then uninstall; all files removed; manifest deleted
- `test_source_dir_immutable`: asr/ unchanged before/after install
