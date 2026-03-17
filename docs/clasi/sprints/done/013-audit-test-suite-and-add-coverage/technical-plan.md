---
status: draft
---

# Sprint 013 Technical Plan

## Architecture Overview

This sprint adds no new production code — it improves the test
infrastructure and fills coverage gaps. Changes fall into three layers:

1. **Infrastructure**: pytest-cov dependency, pyproject.toml configuration,
   .gitignore updates
2. **New test files**: test_cli.py (CLI commands)
3. **Rewritten/expanded test files**: test_mcp_server.py,
   test_frontmatter_tools.py, test_github_issue.py, test_artifact_tools.py,
   test_process_tools.py

## Current State

| File | Tests | Quality | Action |
|------|-------|---------|--------|
| test_state_db.py | 42 | Strong | No changes |
| test_artifact_tools.py | 34 | Strong | Add close/insert edge cases |
| test_frontmatter.py | 18 | Strong | No changes |
| test_init_command.py | 27 | Strong | No changes |
| test_process_tools.py | 20 | Adequate | Strengthen assertions, add error paths |
| test_todo_tools.py | 17 | Adequate | No changes (low priority) |
| test_todo_split.py | 19 | Adequate | No changes (low priority) |
| test_resolve_artifact_path.py | 9 | Adequate | No changes |
| test_versioning.py | 20 | Adequate | No changes |
| test_content_smoke.py | 14 | Adequate | No changes |
| test_frontmatter_tools.py | 11 | Shallow | Rewrite: remove mocking |
| test_mcp_server.py | 2 | Shallow | Expand to 10+ tests |
| test_github_issue.py | 8 | Shallow | Rewrite: test real fallback |
| (new) test_cli.py | 0 | Missing | Create from scratch |

## Component Design

### Component: Coverage Infrastructure

**Use Cases**: SUC-001, SUC-002

Add `pytest-cov` to `[project.optional-dependencies]` dev group. Configure
in pyproject.toml:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=claude_agent_skills --cov-report=term-missing --cov-report=html"

[tool.coverage.run]
branch = true

[tool.coverage.report]
fail_under = 85
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.",
    "if TYPE_CHECKING:",
]
```

Add `htmlcov/` to .gitignore.

### Component: MCP Server Tests (test_mcp_server.py rewrite)

**Use Cases**: SUC-003

Replace the 2 trivial tests with:
- Test that `server` is a FastMCP instance with name "clasi"
- Test that content_path resolves to valid directories (agents, skills, etc.)
- Test that all expected MCP tools are registered on the server
- Test tool count matches expected number
- Test tool names match expected set

Key approach: import the server object and inspect its registered tools
rather than starting the server. Use `server.list_tools()` or inspect
internal tool registry.

### Component: Frontmatter Tools Tests (test_frontmatter_tools.py rewrite)

**Use Cases**: SUC-003

Remove mocking of resolve_artifact_path. Instead, create real file
structures in tmp_path and test end-to-end:
- Read frontmatter from file at original path
- Read frontmatter from file in done/ subdirectory
- Write/merge frontmatter updates to real files
- Error on missing files
- Handle files without existing frontmatter

### Component: GitHub Issue Tests (test_github_issue.py rewrite)

**Use Cases**: SUC-003

Current tests only validate the metadata stub. Expand to:
- Test metadata fallback when no token available (current behavior)
- Test _create_github_issue_api with mocked urllib (success path)
- Test API error handling (HTTPError, malformed JSON)
- Test token detection (_get_github_token with env vars)
- Test repo detection (_get_github_repo)
- Test label handling

### Component: CLI Tests (test_cli.py — new file)

**Use Cases**: SUC-004

Use Click's CliRunner to test all three CLI commands:
- `clasi init` — verify file creation in tmp directory
- `clasi mcp` — verify it attempts to start server (mock run_server)
- `clasi todo-split` — verify file splitting behavior
- Error cases: missing directories, invalid arguments
- Exit codes: 0 for success, non-zero for errors

### Component: Complex Artifact Operation Tests

**Use Cases**: SUC-005

Add to test_artifact_tools.py:
- **close_sprint**: Test full closure flow including versioning (mock git
  tag, verify version file update, verify sprint moved to done/)
- **insert_sprint**: Test inserting between 3+ sprints, verify all
  renumbered correctly, verify state DB updated, verify frontmatter IDs
  updated
- **move_ticket_to_done**: Test with associated plan file, verify both
  moved; test without plan file; test already-in-done path

### Component: Process Tools Test Expansion

**Use Cases**: SUC-003

Strengthen test_process_tools.py:
- Test get_use_case_coverage with real sprint structures containing
  parent references
- Test get_activity_guide for invalid activity names (error handling)
- Test _get_definition for missing names (error message lists available)
- Replace substring assertions with structural validation

## Open Questions

None — the audit data is comprehensive and the approach is straightforward.
