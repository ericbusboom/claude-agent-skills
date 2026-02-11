---
id: "003"
title: Multi-ecosystem version detection
status: todo
use-cases: [SUC-003]
depends-on: []
---

# Multi-ecosystem version detection

## Description

Refactor `versioning.py` to detect version files by ecosystem. Add
`detect_version_file` and `update_version_file` functions. Update both
`tag_version` MCP tool and `close_sprint` auto-versioning block in
`artifact_tools.py` to use the new abstraction. Update `close-sprint.md`
step 8 to reference the version file generically.

## Acceptance Criteria

- [ ] `detect_version_file(project_root)` returns `(path, type)` or `None`
- [ ] `update_version_file(path, file_type, version)` dispatches correctly
- [ ] `tag_version` MCP tool uses `detect_version_file`
- [ ] `close_sprint` auto-versioning uses `detect_version_file`
- [ ] `package.json` version field updated correctly when detected
- [ ] Falls back to git-tag-only when no version file found
- [ ] `close-sprint.md` step 8 references version file generically
- [ ] Existing `pyproject.toml` behavior unchanged

## Testing

- **Existing tests to run**: `tests/unit/test_versioning.py`
- **New tests to write**:
  - `test_detect_version_file_pyproject`
  - `test_detect_version_file_package_json`
  - `test_detect_version_file_priority`
  - `test_detect_version_file_none`
  - `test_update_package_json_version`
  - `test_update_package_json_no_version_field`
  - `test_tag_version_tag_only`
- **Verification command**: `uv run pytest`
