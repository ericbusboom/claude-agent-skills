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

## UC-005: Agent Follows Git Workflow During Ticket Execution

- **Actor**: AI agent (python-expert or other dev agent)
- **Preconditions**: A ticket is in-progress. Git repo is initialized.
- **Main Flow**:
  1. Agent reads the git workflow instruction before starting work.
  2. Agent commits completed work at the end of each ticket with a
     conventional commit message referencing the ticket ID.
  3. If the project uses branches, agent creates a feature branch per ticket.
- **Postconditions**: All ticket work is committed with traceable messages.
  No work is lost to context window expiration.
- **Acceptance Criteria**:
  - [ ] Git workflow instruction exists with commit conventions
  - [ ] Instruction covers when to commit, message format, and branch strategy
  - [ ] Dev agents reference the git workflow instruction

## UC-006: Code Review Gate Before Ticket Completion

- **Actor**: AI agent (python-expert via code review skill)
- **Preconditions**: Ticket implementation and tests are complete.
- **Main Flow**:
  1. Before marking a ticket done, the execute-ticket workflow invokes a
     code review step.
  2. The reviewer checks for quality, standards compliance, security, and
     acceptance criteria coverage.
  3. Issues found are fixed before the ticket can be completed.
- **Postconditions**: Every completed ticket has passed code review.
- **Acceptance Criteria**:
  - [ ] execute-ticket skill includes a review step after testing
  - [ ] Code review checks are defined (standards, security, coverage)
  - [ ] Review findings must be resolved before ticket completion

## UC-007: Dev Agent Works Within SE Process Context

- **Actor**: AI agent (python-expert, documentation-expert)
- **Preconditions**: A ticket plan exists. Testing and coding instructions exist.
- **Main Flow**:
  1. Dev agent is given a ticket to implement.
  2. Agent reads the ticket, ticket plan, and relevant instructions (testing,
     coding standards, git workflow).
  3. Agent implements following the plan, conventions, and acceptance criteria.
  4. Agent writes tests per the testing instructions.
- **Postconditions**: Implementation follows project conventions and satisfies
  the ticket plan.
- **Acceptance Criteria**:
  - [ ] python-expert agent references SE artifacts and instructions
  - [ ] documentation-expert agent has Write/Edit tools and references SE process
  - [ ] Dev agents know where to find tickets, plans, and instructions

## UC-008: Agent Recovers From Errors During Ticket Execution

- **Actor**: AI agent (project-manager, python-expert)
- **Preconditions**: A ticket is in-progress and an error occurs (test failure,
  plan gap, ticket too large).
- **Main Flow**:
  1. Agent encounters a problem: tests fail, the plan has a gap, or the
     ticket scope is too large.
  2. Agent follows the error recovery patterns in the SE instructions.
  3. For test failures: diagnose, fix, re-run.
  4. For plan gaps: update the ticket plan, escalate to architect if
     architectural.
  5. For oversized tickets: split the ticket, update dependencies.
- **Postconditions**: Problem is resolved or escalated. Work is not abandoned.
- **Acceptance Criteria**:
  - [ ] SE instructions include error recovery patterns
  - [ ] Patterns cover test failures, plan gaps, and ticket splitting
  - [ ] Escalation path to human is defined for unresolvable issues

## UC-009: Stakeholder Reviews Artifacts Between Phases

- **Actor**: Developer (stakeholder)
- **Preconditions**: An SE phase has just completed (e.g., brief written,
  technical plan written, tickets created).
- **Main Flow**:
  1. Agent completes a phase and presents the output to the stakeholder.
  2. Stakeholder reviews and either approves or requests changes.
  3. If changes requested, agent revises the artifact and re-presents.
  4. Only after approval does the process advance to the next phase.
- **Postconditions**: Each phase output is stakeholder-approved before the
  next phase begins.
- **Acceptance Criteria**:
  - [ ] SE instructions define review gates between phases
  - [ ] project-manager agent pauses for approval at each gate
  - [ ] Approval/revision cycle is documented
