---
status: draft
---

# Sprint 002 Use Cases

## SUC-001: Capture an Idea in the TODO Directory

- **Actor**: Stakeholder (human)
- **Preconditions**: `docs/plans/todo/` directory exists.
- **Main Flow**:
  1. Stakeholder has an idea while the AI agent is busy with other work.
  2. Stakeholder creates a markdown file in `docs/plans/todo/` with a
     descriptive filename.
  3. File contains one or more ideas as level-1 headings with description
     text beneath each.
- **Postconditions**: Idea is captured and will be found during future
  sprint planning.
- **Acceptance Criteria**:
  - [ ] SE instructions document the TODO directory and its purpose
  - [ ] File format is documented (level-1 headings per idea)
  - [ ] Lifecycle is documented (capture -> mine -> done)

## SUC-002: Clean Up Multi-Topic TODO Files

- **Actor**: Developer or AI agent
- **Preconditions**: A TODO file exists with multiple level-1 headings.
- **Main Flow**:
  1. User runs `clasi todo-split`.
  2. Command scans `docs/plans/todo/` for files with multiple level-1
     headings.
  3. For each such file, command extracts each level-1 section into a new
     file named from the heading.
  4. Original file is deleted after successful split.
  5. Files with a single heading or no headings are left unchanged.
- **Postconditions**: Each TODO file contains a single idea.
- **Acceptance Criteria**:
  - [ ] Multi-heading files are split into individual files
  - [ ] New file names are derived from the heading text
  - [ ] Original file is deleted after split
  - [ ] Single-heading and no-heading files are left alone
  - [ ] Command reports what it did

## SUC-003: Mine TODOs During Sprint Planning

- **Actor**: AI agent (project-manager)
- **Preconditions**: TODO directory has files. Stakeholder is planning a
  new sprint.
- **Main Flow**:
  1. During sprint planning, the project-manager reads TODO files.
  2. Agent discusses relevant TODOs with the stakeholder.
  3. Stakeholder selects which TODOs to include in the sprint.
  4. Selected TODO content is incorporated into the sprint document.
  5. Consumed TODO files are moved to `docs/plans/todo/done/`.
- **Postconditions**: Sprint scope includes relevant TODOs. Consumed
  TODO files are archived.
- **Acceptance Criteria**:
  - [ ] Sprint planning workflow includes a TODO mining step
  - [ ] TODO content is incorporated into the sprint document
  - [ ] Consumed TODO files move to `docs/plans/todo/done/`

## SUC-004: Create a Sprint with Merged Document

- **Actor**: AI agent (project-manager)
- **Preconditions**: A sprint is being planned.
- **Main Flow**:
  1. Agent creates the sprint directory.
  2. Sprint has a single primary document (`sprint.md`) that includes
     goals, scope, problem/solution (formerly in brief.md), and test
     strategy.
  3. Separate usecases.md and technical-plan.md still exist within the
     sprint for detailed planning.
  4. No separate brief.md is created.
- **Postconditions**: Sprint has fewer, more focused documents.
- **Acceptance Criteria**:
  - [ ] Sprint template produces sprint.md without separate brief.md
  - [ ] Sprint.md includes problem, solution, goals, scope, test strategy
  - [ ] MCP create_sprint tool uses the updated template
  - [ ] Existing sprints are not retroactively changed

## SUC-005: Create a Project with Single Overview Document

- **Actor**: AI agent (requirements-analyst, architect)
- **Preconditions**: A new project is being started.
- **Main Flow**:
  1. Stakeholder describes the project.
  2. Agent creates a single `docs/plans/overview.md` containing:
     project identity, high-level requirements, technology choices,
     key scenarios, and a rough sprint roadmap.
  3. Detailed architecture and scenarios are deferred to sprint-level
     documents.
  4. Overview document is general and stable across sprints.
- **Postconditions**: Project has a lightweight top-level plan. Detailed
  planning happens per-sprint.
- **Acceptance Criteria**:
  - [ ] `docs/plans/overview.md` replaces separate brief/usecases/tech-plan
  - [ ] Overview includes project identity, requirements, tech stack,
        scenarios, and sprint roadmap
  - [ ] Instructions reflect the new startup workflow
  - [ ] MCP tools for creating top-level artifacts are updated

## SUC-006: Use Scenarios Instead of Use Cases

- **Actor**: AI agent (any)
- **Preconditions**: The process previously used "use cases" terminology.
- **Main Flow**:
  1. Agent follows instructions that reference "scenarios" rather than
     "use cases."
  2. Scenario format is less formal: a narrative description of how a
     feature is used, with acceptance criteria.
  3. All templates, instructions, and skills use the "scenario" term.
- **Postconditions**: Process terminology is consistent.
- **Acceptance Criteria**:
  - [ ] Instructions use "scenario" instead of "use case"
  - [ ] Templates use "scenario" headers and identifiers
  - [ ] Skills reference scenarios not use cases

## SUC-007: Include Mermaid Diagrams in Technical Plans

- **Actor**: AI agent (architect)
- **Preconditions**: A technical plan is being written.
- **Main Flow**:
  1. Architect reads the diagram guidance in instructions.
  2. Architect includes Mermaid diagrams showing subsystem interactions
     and module dependencies.
  3. Diagrams show the system as it will exist at the end of the sprint.
  4. Architect avoids unnecessary diagrams (no swim lanes unless
     multi-system sequencing, no exhaustive class diagrams).
- **Postconditions**: Technical plan includes clear subsystem diagrams.
- **Acceptance Criteria**:
  - [ ] Instructions include Mermaid diagram guidance
  - [ ] Guidance specifies when to use diagrams and when not to
  - [ ] Guidance covers subsystem interaction and module dependency diagrams
  - [ ] Guidance addresses appropriate level of detail

## SUC-008: Access Language-Specific Instructions via MCP

- **Actor**: AI agent (python-expert or other dev agent)
- **Preconditions**: Per-language instructions exist. MCP server is running.
- **Main Flow**:
  1. Agent calls `list_language_instructions` to see available languages.
  2. Agent calls `get_language_instruction("python")` to get Python-specific
     conventions.
  3. Agent follows the language-specific conventions when implementing code.
- **Postconditions**: Agent has language-appropriate guidance beyond the
  general coding standards.
- **Acceptance Criteria**:
  - [ ] `instructions/languages/python.md` exists with Python conventions
  - [ ] MCP tool lists available language instructions
  - [ ] MCP tool returns the full content of a language instruction
  - [ ] Language instructions complement (not duplicate) general coding standards
