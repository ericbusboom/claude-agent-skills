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
3. Use the GitHub MCP server to create the issue:
   - Call the appropriate GitHub tool to create an issue
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

This skill requires the GitHub MCP server to be available in the agent's
environment. The agent must have appropriate GitHub credentials and permissions
to create issues in the repository.

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
