---
id: '003'
title: "clasr/markers.py \u2014 named provider marker blocks"
status: done
use-cases:
- SUC-003
- SUC-005
- SUC-006
depends-on:
- '001'
github-issue: ''
todo: ''
completes_todo: false
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# clasr/markers.py — named provider marker blocks

## Description

Create `clasr/markers.py` — the module that writes and strips named provider-scoped marker
blocks in Markdown files. This is a NEW module, not a lift of `clasi/platforms/_markers.py`.
The marker format is `<!-- BEGIN clasr:<provider> -->` / `<!-- END clasr:<provider> -->`,
which is distinct from the `CLASI:{name}:START/END` format used by `_markers.py`.

Multiple providers can have independent blocks in the same file. Operations on one
provider's block do not affect other providers' blocks.

## Acceptance Criteria

- [x] `clasr/markers.py` exports `write_block(file_path: Path, provider: str, content: str) -> bool`
- [x] `write_block` creates the file if it does not exist, containing just the block
- [x] `write_block` replaces an existing block for `provider` in place (other providers'
      blocks are preserved)
- [x] `write_block` appends a new block if the file exists but has no block for `provider`
- [x] `write_block` returns `True` if the file was written/changed, `False` if unchanged
- [x] `clasr/markers.py` exports `strip_block(file_path: Path, provider: str) -> bool`
- [x] `strip_block` removes the named block for `provider`; preserves all other content
      including blocks from other providers
- [x] `strip_block` deletes the file if it becomes empty (only whitespace) after stripping
- [x] `strip_block` returns `True` if anything changed, `False` otherwise
- [x] Block format is exactly `<!-- BEGIN clasr:<provider> -->\n...\n<!-- END clasr:<provider> -->`
- [x] Module has NO imports from `clasi`
- [x] `tests/clasr/test_markers.py` covers all the above including multi-provider coexistence

## Implementation Plan

### Approach

Implement from scratch using the `BEGIN/END` marker format. The key requirement is that
multiple providers' blocks coexist; the parser must find only the block matching the given
provider name and leave all others untouched. Use string search (no regex needed) — locate
`<!-- BEGIN clasr:{provider} -->` and `<!-- END clasr:{provider} -->` as exact strings.

### Files to Create

- `clasr/markers.py`
- `tests/clasr/test_markers.py`

### Testing Plan

`tests/clasr/test_markers.py` with at least:
- `test_write_block_creates_file`: file doesn't exist; `write_block` creates it with block
- `test_write_block_replaces_existing`: block exists; call `write_block` with new content;
  assert block updated in place, file preserved around it
- `test_write_block_appends`: file exists without block; assert block appended
- `test_write_block_unchanged`: same content; assert returns False
- `test_strip_block_removes`: block present; call `strip_block`; assert block gone,
  surrounding content preserved
- `test_strip_block_not_found`: block not present; assert returns False, file unchanged
- `test_strip_block_deletes_empty_file`: block was entire file; assert file deleted
- `test_multi_provider_coexistence`: two providers' blocks in same file; strip one;
  assert other's block survives intact
- `test_write_block_two_providers`: write two different providers into same file; assert
  both blocks coexist; re-write one; assert other unchanged
