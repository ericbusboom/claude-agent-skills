---
status: draft
---

# Sprint 010 Use Cases

## SUC-001: Agent Self-Reflects After Correction
Parent: UC-010

- **Actor**: AI agent (triggered by stakeholder correction)
- **Preconditions**: Stakeholder corrects or scolds the agent for an error.
- **Main Flow**:
  1. Agent detects stakeholder correction (tone, keywords, explicit feedback).
  2. Agent acknowledges the correction.
  3. Agent produces a self-reflection document in `docs/plans/reflections/`.
  4. Reflection captures: what happened, what should have happened, root
     cause, proposed fix.
- **Postconditions**: Structured feedback is persisted for process improvement.
- **Acceptance Criteria**:
  - [ ] Self-reflection skill exists at `skills/self-reflect.md`
  - [ ] Scold detection instruction loads in every context
  - [ ] `docs/plans/reflections/` directory is used for output
  - [ ] Reflection document has structured sections

## SUC-002: Stakeholder Enables Auto-Approve Mode
Parent: UC-010

- **Actor**: Stakeholder (verbal instruction)
- **Preconditions**: Stakeholder says "auto-approve" or similar.
- **Main Flow**:
  1. Stakeholder instructs agent to auto-approve.
  2. Agent acknowledges and sets session flag.
  3. At each `AskUserQuestion` breakpoint, agent selects the recommended
     (first) option automatically.
  4. Agent logs each auto-approval in conversation output.
- **Postconditions**: Breakpoints are skipped until stakeholder says stop.
- **Acceptance Criteria**:
  - [ ] Auto-approve instruction exists and is always loaded
  - [ ] Agent selects recommended option at each breakpoint
  - [ ] Agent logs that it auto-approved (visible to stakeholder)
  - [ ] Stakeholder can deactivate with "stop auto-approving"

## SUC-003: Version Tag Works in Non-Python Projects
Parent: UC-010

- **Actor**: AI agent (running `tag_version`)
- **Preconditions**: Project has `package.json` but no `pyproject.toml`.
- **Main Flow**:
  1. `tag_version` scans project root for known version files.
  2. Finds `package.json`, reads current version.
  3. Computes next version and updates `package.json`.
  4. Creates git tag.
- **Postconditions**: Version is bumped in the correct ecosystem file.
- **Acceptance Criteria**:
  - [ ] `tag_version` detects `package.json` when no `pyproject.toml` exists
  - [ ] `package.json` version field is updated correctly
  - [ ] Git tag is still created
  - [ ] Existing `pyproject.toml` behavior unchanged
  - [ ] Falls back to git-tag-only if no version file found

## SUC-004: VSCode Discovers CLASI MCP Server
Parent: UC-010

- **Actor**: Developer (using VSCode Copilot agent mode)
- **Preconditions**: CLASI is installed, project has `.vscode/mcp.json`.
- **Main Flow**:
  1. Developer opens project in VSCode.
  2. VSCode reads `.vscode/mcp.json` and discovers CLASI MCP server.
  3. Copilot agent mode can use CLASI tools.
- **Postconditions**: CLASI tools are available in VSCode.
- **Acceptance Criteria**:
  - [ ] `.vscode/mcp.json` exists with correct CLASI server config
  - [ ] Config uses `"type": "stdio"`, `"command": "clasi"`, `"args": ["mcp"]`
