---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 005 Use Cases

## SUC-001: Inspect Hook Payload After Plan Mode Exit

- **Actor**: Developer debugging the plan-to-todo file-targeting bug
- **Preconditions**: Plan mode has been used and a plan file exists in `~/.claude/plans/`
- **Main Flow**:
  1. Developer exits plan mode (ExitPlanMode tool call)
  2. The PostToolUse hook fires `clasi hook plan-to-todo`
  3. `handle_plan_to_todo` passes the raw payload dict to `plan_to_todo(hook_payload=payload)`
  4. `plan_to_todo()` collects the payload and relevant environment variables
  5. A `## Hook Debug Info` section with a fenced JSON block is appended to the TODO file before writing
  6. Developer reads the TODO file and inspects the payload structure
- **Postconditions**: The created TODO file contains a `## Hook Debug Info` section with the hook payload and env vars as JSON.
- **Acceptance Criteria**:
  - [ ] `handle_plan_to_todo` passes `payload` to `plan_to_todo()` as `hook_payload`
  - [ ] `plan_to_todo()` accepts an optional `hook_payload` parameter (default `None`)
  - [ ] When `hook_payload` is not None, a `## Hook Debug Info` fenced JSON block is appended
  - [ ] The JSON block includes the payload, relevant env vars, `plans_dir`, `plan_file`, and `cwd`
  - [ ] Existing call sites with no `hook_payload` argument are unaffected
  - [ ] `uv run pytest` passes

## SUC-002: Discover and Use the Two Idea-Capture Paths

- **Actor**: Developer (or Claude Code model) who wants to capture an idea or task
- **Preconditions**: CLASI is initialized in the project (`.claude/` populated)
- **Main Flow**:
  1. Developer invokes `/se` with no args and sees `/se plan` listed in the command table
  2. Developer (or model) reads the "When to use" guidance and selects the correct path:
     - Imperative, single-sentence task → `/se todo <text>` for quick capture
     - Exploratory, needs discussion → `/se plan` to enter plan mode
  3. If `/se plan`: model enters plan mode, has the conversation, exits plan mode, and the hook creates the TODO automatically
  4. If `/se todo`: model creates a TODO file immediately from the provided text
- **Postconditions**: The correct capture path was used and a TODO file exists.
- **Acceptance Criteria**:
  - [ ] `clasi/plugin/skills/se/SKILL.md` contains a `/se plan` row in the command table
  - [ ] `clasi/plugin/skills/se/SKILL.md` contains a "When to use /se todo vs /se plan" section
  - [ ] `clasi/plugin/skills/todo/SKILL.md` contains a "When to use this skill vs plan mode" note
  - [ ] `clasi/plugin/agents/team-lead/agent.md` contains a "Capture Ideas and Plans" scenario in the Process section
  - [ ] All three files are mirrored to their `.claude/` counterparts
  - [ ] `clasi init` installs the updated files correctly (idempotent)

## SUC-003: Clean Git History on Sprint Close

- **Actor**: Developer closing a sprint where master has advanced since branching
- **Preconditions**: Sprint branch exists; master has at least one commit made after the sprint branch was created
- **Main Flow**:
  1. Developer calls `close_sprint` (or equivalent)
  2. `merge_branch()` detects the sprint branch is not an ancestor of master
  3. `merge_branch()` runs `git rebase main_branch branch_name` before checking out master
  4. If rebase fails, it is aborted and a `RuntimeError` is raised with the reason
  5. If rebase succeeds, the sprint commits now sit on top of master
  6. `git checkout main_branch` followed by `git merge --no-ff branch_name` creates the merge bubble
  7. `git log --oneline --graph` shows linear sprint commits inside the merge bubble
- **Postconditions**: The sprint branch's commits are rebased onto master before the `--no-ff` merge, giving clean linear history inside the merge bubble.
- **Acceptance Criteria**:
  - [ ] `merge_branch()` runs `git rebase main_branch branch_name` before checkout
  - [ ] On rebase failure, `git rebase --abort` is called and `RuntimeError` is raised
  - [ ] `artifact_tools.py` reports `merge_strategy: "rebase + --no-ff"`
  - [ ] A unit test verifies the rebase step fires when master has advanced after branching
  - [ ] `uv run pytest` passes
