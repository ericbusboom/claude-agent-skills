---
id: '004'
title: "clasr/frontmatter.py \u2014 union frontmatter parser and projector"
status: done
use-cases:
- SUC-007
depends-on:
- '001'
github-issue: ''
todo: ''
completes_todo: false
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# clasr/frontmatter.py — union frontmatter parser and projector

## Description

Create `clasr/frontmatter.py` — the heart of the clasr renderer. This module parses the
union frontmatter format from `asr/agents/*.md` and `asr/rules/*.md` files and projects
it to a per-platform output frontmatter dict. The union format allows a single source file
to carry frontmatter for all platforms simultaneously; the projector extracts the
platform-specific view.

Union frontmatter format (from `SCHEMA.md`):
```yaml
name: code-review         # shared top-level field
description: Review a PR  # shared top-level field
claude:
  tools: [Read, Grep]     # claude-specific; merged on top of shared
copilot:
  applyTo: "**/*.ts"      # copilot-specific
codex: {}                 # absent or empty if no scoping
```

The projected output for `platform="claude"` would be:
```yaml
name: code-review
description: Review a PR
tools: [Read, Grep]
```

Note: `clasi` already has a `clasi/frontmatter.py` (`read_document`). The new
`clasr/frontmatter.py` is a different module with a different API focused on union
projection. It must NOT import from `clasi`.

## Acceptance Criteria

- [x] `clasr/frontmatter.py` exports `parse_union(source: Path) -> tuple[dict, dict, str]`
      where the return is `(shared_fm, full_fm, body)`
- [x] `clasr/frontmatter.py` exports `project(full_fm: dict, body: str, platform: str) -> tuple[dict, str]`
      where result is `(projected_fm_dict, body)` — the projected dict contains shared
      keys merged with platform-specific keys (platform-specific wins on conflict)
- [x] `project` drops all platform-namespace keys (`claude`, `codex`, `copilot`) from the output
- [x] `clasr/frontmatter.py` exports `render_file(source: Path, platform: str) -> str`
      which returns the complete rendered file (YAML frontmatter block + body)
- [x] `render_file` output has valid YAML frontmatter delimited by `---`
- [x] If the platform key is absent in the union frontmatter (e.g. no `copilot:` key),
      `project` returns only the shared fields (no error)
- [x] If the source file has no frontmatter at all, `parse_union` returns empty dicts and
      the full file content as body
- [x] Module has NO imports from `clasi`
- [x] `tests/clasr/test_frontmatter.py` covers all the above cases

## Implementation Plan

### Approach

Use `pyyaml` (already a project dependency). The parsing algorithm:
1. Check if file starts with `---`; if not, no frontmatter — return `({}, {}, full_content)`.
2. Find the closing `---`; extract YAML block; parse with `yaml.safe_load`.
3. The remainder after the second `---` is `body`.
4. For `project`: build output dict from shared keys (all top-level except `claude`,
   `codex`, `copilot`), then `update()` with the platform-specific nested dict.
5. For `render_file`: call `parse_union`, call `project`, serialize output dict with
   `yaml.dump`, reassemble into `---\n{yaml}\n---\n\n{body}`.

### Files to Create

- `clasr/frontmatter.py`
- `tests/clasr/test_frontmatter.py`

### Testing Plan

`tests/clasr/test_frontmatter.py` with at least:
- `test_project_claude`: source with `name`, `description`, `claude.tools`, `copilot.applyTo`;
  project to claude; assert output has `name`, `description`, `tools`; no `claude` key, no
  `copilot` key
- `test_project_copilot`: same source; project to copilot; assert `name`, `description`,
  `applyTo`; no `claude` key
- `test_project_absent_platform`: no `codex:` key; project to codex; assert only shared
  fields in output
- `test_project_override`: platform-specific key overrides shared key with same name
- `test_parse_no_frontmatter`: file with no `---` delimiters; assert empty dicts, full
  content as body
- `test_render_file_round_trip`: write union frontmatter file, call `render_file` for
  `"claude"`, parse the output; assert correct projected fields
- `test_body_verbatim`: body content (multi-paragraph markdown) is unchanged in output
