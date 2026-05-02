---
id: '014'
title: "clasr/merge.py \u2014 JSON deep-merge for multi-provider passthrough"
status: done
use-cases:
- SUC-006
- SUC-010
depends-on:
- '001'
github-issue: ''
todo: ''
completes_todo: false
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# clasr/merge.py — JSON deep-merge for multi-provider passthrough

## Description

Create `clasr/merge.py` — the JSON deep-merge helper used by all three platform
installers when multiple providers write passthrough files to the same destination.

When two providers both ship a JSON passthrough file to the same target path (e.g.
`asr/claude/settings.json` from provider A and provider B both targeting
`.claude/settings.json`), the second install must merge its keys into the existing file
rather than overwriting or erroring. This module owns that logic and is a prerequisite
for tickets 007, 008, and 009.

This module is a leaf node: no `clasr` or `clasi` imports.

## Acceptance Criteria

- [x] `clasr/merge.py` exports `is_json_passthrough(path: Path) -> bool`
      that returns `True` if `path` has a `.json` extension
- [x] `clasr/merge.py` exports `merge_json_files(existing: Path, incoming: dict, provider: str, other_provider: str) -> tuple[dict, list[str]]`
- [x] `merge_json_files` reads `existing` as JSON; deep-merges `incoming` dict into it;
      later provider's keys win on conflict
- [x] `merge_json_files` emits a WARNING to `stderr` for each top-level key present in
      both dicts, naming both `provider` and `other_provider` and the conflicting key
- [x] `merge_json_files` returns `(merged_dict, keys_contributed_by_incoming)` where
      `keys_contributed_by_incoming` is the list of top-level keys from `incoming`
- [x] `merge_json_files` raises `FileNotFoundError` if `existing` does not exist
      (callers must only call when destination already exists)
- [x] Module has NO imports from `clasi` or any other `clasr` module
- [x] `tests/clasr/test_merge.py` passes

## Implementation Plan

### Approach

`is_json_passthrough`: one-liner `path.suffix == ".json"`.

`merge_json_files`:
1. `base = json.loads(existing.read_text())`
2. Detect conflicts: `conflicts = [k for k in incoming if k in base]`
3. For each conflict, `print(f"WARNING: clasr: key '{k}' in {existing} is set by both '{other_provider}' and '{provider}'; '{provider}' wins", file=sys.stderr)`
4. Merge: `merged = {**base, **incoming}` handles shallow top-level; for deep-merge of
   nested dicts, recurse when both `base[k]` and `incoming[k]` are dicts.
5. Return `(merged, list(incoming.keys()))`

Deep-merge helper (private):
```python
def _deep_merge(base: dict, overlay: dict) -> dict:
    result = dict(base)
    for k, v in overlay.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result
```

### Files to Create

- `clasr/merge.py`
- `tests/clasr/test_merge.py`

### Testing Plan

`tests/clasr/test_merge.py`:
- `test_is_json_passthrough_true`: `.json` file returns `True`
- `test_is_json_passthrough_false`: `.md` file returns `False`
- `test_merge_json_files_basic`: no conflicts; result has all keys from both dicts;
  `keys_contributed` equals `list(incoming.keys())`
- `test_merge_json_files_conflict_warning`: both dicts have key `"foo"`; assert warning
  goes to stderr naming both providers; incoming value wins
- `test_merge_json_files_deep_merge`: `base = {"servers": {"a": 1}}`,
  `incoming = {"servers": {"b": 2}}`; assert result is `{"servers": {"a": 1, "b": 2}}`
- `test_merge_json_files_returns_contributed_keys`: incoming has keys `["mcpServers"]`;
  assert second return value is `["mcpServers"]`
- `test_merge_json_files_file_not_found`: nonexistent `existing` path raises
  `FileNotFoundError`

### Documentation Updates

None required beyond docstrings in `clasr/merge.py`.
