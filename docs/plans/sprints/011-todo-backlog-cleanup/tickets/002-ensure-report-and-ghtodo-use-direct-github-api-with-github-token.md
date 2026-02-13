---
id: "002"
title: Ensure report and ghtodo use direct GitHub API with GITHUB_TOKEN
status: todo
use-cases: [SUC-002]
depends-on: []
---

# Ensure report and ghtodo use direct GitHub API with GITHUB_TOKEN

## Description

Audit and update the `/report` and `/ghtodo` skills and the `create_github_issue`
MCP tool to ensure they use direct GitHub API access authenticated via the
`GITHUB_TOKEN` environment variable.

## Acceptance Criteria

- [ ] `/report` skill instructs use of direct GitHub API (not MCP proxy)
- [ ] `/ghtodo` skill instructs use of direct GitHub API (not MCP proxy)
- [ ] `create_github_issue` in `artifact_tools.py` reads GITHUB_TOKEN from env
- [ ] Skills explicitly mention GITHUB_TOKEN as the auth mechanism

## Testing

- **Existing tests to run**: `uv run pytest`
- **New tests to write**: None (audit and content update)
- **Verification command**: `uv run pytest`
