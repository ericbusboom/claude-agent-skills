---
status: draft
---

# Use Cases

## UC-001: Link Shared Definitions into a Target Repository

- **Actor**: Developer
- **Preconditions**: `claude-agent-skills` is installed via pip/pipx. Target
  repository exists on disk.
- **Main Flow**:
  1. Developer runs `link-claude-agents` from the target repo (or passes
     the target path as an argument).
  2. Script locates the source repo (via the installed package path).
  3. Script creates `.github/copilot/` symlinks for agents, skills, and
     instructions.
  4. Script creates `.claude/` symlinks for agents (directory), skills
     (per-skill `SKILL.md` files), and rules (instructions directory).
  5. Script reports what was linked.
- **Postconditions**: Target repo has working symlinks. Both Copilot and
  Claude Code can discover the shared definitions.
- **Acceptance Criteria**:
  - [ ] `link-claude-agents` creates all expected symlinks
  - [ ] Symlinks resolve to the correct source files
  - [ ] Re-running the command is idempotent (no errors, no duplicates)
  - [ ] Stale symlinks from previous runs are replaced

## UC-002: Preview Changes Before Linking (Dry Run)

- **Actor**: Developer
- **Preconditions**: Same as UC-001.
- **Main Flow**:
  1. Developer runs `link-claude-agents -N` (or `--dry-run`).
  2. Script prints what it would do without creating any symlinks.
- **Postconditions**: No filesystem changes. Developer sees planned actions.
- **Acceptance Criteria**:
  - [ ] Dry run produces output describing all planned symlinks
  - [ ] No files or directories are created or modified

## UC-003: Add New Agent or Skill Definition

- **Actor**: Developer / maintainer of this repo
- **Preconditions**: Source repo is checked out.
- **Main Flow**:
  1. Developer adds a new `.md` file to `agents/` or `skills/`.
  2. Developer re-runs `link-claude-agents` in target repos (or the
     symlinks already pick up the new file for directory-level links).
- **Postconditions**: New definition is available in all linked target repos.
- **Acceptance Criteria**:
  - [ ] New agent files appear via the directory symlink immediately
  - [ ] New skill files require re-running the script (since Claude skills
    use per-file symlinks)

## UC-004: Share SE Process Instructions Across Projects

- **Actor**: Developer
- **Preconditions**: `instructions/` directory contains SE process and testing
  instruction files.
- **Main Flow**:
  1. Developer runs `link-claude-agents` in a target repo.
  2. Script links `instructions/` as `.claude/rules/` for Claude Code.
  3. Script links `instructions/` as `.github/copilot/instructions/` for
     Copilot.
  4. AI assistants in the target repo can now reference the SE process.
- **Postconditions**: Both AI tools discover the instructions automatically.
- **Acceptance Criteria**:
  - [ ] Claude Code loads instruction files from `.claude/rules/`
  - [ ] Copilot loads instruction files from `.github/copilot/instructions/`
  - [ ] Instructions guide AI behavior when planning and implementing work
