---
status: draft
---

# Sprint 012 Use Cases

## SUC-001: Generate AGENTS.md

- **Actor**: Developer running `clasi init`
- **Preconditions**: Target directory exists
- **Main Flow**:
  1. `clasi init` generates an `AGENTS.md` at the project root
  2. The file contains a high-level overview of the CLASI SE process
  3. The overview directs agents to the MCP server for detailed instructions
- **Postconditions**: `AGENTS.md` exists with SE process guidance
- **Acceptance Criteria**:
  - [ ] `AGENTS.md` is created at the project root
  - [ ] Content covers: starting a project, opening a sprint, working on tickets
  - [ ] References MCP tools for detailed instructions
  - [ ] Idempotent (re-running updates without duplicating)

## SUC-002: Remove Copilot mirror, rely on AGENTS.md

- **Actor**: Developer running `clasi init`
- **Preconditions**: Target directory exists
- **Main Flow**:
  1. `clasi init` no longer creates `.github/copilot/instructions/` files
  2. Copilot picks up instructions from `AGENTS.md` instead
- **Postconditions**: No `.github/copilot/instructions/` files created
- **Acceptance Criteria**:
  - [ ] `.github/copilot/instructions/` is not created by `clasi init`
  - [ ] Existing copilot mirror tests are updated/removed

## SUC-003: Symlink .claude to .codex

- **Actor**: Developer running `clasi init`
- **Preconditions**: `.claude/` directory exists after init
- **Main Flow**:
  1. `clasi init` creates a `.codex` symlink pointing to `.claude`
  2. ChatGPT Codex reads `.codex/` and finds skills/rules
- **Postconditions**: `.codex` symlink exists pointing to `.claude`
- **Acceptance Criteria**:
  - [ ] `.codex` is a symlink to `.claude`
  - [ ] Works on macOS and Linux
  - [ ] Idempotent (re-running doesn't break existing symlink)

## SUC-004: Add .gitignore entries for installed files

- **Actor**: Developer running `clasi init`
- **Preconditions**: Target directory exists
- **Main Flow**:
  1. `clasi init` appends entries to `.gitignore` for installed files
  2. Entries cover `.claude/`, `.codex`, `.mcp.json`, `AGENTS.md`
- **Postconditions**: `.gitignore` excludes CLASI-installed files
- **Acceptance Criteria**:
  - [ ] `.gitignore` is created or appended to
  - [ ] Entries are not duplicated on re-run
  - [ ] Covers all files installed by `clasi init`
