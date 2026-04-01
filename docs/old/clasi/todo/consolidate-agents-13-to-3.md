---
status: pending
---

# Agent Consolidation: 13 Agents → 3

## Context

The current CLASI process has 13 agents across 3 tiers. A typical sprint requires 2 top-level dispatches + 4+ sub-dispatches before any code gets written. Each dispatch is a full subagent invocation with context rendering, execution, and contract validation. This makes the process too slow for practical use — the user spends more time waiting on planning overhead than getting code written.

The goal is to collapse to 3 agents with a maximum dispatch depth of 1 (team-lead → planner or team-lead → programmer, never deeper).

## New Architecture

### 3 Agents

| Agent | Absorbs | Role |
|-------|---------|------|
| **team-lead** | sprint-executor, sprint-reviewer, ad-hoc-executor, project-manager, project-architect, todo-worker | Orchestrator. Manages TODOs, dispatches planning, loops over tickets dispatching programmer directly, validates sprint, closes sprint. Now has write access to `docs/clasi/`. |
| **sprint-planner** | architect, architecture-reviewer, technical-lead | Single-dispatch planner. Receives TODOs + goals, produces sprint.md, architecture-update.md, usecases.md, and tickets — all in one session. No sub-dispatches. Uses instructions (not agents) for architecture quality. |
| **programmer** (renamed code-monkey) | code-reviewer (dropped for now) | Implements tickets. Dispatched directly by team-lead, one per ticket. |

### New Dispatch Tree
```
team-lead
  ├── dispatch_to_sprint_planner(...)   # 1 dispatch for all planning
  └── dispatch_to_programmer(...)       # 1 dispatch per ticket, directly
```

### New Sprint Flow
1. team-lead creates sprint, calls `dispatch_to_sprint_planner` (one dispatch)
2. team-lead: stakeholder approval
3. team-lead: acquire lock, loop tickets, call `dispatch_to_programmer` per ticket
4. team-lead: run review checklist inline (no dispatch)
5. team-lead: close sprint

## Implementation Plan (3 Phases)

### Phase 1: Collapse planning chain (sprint-planner absorbs 3 agents)

**Files to modify:**
- `clasi/agents/domain-controllers/sprint-planner/agent.md` — rewrite to do architecture + review + tickets inline. Add sections from architect and technical-lead agent.md.
- `clasi/agents/domain-controllers/sprint-planner/contract.yaml` — remove `delegates_to`, update `allowed_tools`
- `clasi/agents/domain-controllers/sprint-planner/dispatch-template.md.j2` — update to instruct inline architecture work
- `clasi/tools/dispatch_tools.py` — remove `dispatch_to_architect`, `dispatch_to_architecture_reviewer`, `dispatch_to_technical_lead`

**New CLASI instructions** (for sprint-planner subagent, loaded via `get_instruction()`):
- `clasi/instructions/architecture-authoring.md` — from architect agent.md
- `clasi/instructions/architecture-review-checklist.md` — from architecture-reviewer agent.md

**Plan files → merged into tickets**: Sprint-planner produces one file per ticket with an "Implementation Plan" section, not separate plan files.

### Phase 2: Team-lead absorbs execution/review agents

**New `.claude/skills/`** (team-lead absorbed roles become user-invocable skills):
- `.claude/skills/sprint-execution.md` — from sprint-executor: loop over tickets, dispatch programmer, validate each
- `.claude/skills/sprint-review.md` — from sprint-reviewer: validation checklist before closing
- `.claude/skills/out-of-process.md` — from ad-hoc-executor: dispatch programmer directly without sprint ceremony

**Files to modify:**
- `clasi/agents/main-controller/team-lead/agent.md` + `CLAUDE.md` — rewrite process to reference skills instead of dispatching to executor/reviewer/ad-hoc agents
- `clasi/tools/dispatch_tools.py` — remove `dispatch_to_sprint_executor`, `dispatch_to_sprint_reviewer`, `dispatch_to_ad_hoc_executor`. Rename `dispatch_to_code_monkey` → `dispatch_to_programmer`, change allowed_callers to `{"team-lead"}`.
- `clasi/agents/task-workers/code-monkey/` — rename directory to `programmer/`, update agent.md name field
- `clasi/hooks/role_guard.py` — exempt team-lead (tier 0) from write blocks on `docs/clasi/` paths. Team-lead needs to write TODO files, update frontmatter, create sprint review notes.

### Phase 3: Team-lead absorbs project-manager, todo-worker, project-architect

**New `.claude/skills/`**:
- `.claude/skills/project-initiation.md` — from project-manager (initiation mode)
- `.claude/skills/sprint-roadmap.md` — from project-manager (roadmap mode)

**New CLASI instruction**:
- `clasi/instructions/todo-assessment.md` — from project-architect agent.md

**Files to modify:**
- `clasi/agents/main-controller/team-lead/agent.md` + `CLAUDE.md` — reference new skills for initiation/roadmap
- `clasi/tools/dispatch_tools.py` — remove `dispatch_to_project_manager`, `dispatch_to_todo_worker`, `dispatch_to_project_architect`

**Agents to archive** move to an `archived/` until we're sure the new process is working smoothly:
- `clasi/agents/domain-controllers/project-manager/`
- `clasi/agents/domain-controllers/sprint-executor/`
- `clasi/agents/domain-controllers/sprint-reviewer/`
- `clasi/agents/domain-controllers/ad-hoc-executor/`
- `clasi/agents/domain-controllers/todo-worker/`
- `clasi/agents/task-workers/architect/`
- `clasi/agents/task-workers/architecture-reviewer/`
- `clasi/agents/task-workers/technical-lead/`
- `clasi/agents/task-workers/code-reviewer/`
- `clasi/agents/task-workers/project-architect/`

## Verification

After each phase:
1. `uv run pytest` — all existing tests pass
2. Test the dispatch tools that remain: call `dispatch_to_sprint_planner` and `dispatch_to_programmer` with a test sprint
3. Verify removed dispatch tools are gone from `dispatch_tools.py` and their delegation edges are cleaned up
4. Verify role_guard.py allows team-lead to write to `docs/clasi/` after Phase 2
