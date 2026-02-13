# Using the /report Skill

The `/report` skill allows you to quickly create GitHub issues on the `ericbusboom/claude-agent-skills` repository to report bugs or problems you encounter while using the CLASI (Claude Agent Skills Instructions) tools in any project.

## Prerequisites

- Preferred: `GITHUB_TOKEN` or `GH_TOKEN` set in the environment
- Fallback: GitHub CLI (`gh`) installed and authenticated (`gh auth login`)

## Usage Examples

### Example 1: Simple Bug Report

```
/report The execute-ticket skill doesn't handle special characters in ticket titles correctly
```

This will create an issue with:
- **Title**: "The execute-ticket skill doesn't handle special characters in ticket titles correctly"
- **Body**: Same as title (expanded as needed)

### Example 2: Detailed Bug Report

```
/report
Title: Python-expert agent suggests deprecated libraries
Description: When asking for authentication implementations, the python-expert agent 
suggested using the deprecated 'pycrypto' library instead of 'cryptography'. This 
happened in sprint 003 while working on ticket 005. The agent should check for 
deprecated status before recommending libraries.

Steps to reproduce:
1. Start execute-ticket for an auth-related task
2. Ask python-expert for recommendations
3. Notice deprecated library suggestion

Expected: Recommend actively maintained 'cryptography' library
Actual: Recommended deprecated 'pycrypto' library
```

### Example 3: Quick Issue Report

```
/report plan-sprint doesn't validate empty sprint titles
```

### Example 4: Feature Request

```
/report
It would be helpful if the project-status skill could show a progress percentage 
for each sprint based on completed vs total tickets. Currently it only shows 
counts which makes it hard to quickly assess progress.
```

## What Happens

When you invoke `/report`, the skill will:

1. Parse your input into a title and description (auto-generate title if missing)
2. Create the issue via the GitHub API when a token is available; otherwise use `gh`:
   ```bash
   gh issue create \
     --repo ericbusboom/claude-agent-skills \
     --title "Your Title" \
     --body "Your Description"
   ```
3. Provide you with the issue number and URL for reference

## Output Example

```
✅ Issue created successfully!

Issue #42: Python-expert agent suggests deprecated libraries
URL: https://github.com/ericbusboom/claude-agent-skills/issues/42

The issue has been reported and will be reviewed by the maintainers.
```

## Tips

- **Be specific**: Include which skill, agent, or instruction is involved
- **Include context**: Mention what you were trying to do
- **Add steps**: If it's a bug, include steps to reproduce
- **Show examples**: Include relevant error messages or unexpected output
- **Reference artifacts**: Mention sprint/ticket numbers if applicable

## When to Use /report

Use the `/report` skill when you encounter:

- **Bugs**: Skills, agents, or instructions not working as expected
- **Documentation issues**: Unclear or missing documentation
- **Feature requests**: Ideas for improvements
- **Inconsistencies**: Conflicting guidance from different components
- **Performance issues**: Slow operations or timeouts

## Alternative: Manual Issue Creation

If you need more control (e.g., adding labels, assigning reviewers), you can create issues manually:

```bash
gh issue create --repo ericbusboom/claude-agent-skills
```

Or visit: https://github.com/ericbusboom/claude-agent-skills/issues/new
