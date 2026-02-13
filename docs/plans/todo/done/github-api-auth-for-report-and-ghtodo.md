---
status: done
sprint: '011'
tickets:
- '002'
---

# Ensure /report and /ghtodo use direct GitHub API access with GITHUB_TOKEN

Verify and update both the `/report` and `/ghtodo` skills so they use direct
GitHub API access (via `gh` CLI or HTTP requests) and authenticate using the
`GITHUB_TOKEN` environment variable, rather than relying on MCP server
proxying or other auth mechanisms.
