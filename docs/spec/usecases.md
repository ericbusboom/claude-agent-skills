# CLASI — Use Cases

## Actor Glossary

| Actor | Description |
|---|---|
| **Stakeholder** | The human who owns the project. Interacts with team-lead only. |
| **Team Lead** | Tier 0 dispatcher. Routes requests, validates returns, reports to stakeholder. |
| **Domain Controller** | Tier 1 agent owning one process phase (e.g., sprint-planner, sprint-executor). |
| **Task Worker** | Tier 2 leaf agent implementing atomic units (e.g., code-monkey, architect). |
| **MCP Server** | The CLASI MCP server that manages state, dispatch logging, and lifecycle enforcement. |

---

## UC-001 — Bootstrap a New Project

**Actor**: Stakeholder, Team Lead, Project Manager, Project Architect
**Preconditions**: No `overview.md` exists in `docs/clasi/`. A written specification file exists.

**Main Flow**:

```mermaid
sequenceDiagram
    participant S as Stakeholder
    participant TL as Team Lead
    participant PM as Project Manager
    participant PA as Project Architect

    S->>TL: "Start a project" + spec file path
    TL->>PM: dispatch_to_project_manager(mode="initiation", spec_file)
    PM-->>TL: {status: success, files: [overview.md, specification.md, usecases.md]}
    TL->>TL: Verify all three files exist

    alt TODOs exist in docs/clasi/todo/
        TL->>PA: dispatch_to_project_architect(todo_files)
        PA-->>TL: {assessments: [...]}
        TL->>PM: dispatch_to_project_manager(mode="roadmap", assessments, goals)
        PM-->>TL: {sprint_files: [...]}
    end

    TL->>S: Present roadmap for feedback
```

**Postconditions**:
- `docs/clasi/overview.md`, `specification.md`, `usecases.md` exist and contain full stakeholder detail.
- If TODOs were present, a sprint roadmap groups them into lightweight `sprint.md` files.
- Stakeholder has reviewed and acknowledged the roadmap.

**Error Flows**:
- If project-manager returns without all three files: re-dispatch with instructions to complete missing artifacts.
- If MCP server unavailable: halt and instruct stakeholder to check `.mcp.json`.

---

## UC-002 — Execute TODOs Through a Full Sprint

**Actor**: Stakeholder, Team Lead, Sprint Planner, Sprint Executor, Sprint Reviewer
**Preconditions**: No sprint is currently open. One or more TODOs or issues exist.

**Main Flow**:

```mermaid
sequenceDiagram
    participant S as Stakeholder
    participant TL as Team Lead
    participant TW as TODO Worker
    participant SP as Sprint Planner
    participant SE as Sprint Executor
    participant SR as Sprint Reviewer
    participant MCP as MCP Server

    S->>TL: "Run these TODOs"
    opt Raw ideas (not yet files)
        TL->>TW: dispatch_to_todo_worker(action="create")
        TW-->>TL: {todo_files: [...]}
    end

    TL->>MCP: create_sprint(title)
    MCP-->>TL: {sprint_id, sprint_directory}

    TL->>SP: dispatch_to_sprint_planner(mode="detail", todo_ids, goals)
    SP-->>TL: {sprint.md, usecases.md, architecture-update.md, tickets/}

    TL->>S: Present sprint plan
    S->>TL: Approve
    TL->>MCP: record_gate_result("stakeholder_approval", "passed")
    TL->>MCP: acquire_execution_lock(sprint_id)
    MCP-->>TL: {branch}

    TL->>SE: dispatch_to_sprint_executor(tickets)
    SE-->>TL: {status: success, all tickets done}

    TL->>SR: dispatch_to_sprint_reviewer
    SR-->>TL: {verdict: "pass"}

    TL->>MCP: close_sprint(sprint_id, branch)
    TL->>S: Sprint closed
```

**Postconditions**:
- All tickets are in `done` status and moved to `tickets/done/`.
- Sprint branch is merged to main.
- Sprint directory is archived to `sprints/done/`.
- Version is bumped and tagged.

**Error Flows**:
- Sprint-reviewer returns `fail`: team-lead addresses blocking issues and re-dispatches.
- Sprint-executor fails to complete a ticket after 2 re-dispatches: escalates to stakeholder.
- `close_sprint` fails: team-lead reads error, addresses issue, retries.

