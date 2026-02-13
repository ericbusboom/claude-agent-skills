---
status: complete
---

# Sprint 011 Use Cases

## SUC-001: Explicit SE Process Default
Parent: N/A

- **Actor**: Agent (Claude Code)
- **Preconditions**: Agent receives a code change request
- **Main Flow**:
  1. Agent reads `.claude/rules/clasi-se-process.md`
  2. Rule clearly states CLASI SE is the default process
  3. Agent follows the process unless user opts out with "out of process", "direct", etc.
- **Postconditions**: Agent uses CLASI SE process by default
- **Acceptance Criteria**:
  - [ ] Rule file explicitly states CLASI SE is the default
  - [ ] Opt-out phrases are documented

## SUC-002: GitHub API Direct Auth
Parent: N/A

- **Actor**: `/report` and `/ghtodo` skills
- **Preconditions**: GITHUB_TOKEN is set in environment
- **Main Flow**:
  1. Skill is invoked
  2. Skill uses direct GitHub API access via `gh` CLI or `create_github_issue` MCP tool
  3. Auth is provided by GITHUB_TOKEN env var
- **Postconditions**: GitHub issue is created with proper auth
- **Acceptance Criteria**:
  - [ ] Both skills use GITHUB_TOKEN for auth
  - [ ] No reliance on external MCP proxying for auth

## SUC-003: Copilot Support in clasi init
Parent: N/A

- **Actor**: Developer running `clasi init`
- **Preconditions**: Developer has a project directory
- **Main Flow**:
  1. Developer runs `clasi init`
  2. Command generates Claude Code config (existing)
  3. Command also generates `.github/copilot-instructions.md` or equivalent
- **Postconditions**: Project has both Claude Code and Copilot configuration
- **Acceptance Criteria**:
  - [ ] `clasi init` generates Copilot config files
  - [ ] Existing Claude Code generation is unchanged
