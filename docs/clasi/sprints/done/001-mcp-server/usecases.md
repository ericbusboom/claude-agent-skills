---
status: draft
---

# Sprint 001 Use Cases

## SUC-001: Initialize a Repository for CLASI

- **Actor**: Developer
- **Preconditions**: `claude-agent-skills` is installed via pip/pipx. Target
  repository exists on disk.
- **Main Flow**:
  1. Developer runs `clasi init` from the target repo.
  2. `clasi` writes SE process instruction files into `.claude/rules/` and
     `.github/copilot/instructions/`.
  3. `clasi` adds the MCP server configuration to `.claude/settings.json`.
  4. Developer can optionally use `--global` to also add MCP config to the
     global Claude settings.
- **Postconditions**: The repo has instruction files that direct LLMs to
  MCP tools. MCP server is configured and discoverable.
- **Acceptance Criteria**:
  - [ ] `clasi init` creates instruction files in the correct locations
  - [ ] MCP server config is added to `.claude/settings.json`
  - [ ] `--global` flag adds config to global settings
  - [ ] Re-running `clasi init` is safe (idempotent)
  - [ ] No symlinks are created

## SUC-002: LLM Discovers SE Process via MCP

- **Actor**: AI agent (any)
- **Preconditions**: Repo has been initialized with `clasi init`. MCP
  server is running.
- **Main Flow**:
  1. LLM reads instruction files from `.claude/rules/`.
  2. Instructions direct the LLM to call MCP tools for specific activities.
  3. LLM calls `get_se_overview` for the high-level process.
  4. LLM calls activity-specific tools (e.g., `get_instruction` for coding
     standards, `get_agent_definition` for a specific agent).
- **Postconditions**: LLM has the SE process context it needs for the
  current activity.
- **Acceptance Criteria**:
  - [ ] `get_se_overview` returns a coherent process overview
  - [ ] `list_agents` / `list_skills` / `list_instructions` return all items
  - [ ] `get_agent_definition(name)` returns the full agent markdown
  - [ ] `get_skill_definition(name)` returns the full skill markdown
  - [ ] `get_instruction(name)` returns the full instruction markdown

## SUC-003: Create a New Sprint via MCP

- **Actor**: AI agent (project-manager)
- **Preconditions**: MCP server is running. `docs/plans/` exists.
- **Main Flow**:
  1. Agent calls `create_sprint(title="Feature X")`.
  2. MCP server determines the next sprint number (e.g., 002).
  3. MCP server creates the directory `docs/plans/sprints/002-feature-x/`
     with template files: `sprint.md`, `brief.md`, `usecases.md`,
     `technical-plan.md`, and `tickets/` + `tickets/done/` dirs.
  4. MCP server returns the sprint path, number, and template content.
  5. Agent reads and edits the template files to fill in sprint details.
- **Postconditions**: Sprint directory exists with template files ready
  for editing.
- **Acceptance Criteria**:
  - [ ] Sprint number is auto-assigned (sequential)
  - [ ] Directory structure is created with all template files
  - [ ] Templates have correct YAML frontmatter and section structure
  - [ ] Return value includes the sprint path, number, and branch name
  - [ ] Slug is derived from the title (lowercase, hyphenated)

## SUC-004: Create a Ticket within a Sprint via MCP

- **Actor**: AI agent (systems-engineer)
- **Preconditions**: Sprint directory exists.
- **Main Flow**:
  1. Agent calls `create_ticket(sprint_id="001", title="Add auth endpoint")`.
  2. MCP server determines the next ticket number within the sprint.
  3. MCP server creates the ticket file in the sprint's `tickets/` dir
     with a template (YAML frontmatter + sections).
  4. MCP server returns the ticket path, number, and template content.
  5. Agent edits the ticket to fill in details and acceptance criteria.
- **Postconditions**: Ticket file exists with template ready for editing.
- **Acceptance Criteria**:
  - [ ] Ticket number is auto-assigned within the sprint (sequential)
  - [ ] Ticket file has correct YAML frontmatter (id, title, status, etc.)
  - [ ] Template includes sections for description and acceptance criteria
  - [ ] Return value includes the ticket path and number

## SUC-005: Query Sprint and Ticket Status via MCP

- **Actor**: AI agent (project-manager)
- **Preconditions**: Sprints and tickets exist.
- **Main Flow**:
  1. Agent calls `list_sprints(status="active")` to see open sprints.
  2. Agent calls `list_tickets(sprint_id="001")` to see tickets in a sprint.
  3. Agent calls `get_sprint_status(sprint_id="001")` for a summary with
     ticket counts by status.
- **Postconditions**: Agent has structured data about project state.
- **Acceptance Criteria**:
  - [ ] `list_sprints` returns sprints filterable by status
  - [ ] `list_tickets` returns tickets filterable by sprint and status
  - [ ] `get_sprint_status` returns ticket counts (todo, in-progress, done)
  - [ ] Results include file paths for each item

## SUC-006: Update Artifact Status via MCP

- **Actor**: AI agent (project-manager)
- **Preconditions**: A ticket or sprint exists.
- **Main Flow**:
  1. Agent calls `update_ticket_status(path, "in-progress")`.
  2. MCP server updates the YAML frontmatter in the ticket file.
  3. Agent calls `move_ticket_to_done(path)` when ticket is complete.
  4. MCP server moves the ticket file to the sprint's `tickets/done/` dir.
- **Postconditions**: Artifact frontmatter is updated. Completed items
  are in their `done/` directories.
- **Acceptance Criteria**:
  - [ ] `update_ticket_status` modifies frontmatter without changing content
  - [ ] `move_ticket_to_done` moves both ticket and plan files
  - [ ] `close_sprint` moves the entire sprint directory to `done/`

## SUC-007: Create Top-Level Planning Artifacts via MCP

- **Actor**: AI agent (requirements-analyst, architect)
- **Preconditions**: MCP server is running.
- **Main Flow**:
  1. Agent calls `create_brief()` to create `docs/plans/brief.md`.
  2. MCP server creates the file with a template (frontmatter + sections).
  3. Similarly for `create_technical_plan()` and `create_use_cases()`.
- **Postconditions**: Planning artifact exists with template structure.
- **Acceptance Criteria**:
  - [ ] Each creation tool produces a file with correct template
  - [ ] Templates match the artifact formats defined in SE instructions
  - [ ] Tools return the file path and template content
  - [ ] Tools refuse to overwrite existing artifacts (error if already exists)
