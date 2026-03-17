---
id: '002'
title: Rewrite shallow test files (mcp_server, frontmatter_tools, github_issue)
status: done
use-cases:
- SUC-003
depends-on:
- '001'
---

# Rewrite shallow test files (mcp_server, frontmatter_tools, github_issue)

## Description

Three test files were identified as shallow during the audit. Each needs
a different fix:

- **test_mcp_server.py** (2 tests): Expand to verify tool registration,
  tool count, tool names, and content_path resolution for all content
  directories.
- **test_frontmatter_tools.py** (11 tests): Remove mocking of
  resolve_artifact_path. Use real file structures in tmp_path and test
  end-to-end read/write/merge of frontmatter through the tool functions.
- **test_github_issue.py** (8 tests): Keep metadata fallback tests but
  add tests for _get_github_token, _get_github_repo, and mock-urllib
  tests for _create_github_issue_api success/error paths.

## Tasks

### test_mcp_server.py
1. Import server and inspect registered tools
2. Assert all expected MCP tool names are present
3. Assert tool count matches expected number
4. Test content_path() for agents/, skills/, instructions/, languages/
5. Verify server.name == "clasi"

### test_frontmatter_tools.py
1. Remove all `@patch("...resolve_artifact_path")` decorators
2. Create real directory structures with done/ subdirectories in tmp_path
3. Test read_artifact_frontmatter with file at original path
4. Test read_artifact_frontmatter with file in done/ subdirectory
5. Test write_artifact_frontmatter creates/merges frontmatter
6. Test error on missing file
7. Test file without existing frontmatter

### test_github_issue.py
1. Keep existing metadata fallback tests (they're valid for the no-token path)
2. Add tests for _get_github_token: test GITHUB_TOKEN, GH_TOKEN, neither
3. Add tests for _get_github_repo: test env var, git config, neither
4. Add tests for _create_github_issue_api: mock urllib, test success response
5. Add tests for API error: HTTPError handling, malformed JSON response

## Acceptance Criteria

- [ ] test_mcp_server.py has >= 8 tests
- [ ] test_frontmatter_tools.py has zero mocked internal functions
- [ ] test_github_issue.py covers token/repo detection and API call paths
- [ ] All tests pass: `uv run pytest tests/unit/test_mcp_server.py tests/unit/test_frontmatter_tools.py tests/unit/test_github_issue.py`

## Testing

- **Existing tests to run**: Full suite to verify no regressions
- **New tests to write**: Replacements for all three files as described
- **Verification command**: `uv run pytest -v tests/unit/test_mcp_server.py tests/unit/test_frontmatter_tools.py tests/unit/test_github_issue.py`
