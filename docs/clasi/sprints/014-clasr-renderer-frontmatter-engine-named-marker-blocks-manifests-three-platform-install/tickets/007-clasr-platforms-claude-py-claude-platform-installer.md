---
id: '007'
title: "clasr/platforms/claude.py \u2014 Claude platform installer"
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

# clasr/platforms/claude.py — Claude platform installer

## Description

Create `clasr/platforms/claude.py` — the Claude platform installer. Given an `asr/`
source directory, installs CLASI-rendered content into `.claude/` in the target directory.
Uses `links`, `markers`, `frontmatter`, and `manifest` modules from the `clasr` package.

This module is ENTIRELY SEPARATE from `clasi/platforms/claude.py`. It must NOT import
from `clasi`.

## Acceptance Criteria

- [x] `clasr/platforms/claude.py` exports `install(source: Path, target: Path, provider: str, copy: bool = False) -> None`
- [x] `install` symlinks (or copies) each `source/skills/<n>/SKILL.md` to
      `.claude/skills/<n>/SKILL.md`; uses `clasr.links.link_or_copy`
- [x] `install` renders each `source/agents/<n>.md` with `platform="claude"` and writes
      to `.claude/agents/<n>.md`; uses `clasr.frontmatter.render_file`
- [x] `install` renders each `source/rules/<n>.md` with `platform="claude"` and writes
      to `.claude/rules/<n>.md`
- [x] `install` copies `source/claude/` contents to `.claude/` (preserving subdir structure)
- [x] For JSON passthrough files (`.json` extension): if the destination already exists,
      call `clasr.merge.merge_json_files`; write the merged result; record manifest entry
      `kind: "json-merged"` with `"keys"` list returned by `merge_json_files`
- [x] For non-JSON passthrough files: if the destination already exists and is NOT in the
      current provider's existing manifest, raise an error naming both providers
- [x] `install` writes `source/AGENTS.md` content as named marker block into both
      `AGENTS.md` AND `CLAUDE.md`; uses `clasr.markers.write_block`
- [x] `install` writes manifest to `.claude/.clasr-manifest/<provider>.json` with correct
      entries for each installed file
- [x] `clasr/platforms/claude.py` exports `uninstall(target: Path, provider: str) -> None`
- [x] `uninstall` reads manifest from `.claude/.clasr-manifest/<provider>.json`
- [x] `uninstall` removes each manifest entry: `unlink_alias` for symlink/copy,
      `unlink` for rendered files, `strip_block` for marker-block entries
- [x] `uninstall` for `json-merged` entries: removes only the provider's contributed keys
      from the shared JSON file; deletes the file if it becomes empty (`{}` or similar)
- [x] `uninstall` strips the named block from both `AGENTS.md` and `CLAUDE.md`
- [x] `uninstall` deletes the manifest file after successful cleanup
- [x] Module has NO imports from `clasi`
- [x] `tests/clasr/test_platform_claude.py` passes

## Implementation Plan

### Approach

Create `clasr/platforms/` as a package (`__init__.py`). Implement `claude.py` with two
public functions. Use the `asr/` source layout:
- `source/skills/*/SKILL.md` → `link_or_copy` to `.claude/skills/*/SKILL.md`
- `source/agents/*.md` → `frontmatter.render_file(path, "claude")` → `.claude/agents/*.md`
- `source/rules/*.md` → `frontmatter.render_file(path, "claude")` → `.claude/rules/*.md`
- `source/claude/<file>` → passthrough to `.claude/<file>`:
  - If `.json`: check if destination exists; if yes, call `merge.merge_json_files`
    and write the merged result; record `kind: "json-merged"` with `"keys"` list.
  - If not `.json`: if destination exists and NOT in current provider's existing manifest,
    raise `RuntimeError` naming both providers. Otherwise copy. Record `kind: "copy"`.
- `source/AGENTS.md` → `markers.write_block(target/"AGENTS.md", provider, content)`
  and same for `CLAUDE.md`
- At end: build the manifest dict and call `manifest.write_manifest`

For uninstall: read the manifest; iterate entries; dispatch by `kind`. For
`"json-merged"`: load the file, remove the provider's `"keys"`, write back;
delete the file if the result is empty (`{}` or `{"servers": {}}` etc.).

### Files to Create

- `clasr/platforms/__init__.py`
- `clasr/platforms/claude.py`
- `tests/clasr/test_platform_claude.py`

### Testing Plan

`tests/clasr/test_platform_claude.py` using a fixture `asr/` directory (created in tmpdir):
- `test_install_creates_skill_symlinks`: install; assert `.claude/skills/*/SKILL.md` is
  a symlink to `source/skills/*/SKILL.md`
- `test_install_renders_agents`: agent with union frontmatter; install; assert output has
  only `claude:` projected fields
- `test_install_writes_marker_blocks`: install; assert AGENTS.md and CLAUDE.md both
  contain `<!-- BEGIN clasr:<provider> -->` block
- `test_install_passthrough`: `source/claude/settings.json`; install; assert
  `.claude/settings.json` exists with same content
- `test_install_writes_manifest`: install; assert manifest JSON exists and is valid
- `test_uninstall_removes_all_entries`: install then uninstall; assert all installed
  files are removed; manifest file is deleted
- `test_source_dir_immutable`: verify `asr/` directory is byte-for-byte identical before
  and after install
