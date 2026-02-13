---
name: ghtodo
description: Create a GitHub issue from user input
---

# GitHub TODO Skill

This skill captures an idea or task as a GitHub issue in the current repository.

## Process

1. Take the user's input (everything after `/ghtodo`).
2. Parse the input to extract:
   - Issue title (first line or summary)
   - Issue body (remaining content)
   - Optional labels (if specified)
3. Create the issue using direct GitHub API access:
   - Prefer the `create_github_issue` CLASI MCP tool, which uses `GITHUB_TOKEN`
     or `GH_TOKEN` from the environment for authentication
   - Fallback: use the `gh` CLI (`gh issue create`)
   - Use markdown formatting for the issue body
4. Confirm the issue was created and provide:
   - Issue number
   - Issue URL
   - Issue title

## Output

Confirm the issue was created with:
- Issue number (e.g., #123)
- Direct link to the issue
- Brief summary of what was created

## Requirements

This skill requires `GITHUB_TOKEN` or `GH_TOKEN` to be set in the environment
for direct GitHub API access. The `gh` CLI is supported as a fallback. The agent
must have appropriate permissions to create issues in the repository.

## Example Usage

```
/ghtodo Add user authentication
Need to implement OAuth2 authentication for the API.
Labels: enhancement, security
```

This would create an issue with:
- Title: "Add user authentication"
- Body: "Need to implement OAuth2 authentication for the API."
- Labels: enhancement, security
