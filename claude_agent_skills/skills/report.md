---
name: report
description: Create a GitHub issue on the claude-agent-skills repository to report bugs or problems encountered while working in another repository
---

# Report Issue Skill

This skill creates a GitHub issue on the `ericbusboom/claude-agent-skills` repository using the GitHub CLI (`gh`). Use this when working in another repository with the SE process MCP server to report bugs, issues, or problems with the CLASI tools, agents, skills, or instructions.

## Process

1. Collect the issue information from the user:
   - **Title**: A concise summary of the bug or problem
   - **Description**: Detailed explanation of the issue including:
     - What you were trying to do
     - What went wrong
     - Steps to reproduce (if applicable)
     - Expected vs. actual behavior
     - Any error messages or logs
     - Context (which skill/agent/instruction was involved)

2. Use `gh` to create the issue on the `ericbusboom/claude-agent-skills` repository:
   ```bash
   gh issue create \
     --repo ericbusboom/claude-agent-skills \
     --title "TITLE" \
     --body "DESCRIPTION"
   ```

3. Confirm the issue was created and provide the issue number/URL.

## Usage

To use this skill, invoke it with the issue details:

```
/report
Title: Bug in execute-ticket skill
Description: The execute-ticket skill fails when the ticket path contains special characters...
```

Or more informally:

```
/report The plan-sprint skill doesn't handle empty sprints correctly
```

## Example

**Input:**
```
/report
The python-expert agent suggests using deprecated libraries without checking their support status
```

**Process:**
1. Parse the user input into title and description
2. Execute: `gh issue create --repo ericbusboom/claude-agent-skills --title "Python-expert agent suggests deprecated libraries" --body "The python-expert agent suggests using deprecated libraries without checking their support status. This can lead to security vulnerabilities and maintenance issues."`
3. Report success with issue URL

**Output:**
```
✅ Issue created successfully!

Issue #42: Python-expert agent suggests deprecated libraries
URL: https://github.com/ericbusboom/claude-agent-skills/issues/42

The issue has been reported and will be reviewed by the maintainers.
```

## Benefits

- **Quick Reporting**: Easily report issues without leaving your workflow
- **Centralized Tracking**: All CLASI-related issues in one place
- **Context Preservation**: Include detailed context about the problem
- **Workflow Integration**: Seamless integration with SE process work

## Notes

- Requires GitHub CLI (`gh`) to be installed and authenticated
- Issues are created with default labels (none) - maintainers will triage
- For urgent issues or discussions, consider creating the issue manually for more control over labels, assignees, etc.
