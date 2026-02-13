---
status: complete
---

# Sprint 011 Technical Plan

## Architecture Overview

Three independent changes, each modifying different parts of the codebase:
1. A rule file update (static content)
2. A skill/MCP tool audit and update (Python + skill markdown)
3. An init command extension (Python CLI)

## Component Design

### Component: CLASI SE Process Rule (SUC-001)

**Use Cases**: SUC-001

Update `.claude/rules/clasi-se-process.md` to add an explicit "Default Behavior"
section stating the CLASI SE process is mandatory for all code change requests
unless the user opts out.

Files: `.claude/rules/clasi-se-process.md`

### Component: GitHub API Auth (SUC-002)

**Use Cases**: SUC-002

Audit the `/report` and `/ghtodo` skill definitions and the `create_github_issue`
MCP tool implementation. Ensure they use `GITHUB_TOKEN` from the environment
for direct API access.

Files:
- `claude_agent_skills/skills/report.md`
- `claude_agent_skills/skills/ghtodo.md`
- `claude_agent_skills/artifact_tools.py` (create_github_issue function)

### Component: Copilot Init Support (SUC-003)

**Use Cases**: SUC-003

Extend the `clasi init` CLI command to also generate VS Code Copilot configuration
files (e.g., `.github/copilot-instructions.md`).

Files:
- `claude_agent_skills/cli.py` (init command)
- Copilot template files

## Open Questions

None — all three changes are straightforward.