---

## UC-003 — Plan a Sprint Without Executing It

**Actor**: Stakeholder, Team Lead, Sprint Planner
**Preconditions**: Stakeholder explicitly wants to review the plan before execution begins.

**Main Flow**:

```mermaid
sequenceDiagram
    participant S as Stakeholder
    participant TL as Team Lead
    participant SP as Sprint Planner
    participant MCP as MCP Server

    S->>TL: "Plan a sprint but don't run it yet"
    TL->>MCP: create_sprint(title)
    MCP-->>TL: {sprint_id, sprint_directory}

    TL->>SP: dispatch_to_sprint_planner(mode="detail")
    SP-->>TL: {sprint.md, architecture-update.md, tickets/}

    TL->>S: Present plan
    S->>TL: Approve
    TL->>MCP: record_gate_result("stakeholder_approval", "passed")
    TL->>S: "Sprint ready for execution when you give the go-ahead"
```

**Postconditions**:
- Sprint directory is fully populated.
- Stakeholder approval gate is recorded.
- Execution lock is NOT acquired.
- Sprint remains in `ticketing` phase.

---

## UC-004 — Add a TODO to an Open Sprint

**Actor**: Stakeholder, Team Lead, Sprint Planner, Sprint Executor
**Preconditions**: A sprint is currently open and in the `executing` phase.

**Main Flow**:

```mermaid
sequenceDiagram
    participant S as Stakeholder
    participant TL as Team Lead
    participant SP as Sprint Planner
    participant SE as Sprint Executor
    participant MCP as MCP Server

    S->>TL: "Add this TODO to the current sprint"
    TL->>MCP: list_sprints()
    MCP-->>TL: open sprint ID, directory, branch
    TL->>SP: dispatch_to_sprint_planner(mode="add_to_sprint", todo_ids)
    SP-->>TL: {new_ticket_files: [...]}
    TL->>SE: dispatch_to_sprint_executor(tickets=[new tickets only])
    SE-->>TL: {status: success}
    TL->>S: New TODO implemented and committed
```

**Postconditions**:
- New ticket(s) are created, implemented, and moved to `done/`.
- No new sprint branch is created; changes are on the existing sprint branch.

**Error Flows**:
- If sprint is not in `executing` phase: team-lead informs stakeholder and suggests waiting.

---

## UC-005 — Close a Completed Sprint

**Actor**: Stakeholder, Team Lead, Sprint Reviewer, MCP Server
**Preconditions**: Sprint is fully executed; all tickets have `status: done`.

**Main Flow**:

```mermaid
sequenceDiagram
    participant S as Stakeholder
    participant TL as Team Lead
    participant SR as Sprint Reviewer
    participant MCP as MCP Server

    S->>TL: "Close the sprint"
    TL->>SR: dispatch_to_sprint_reviewer(sprint_id, sprint_directory)
    SR-->>TL: {verdict: "pass", checklist: [...]}

    TL->>MCP: close_sprint(sprint_id, branch_name)
    Note over MCP: Merges branch → main\nArchives sprint directory\nBumps version, pushes tags\nDeletes sprint branch
    MCP-->>TL: {status: success}
    TL->>S: Sprint NNN closed and merged
```

**Postconditions**:
- Sprint branch is deleted.
- Sprint directory is in `sprints/done/`.
- Version is bumped and tagged.
- Execution lock is released.

**Error Flows**:
- Sprint-reviewer returns `fail`: team-lead reports blocking issues to stakeholder before proceeding.

---

## UC-006 — Make an Out-of-Process Change

**Actor**: Stakeholder, Team Lead, Ad-Hoc Executor, Code Monkey, Code Reviewer
**Preconditions**: Stakeholder has explicitly authorized OOP execution (says "out of process", "direct change", or `/oop`).

**Main Flow**:

