---
status: draft
sprint: "003"
---

# Sprint 003 Use Cases

## SUC-001: Capture an Idea in the TODO Directory
Parent: UC-004

- **Actor**: Stakeholder (human)
- **Preconditions**: `docs/plans/todo/` directory exists.
- **Main Flow**:
  1. Stakeholder has an idea while the AI agent is busy.
  2. Stakeholder creates a markdown file in `docs/plans/todo/` with a
     descriptive filename.
  3. File contains one or more ideas as level-1 headings with description.
- **Postconditions**: Idea is captured for future sprint planning.
- **Acceptance Criteria**:
  - [ ] SE instructions document the TODO directory and its purpose
  - [ ] File format is documented (level-1 headings per idea)
  - [ ] Lifecycle is documented (capture -> mine -> done)

## SUC-002: Clean Up Multi-Topic TODO Files
Parent: UC-004

- **Actor**: Developer or AI agent
- **Preconditions**: A TODO file exists with multiple level-1 headings.
- **Main Flow**:
  1. User runs `clasi todo-split`.
  2. Command scans `docs/plans/todo/` for files with multiple headings.
  3. Each heading section is extracted into a new file named from the heading.
  4. Original file is deleted after successful split.
- **Postconditions**: Each TODO file contains a single idea.
- **Acceptance Criteria**:
  - [ ] Multi-heading files split into individual files
  - [ ] New file names derived from heading text (slugified)
  - [ ] Original file deleted after split
  - [ ] Single-heading and no-heading files left alone

## SUC-003: Mine TODOs During Sprint Planning
Parent: UC-004

- **Actor**: AI agent (project-manager)
- **Preconditions**: TODO directory has files. A sprint is being planned.
- **Main Flow**:
  1. During sprint planning, project-manager reads TODO files.
  2. Agent discusses relevant TODOs with stakeholder.
  3. Stakeholder selects which TODOs to include.
  4. Selected content is incorporated into sprint document.
  5. Consumed TODO files move to `docs/plans/todo/done/`.
- **Postconditions**: Sprint scope includes relevant TODOs. Consumed files
  archived.
- **Acceptance Criteria**:
  - [ ] Sprint planning workflow includes TODO mining step
  - [ ] Consumed TODO files move to `docs/plans/todo/done/`

## SUC-004: Create a Sprint with Merged Document
Parent: UC-004

- **Actor**: AI agent (project-manager)
- **Preconditions**: A sprint is being planned.
- **Main Flow**:
  1. Agent creates sprint directory.
  2. Sprint has a single primary document (`sprint.md`) that includes goals,
     scope, problem/solution, test strategy.
  3. Separate usecases.md and technical-plan.md still exist for detail.
  4. No separate brief.md is created.
- **Postconditions**: Sprint has fewer, more focused documents.
- **Acceptance Criteria**:
  - [ ] Sprint template produces sprint.md without separate brief.md
  - [ ] Sprint.md includes problem, solution, goals, scope, test strategy
  - [ ] MCP `create_sprint` uses updated template

## SUC-005: Create a Project with Single Overview Document
Parent: UC-009

- **Actor**: AI agent (requirements-analyst, architect)
- **Preconditions**: A new project is being started.
- **Main Flow**:
  1. Stakeholder describes the project.
  2. Agent creates `docs/plans/overview.md` containing project identity,
     high-level requirements, tech stack, key scenarios, sprint roadmap.
  3. Detailed architecture and scenarios deferred to sprint-level documents.
- **Postconditions**: Lightweight top-level plan. Detailed planning per-sprint.
- **Acceptance Criteria**:
  - [ ] `docs/plans/overview.md` replaces separate brief/usecases/tech-plan
  - [ ] Instructions reflect the new startup workflow
  - [ ] MCP tools for top-level artifacts updated

## SUC-006: Include Mermaid Diagrams in Technical Plans
Parent: UC-004

- **Actor**: AI agent (architect)
- **Preconditions**: A technical plan is being written.
- **Main Flow**:
  1. Architect reads diagram guidance in instructions.
  2. Architect includes Mermaid diagrams for subsystem interactions and
     module dependencies.
  3. Diagrams show target state at sprint end.
  4. Unnecessary diagrams avoided (no swim lanes unless multi-system
     sequencing, no exhaustive class diagrams).
- **Postconditions**: Technical plan includes clear subsystem diagrams.
- **Acceptance Criteria**:
  - [ ] Instructions include Mermaid diagram guidance
  - [ ] Guidance specifies when to use and when not to
  - [ ] Covers subsystem interaction and module dependency diagrams

## SUC-007: Access Language-Specific Instructions via MCP
Parent: UC-009

- **Actor**: AI agent (python-expert or other dev agent)
- **Preconditions**: Per-language instructions exist. MCP server running.
- **Main Flow**:
  1. Agent calls `list_language_instructions` to see available languages.
  2. Agent calls `get_language_instruction("python")` for Python conventions.
  3. Agent follows language-specific conventions when implementing.
- **Postconditions**: Agent has language-appropriate guidance.
- **Acceptance Criteria**:
  - [ ] `instructions/languages/python.md` exists
  - [ ] MCP tool lists available language instructions
  - [ ] MCP tool returns full content of a language instruction
