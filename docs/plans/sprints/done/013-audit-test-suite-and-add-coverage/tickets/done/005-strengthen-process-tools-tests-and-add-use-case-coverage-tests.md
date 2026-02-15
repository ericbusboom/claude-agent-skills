---
id: '005'
title: Strengthen process_tools tests and add use_case_coverage tests
status: done
use-cases:
- SUC-003
depends-on:
- '001'
---

# Strengthen process_tools tests and add use_case_coverage tests

## Description

test_process_tools.py has 20 tests rated "adequate" — assertions are
mostly substring checks ("X in result") that don't validate structure.
Additionally, get_use_case_coverage() has complex parent-chain parsing
logic that is completely untested.

## Tasks

### Strengthen existing tests
1. Replace `assert "string" in result` with structural assertions:
   - Parse JSON returns and validate keys/types
   - Validate markdown heading structure (starts with "# ")
   - Check that list functions return valid JSON arrays
2. Test get_activity_guide with invalid activity name (should raise/error)
3. Test _get_definition with nonexistent name (should list available names)

### Add use_case_coverage tests
1. Create a tmp_path project structure with:
   - docs/plans/usecases.md containing UC-001, UC-002, UC-003 headers
   - Sprint directories with usecases.md files containing Parent: UC-001 refs
   - A sprint in done/ with Parent: UC-002 refs
2. Monkeypatch _plans_dir to point to tmp_path
3. Call get_use_case_coverage and validate:
   - UC-001 reported as covered by active sprint
   - UC-002 reported as covered by done sprint
   - UC-003 reported as uncovered
4. Test with no usecases.md file (graceful empty response)
5. Test with malformed Parent: references

## Acceptance Criteria

- [ ] All JSON-returning functions validated with json.loads + key checks
- [ ] Error paths tested for invalid activity and missing definition names
- [ ] get_use_case_coverage tested with real directory structures
- [ ] >= 8 new or rewritten tests
- [ ] All tests pass

## Testing

- **Existing tests to run**: `uv run pytest tests/system/test_process_tools.py`
- **New tests to write**: Added/rewritten in test_process_tools.py
- **Verification command**: `uv run pytest -v tests/system/test_process_tools.py`
