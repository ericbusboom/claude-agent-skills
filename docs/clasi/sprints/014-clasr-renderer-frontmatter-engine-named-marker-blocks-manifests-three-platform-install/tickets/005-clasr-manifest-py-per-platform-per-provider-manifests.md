---
id: '005'
title: "clasr/manifest.py \u2014 per-platform per-provider manifests"
status: done
use-cases:
- SUC-003
- SUC-004
- SUC-005
- SUC-008
depends-on:
- '001'
github-issue: ''
todo: ''
completes_todo: false
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# clasr/manifest.py — per-platform per-provider manifests

## Description

Create `clasr/manifest.py` — the module that reads and writes per-platform per-provider
manifests. Manifests live inside the platform directory they describe:

- `.claude/.clasr-manifest/<provider>.json`
- `.codex/.clasr-manifest/<provider>.json`
- `.github/.clasr-manifest/<provider>.json`

Writes are atomic: serialize to `<file>.tmp`, then `os.replace` to the final path.
Partial writes are impossible even on crash or interrupt.

Manifest schema:
```json
{
  "version": 1,
  "provider": "myprovider",
  "platform": "claude",
  "source": "/abs/path/to/asr",
  "entries": [
    {"path": ".claude/skills/foo/SKILL.md", "kind": "symlink", "target": "..."},
    {"path": ".claude/agents/bar.md", "kind": "rendered", "from": "..."},
    {"path": ".claude/settings.json", "kind": "copy", "from": "..."},
    {"path": "AGENTS.md", "kind": "marker-block", "block": "clasr:myprovider"}
  ]
}
```

## Acceptance Criteria

- [x] `clasr/manifest.py` exports `manifest_path(platform_dir: Path, provider: str) -> Path`
      which returns `platform_dir / ".clasr-manifest" / f"{provider}.json"`
- [x] `clasr/manifest.py` exports `write_manifest(platform_dir: Path, provider: str, manifest: dict) -> None`
      which writes atomically: serialize to `<manifest>.tmp`, then `os.replace`
- [x] `write_manifest` creates the `.clasr-manifest/` directory if it does not exist
- [x] `clasr/manifest.py` exports `read_manifest(platform_dir: Path, provider: str) -> dict | None`
      which returns the parsed manifest dict, or `None` if the manifest file does not exist
- [x] `clasr/manifest.py` exports `delete_manifest(platform_dir: Path, provider: str) -> bool`
      which deletes the manifest file and returns `True` if deleted, `False` if not found
- [x] Module has NO imports from `clasi`
- [x] `tests/clasr/test_manifest.py` covers all the above

## Implementation Plan

### Approach

Simple JSON I/O with `os.replace` atomicity. The `.tmp` file is written in the same
directory as the final file so that `os.replace` is atomic (same filesystem). Create the
`.clasr-manifest/` parent directory before writing. For `read_manifest`, use
`json.loads(path.read_text())`; on `FileNotFoundError`, return `None`.

### Files to Create

- `clasr/manifest.py`
- `tests/clasr/test_manifest.py`

### Testing Plan

`tests/clasr/test_manifest.py` with at least:
- `test_write_and_read_manifest`: write a manifest, read it back; assert round-trip equality
- `test_write_manifest_atomic`: verify `.tmp` file is used — monkeypatch `os.replace` to
  capture the args; assert source arg ends with `.tmp`
- `test_write_manifest_creates_parent_dir`: `.clasr-manifest/` doesn't exist; assert
  created after write
- `test_read_manifest_not_found`: no manifest file; assert returns `None`
- `test_delete_manifest`: write then delete; assert returns `True`, file gone
- `test_delete_manifest_not_found`: no file; assert returns `False`
- `test_manifest_path`: assert correct path construction for given inputs
