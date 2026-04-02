---
id: 008
title: Replace custom frontmatter parsing with python-frontmatter
status: done
use-cases: []
depends-on: []
github-issue: ''
todo: replace-custom-frontmatter-parsing-with-python-frontmatter.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Replace custom frontmatter parsing with python-frontmatter

## Description

Replace the hand-rolled YAML frontmatter parsing and writing code in
`clasi/frontmatter.py` with the `python-frontmatter` package, keeping the
same public API and on-disk format.

## Acceptance Criteria

- [x] `python-frontmatter` added to `pyproject.toml` dependencies and installed
- [x] `clasi/frontmatter.py` uses `python-frontmatter` for parsing (reading)
- [x] `clasi/artifact.py` `write()` method uses shared `_write_document` helper
- [x] On-disk frontmatter format unchanged (`---\nkey: value\n---\nbody`)
- [x] All 803 existing tests pass with `uv run pytest`

## Testing

- **Existing tests to run**: `tests/unit/test_frontmatter.py`, `tests/unit/test_artifact.py`, full suite
- **New tests to write**: No new tests required; existing suite validates round-trip correctness
- **Verification command**: `uv run pytest`
