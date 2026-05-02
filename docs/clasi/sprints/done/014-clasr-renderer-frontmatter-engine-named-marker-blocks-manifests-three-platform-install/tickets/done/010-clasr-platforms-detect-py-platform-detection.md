---
id: '010'
title: "clasr/platforms/detect.py \u2014 platform detection"
status: done
use-cases:
- SUC-004
depends-on:
- '007'
- 008
- 009
github-issue: ''
todo: ''
completes_todo: false
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# clasr/platforms/detect.py — platform detection

## Description

Create `clasr/platforms/detect.py` — read-only detection of which `clasr`-managed
platforms and providers are installed in a target directory. Used by `cli.py` for
informational output and potentially for smart defaults in future sprints.

## Acceptance Criteria

- [x] `clasr/platforms/detect.py` exports `detect(target: Path) -> dict[str, list[str]]`
- [x] Returns a dict like `{"claude": ["prov_a", "prov_b"], "codex": [], "copilot": ["prov_a"]}`
- [x] Detection is based on `.clasr-manifest/` directory presence and manifest file stems:
  - Claude: `.claude/.clasr-manifest/` exists → list JSON file stems (sans `.json`)
  - Codex: `.codex/.clasr-manifest/` exists → same
  - Copilot: `.github/.clasr-manifest/` exists → same
- [x] Missing platform directory → empty list for that platform (no error)
- [x] Module has NO imports from `clasi`
- [x] `tests/clasr/test_platform_detect.py` passes

## Implementation Plan

### Approach

Pure filesystem inspection. For each platform, check if the `.clasr-manifest/` directory
exists under the platform dir; if so, list all `*.json` files and return their stems as
provider names. No manifest file parsing needed — presence is sufficient for detection.

### Files to Create

- `clasr/platforms/detect.py`
- `tests/clasr/test_platform_detect.py`

### Testing Plan

`tests/clasr/test_platform_detect.py`:
- `test_detect_empty`: target has no platform dirs; assert all three lists are empty
- `test_detect_claude_one_provider`: `.claude/.clasr-manifest/myprov.json` exists;
  assert `detect()["claude"] == ["myprov"]`
- `test_detect_multiple_providers`: two manifest files under claude; assert both in list
- `test_detect_mixed`: claude has one provider, copilot has two; codex has none