```mermaid
sequenceDiagram
    participant S as Stakeholder
    participant TL as Team Lead
    participant AH as Ad-Hoc Executor
    participant CM as Code Monkey
    participant CR as Code Reviewer

    S->>TL: "/oop: Fix the typo in the config loader"
    TL->>AH: dispatch_to_ad_hoc_executor(task, scope_directory)
    AH->>CM: dispatch_to_code_monkey(...)
    CM-->>AH: code written, tests passing
    AH->>AH: Run full test suite
    opt Non-trivial change
        AH->>CR: dispatch_to_code_reviewer(...)
        CR-->>AH: {verdict: "PASS"}
    end
    AH->>AH: Commit to current branch
    AH-->>TL: {status: success, commit: "abc1234"}
    TL->>S: Change committed: abc1234
```

**Postconditions**:
- Change is committed directly to the current branch.
- Full test suite passes.
- No sprint directory, tickets, or architecture artifacts created.

**Error Flows**:
- If the change is larger than expected (would normally warrant a sprint): ad-hoc-executor flags this to team-lead, who asks stakeholder whether to continue OOP or switch to a sprint.

---

## UC-007 — Create a TODO from Stakeholder Input

**Actor**: Stakeholder, Team Lead, TODO Worker
**Preconditions**: Stakeholder has a new idea or feature request.

**Main Flow**:

1. Stakeholder provides raw, conversational text describing the idea.
2. Team-lead dispatches to todo-worker with `action="create"` and the raw text.
3. TODO Worker interprets the input, structures it into a proper TODO file with:
   - A clear, descriptive title
   - YAML frontmatter (`status: pending`)
   - A Problem section
   - A Desired Behavior section
4. TODO Worker creates the file using the CLASI `todo` MCP skill.
5. Returns the file path to team-lead.

**Postconditions**:
- A new `.md` file exists in `docs/clasi/todo/`.
- File has proper frontmatter and structure.

---

## UC-008 — Import GitHub Issues as TODOs

**Actor**: Stakeholder, Team Lead, TODO Worker
**Preconditions**: GitHub issues exist in the project repository.

**Main Flow**:

1. Stakeholder provides issue URLs or a repository reference.
2. Team-lead dispatches to todo-worker with `action="import"` and the issue references.
3. TODO Worker uses the `gh-import` skill to:
   - Fetch each issue via the `gh` CLI.
   - Check for existing TODOs with matching GitHub issue URLs (skip duplicates).
   - Create a TODO file preserving the issue title, body, labels, and assignee.
   - Add a reference back to the GitHub issue URL.
4. Returns import results (created files, skipped duplicates, any failures).

**Postconditions**:
- Each imported issue has a corresponding TODO file in `docs/clasi/todo/`.
- No duplicate TODOs created.

---

## UC-009 — Sprint Planning (Internal): Architecture Phase

**Actor**: Sprint Planner, Architect, Architecture Reviewer
**Preconditions**: Sprint directory exists; `sprint.md` is populated. Sprint is in `planning_docs` phase.

**Main Flow**:

```mermaid
sequenceDiagram
    participant SP as Sprint Planner
    participant ARC as Architect
    participant ARCR as Architecture Reviewer
    participant MCP as MCP Server

    SP->>ARC: dispatch_to_architect(sprint_id, sprint_directory)
    ARC-->>SP: architecture-update.md written

    SP->>MCP: advance_sprint_phase(sprint_id)
    Note over MCP: planning_docs → architecture_review

    SP->>ARCR: dispatch_to_architecture_reviewer(sprint_id, sprint_directory)
    ARCR-->>SP: {verdict: "APPROVE"}

    SP->>MCP: record_gate_result("architecture_review", "passed")
    SP->>MCP: advance_sprint_phase(sprint_id)
    Note over MCP: architecture_review → stakeholder_review
```

**Error Flows**:
- Architecture reviewer returns `REVISE`: sprint-planner sends feedback to architect and re-dispatches. Maximum 2 iterations before escalating to team-lead.
- Architecture reviewer returns `APPROVE WITH CHANGES`: sprint-planner records the gate as passed and carries the advisory items into ticket notes.

---

## UC-010 — Sprint Execution (Internal): Ticket Execution Loop

**Actor**: Sprint Executor, Code Monkey, Code Reviewer
**Preconditions**: Sprint is in `executing` phase; tickets exist in `tickets/` with `status: todo`.

**Main Flow**:

