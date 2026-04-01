---
status: draft
---

# Sprint 004 Use Cases

## SUC-001: Fix clasi init to produce .mcp.json
Parent: UC-004

- **Actor**: Developer setting up a new project
- **Preconditions**: `clasi` is installed via pip/uv
- **Main Flow**:
  1. Developer runs `clasi init` in their project directory.
  2. Command creates `.mcp.json` at the project root with clasi MCP config.
  3. Command creates `.claude/rules/clasi-se-process.md` instruction file.
  4. If `.mcp.json` already exists, the clasi entry is merged in.
- **Postconditions**: `.mcp.json` contains clasi MCP server config
- **Acceptance Criteria**:
  - [ ] `clasi init` creates `.mcp.json` (not `.claude/settings.json`)
  - [ ] Existing `.mcp.json` content is preserved (merge, not overwrite)
  - [ ] Command is idempotent

## SUC-002: Manage TODOs through MCP tools
Parent: UC-004

- **Actor**: AI agent managing the TODO directory
- **Preconditions**: `docs/plans/todo/` exists
- **Main Flow**:
  1. Agent calls `list_todos` to see active TODO items.
  2. Agent calls `move_todo_to_done(filename)` to archive a consumed TODO.
- **Postconditions**: TODO file moved to `docs/plans/todo/done/`
- **Acceptance Criteria**:
  - [ ] `list_todos` returns titles and filenames of active TODOs
  - [ ] `move_todo_to_done` moves file to `done/` subdirectory
  - [ ] Error on nonexistent file

## SUC-003: Dissolve coding standards into language instructions
Parent: UC-004

- **Actor**: AI agent reading coding instructions
- **Preconditions**: `instructions/coding-standards.md` exists with mixed content
- **Main Flow**:
  1. Python-specific content (type hints, imports, style, naming) is moved
     into `instructions/languages/python.md`.
  2. Truly generic content (error handling principles, dependency management)
     stays in a slimmed-down general instruction or is also absorbed.
  3. `coding-standards.md` is removed.
  4. References in other files are updated.
- **Postconditions**: No `coding-standards.md`; content lives in language files
- **Acceptance Criteria**:
  - [ ] `coding-standards.md` deleted
  - [ ] Python content merged into `languages/python.md`
  - [ ] All references updated (system-engineering.md, process_tools.py ACTIVITY_GUIDES)
  - [ ] No content lost

## SUC-004: Read and write frontmatter via MCP
Parent: UC-009

- **Actor**: AI agent inspecting or updating artifact metadata
- **Preconditions**: Target file exists
- **Main Flow**:
  1. Agent calls `read_frontmatter(path)` to get metadata as JSON.
  2. Agent calls `write_frontmatter(path, updates)` to merge updates.
- **Postconditions**: Frontmatter reflects the updates
- **Acceptance Criteria**:
  - [ ] `read_frontmatter` returns JSON dict
  - [ ] `write_frontmatter` merges into existing frontmatter
  - [ ] `write_frontmatter` creates frontmatter on a plain file
  - [ ] Error on nonexistent file

## SUC-005: Transparent done/ path resolution
Parent: UC-009

- **Actor**: AI agent referencing an artifact by its original path
- **Preconditions**: Artifact has been moved to a `done/` subdirectory
- **Main Flow**:
  1. Agent calls an MCP tool with the original path (without `done/`).
  2. The tool's path resolver checks the original path first.
  3. If not found, it checks with `done/` inserted before the filename.
  4. Returns the resolved path or raises an error.
- **Postconditions**: Tool operates on the correct file regardless of location
- **Acceptance Criteria**:
  - [ ] `resolve_artifact_path` finds files in their original location
  - [ ] `resolve_artifact_path` finds files after move to `done/`
  - [ ] Existing MCP tools (update_ticket_status, move_ticket_to_done) use the resolver
  - [ ] Error with clear message when file not found in either location

## SUC-006: Automatic versioning on sprint closure
Parent: UC-004

- **Actor**: AI agent closing a sprint
- **Preconditions**: Sprint is being closed via `close_sprint`
- **Main Flow**:
  1. On sprint closure, version is computed: `<major>.<isodate>.<build>`.
  2. The date is today's ISO date (YYYYMMDD).
  3. Build number increments from the last tag with the same date, or resets
     to 1 if the date changed.
  4. Major only changes by explicit human request.
  5. Version is written to `pyproject.toml`.
  6. Git commit is tagged with `v<version>`.
- **Postconditions**: New git tag exists; `pyproject.toml` has updated version
- **Acceptance Criteria**:
  - [ ] Version format is `<major>.<isodate>.<build>`
  - [ ] Build resets when date changes
  - [ ] Git tag created on merge commit
  - [ ] `pyproject.toml` version updated

## SUC-007: Slash commands for common SE actions
Parent: UC-004

- **Actor**: Developer using Claude Code
- **Preconditions**: CLASI is initialized in the project
- **Main Flow**:
  1. User types `/todo <text>` — AI creates a TODO file from the text.
  2. User types `/next` — AI determines current state and executes the
     next process step.
  3. User types `/status` — AI runs project-status and reports.
- **Postconditions**: Requested action completed
- **Acceptance Criteria**:
  - [ ] `/todo` creates a file in `docs/plans/todo/`
  - [ ] `/next` determines and executes the next process step
  - [ ] `/status` reports project state
  - [ ] Skills are installed as `.claude/skills/` files