```mermaid
sequenceDiagram
    participant SE as Sprint Executor
    participant CM as Code Monkey
    participant CR as Code Reviewer
    participant MCP as MCP Server

    loop For each ticket in dependency order
        SE->>SE: Verify all depends-on tickets are done
        SE->>MCP: update_ticket_status(ticket_id, "in-progress")
        SE->>CM: dispatch_to_code_monkey(ticket_path, plan_path, scope)
        CM-->>SE: code written, tests passing, ticket frontmatter updated

        SE->>SE: Validate: all criteria checked, status=done, tests pass
        alt Validation fails (≤2 times)
            SE->>CM: re-dispatch with specific feedback
        else Validation passes
            SE->>MCP: move_ticket_to_done(ticket_id)
            SE->>SE: Commit ticket move
        end
    end

    SE->>MCP: update sprint status = done
```

**Postconditions**:
- All tickets are in `tickets/done/` with `status: done`.
- Full test suite passes after each ticket.
- All changes committed on the sprint branch.

**Error Flows**:
- Ticket fails validation after 2 re-dispatches: sprint-executor escalates to team-lead with a detailed report.

---

## UC-011 — Code Review (Internal): Two-Phase Review

**Actor**: Code Reviewer
**Preconditions**: Code-monkey has completed implementation. Sprint-executor has requested review.

**Main Flow**:

```mermaid
flowchart TD
    START[Receive review request] --> P1[Phase 1: Correctness]
    P1 --> CHECK{All acceptance\ncriteria pass?}
    CHECK -->|No| FAIL1[Return Phase 1 FAIL\nwith specific findings]
    CHECK -->|Yes| P2[Phase 2: Quality]
    P2 --> ISSUES{Critical or\nmajor issues?}
    ISSUES -->|Yes| FAIL2[Return Phase 2 FAIL\nwith severity rankings]
    ISSUES -->|No| PASS[Return PASS verdict]
```

**Phase 1 checks**:
- Every acceptance criterion is individually evaluated: PASS or FAIL
- Tests exist for each criterion and pass
- No criteria silently skipped or partially implemented

**Phase 2 checks** (only if Phase 1 passes):
- Coding standards compliance
- Security (injection risks, hardcoded secrets, missing validation)
- Architectural consistency
- Maintainability (naming, abstraction, complexity)

**Severity levels**: Critical (must fix) → Major (should fix) → Minor (fix if time permits) → Suggestion (consider for future)

**Postconditions**:
- Review document produced with overall PASS or FAIL verdict.
- Blocking issues identified with specific file locations and remediation guidance.

---

## UC-012 — Architecture Review (Internal): Sprint Architecture Validation

**Actor**: Architecture Reviewer
**Preconditions**: Architect has written `architecture-update.md`. Sprint is in `architecture_review` phase.

**Main Flow**:

1. Read the current consolidated architecture from `docs/clasi/architecture/`.
2. Read the sprint's `architecture-update.md`.
3. Read `instructions/architectural-quality.md`.
4. Explore the codebase with Grep/Glob to check for drift between documented and actual architecture.
5. Evaluate against all review criteria (version consistency, codebase alignment, design quality, anti-patterns, risks).
6. Produce review with verdict, design quality assessment, and findings.

**Verdict guidelines**:
- **APPROVE**: No significant issues.
- **APPROVE WITH CHANGES**: Contained minor issues fixable during implementation.
- **REVISE**: Circular dependencies, god components, inconsistency between Sprint Changes and document body, or significant unaccounted codebase drift.

**Postconditions**:
- Review document produced with verdict, design quality assessment, and (if applicable) blocking findings.
- Gate result recorded by sprint-planner based on the verdict.

---

## UC-013 — Check Project Status

**Actor**: Stakeholder, Team Lead
**Preconditions**: Project has been initiated.

**Main Flow**:

1. Stakeholder asks for a status update.
2. Team-lead calls `list_sprints()` and `get_sprint_status(sprint_id)` for any open sprints.
3. Team-lead reads `docs/clasi/` to identify which artifacts exist.
4. Team-lead reports:
   - Which phase the project is in (initiation, sprint planning, executing, etc.)
   - Which sprint is open (if any) and its current phase
   - How many tickets are done vs. remaining
   - What the next action is

**Postconditions**: Stakeholder has a clear, current picture of project state.
