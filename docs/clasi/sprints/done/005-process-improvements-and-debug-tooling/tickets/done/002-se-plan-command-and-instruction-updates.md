---
id: '002'
title: /se plan Command and Instruction Updates
status: done
use-cases:
- SUC-002
depends-on: []
github-issue: ''
todo: plan-link-planning-to-todos-se-plan-command-and-instruction-updates.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# /se plan Command and Instruction Updates

## Description

There are two paths for capturing future work in CLASI — quick capture via `/se todo`
and discussed planning via plan mode — but nothing tells the model (or the developer)
when to use which, and there is no explicit `/se plan` command. The connection between
plan mode and the TODO system is implicit.

This ticket adds `/se plan` to the SE skill command table, adds "when to use" guidance
to both skill files, and adds a "Capture Ideas and Plans" scenario to the team-lead
agent instructions. All changes are markdown only. The six affected files are mirrored
to their `.claude/` counterparts so the live session picks them up immediately.

## Acceptance Criteria

- [x] `clasi/plugin/skills/se/SKILL.md` contains a `/se plan` row in the command table with action "Enter plan mode via `EnterPlanMode`"
- [x] `clasi/plugin/skills/se/SKILL.md` contains a "When to use /se todo vs /se plan" section explaining both paths
- [x] `clasi/plugin/skills/todo/SKILL.md` contains a "When to use this skill vs plan mode" note directing to plan mode when discussion is needed
- [x] `clasi/plugin/agents/team-lead/agent.md` contains a "Capture Ideas and Plans" scenario in the Process section describing both paths and selection heuristics
- [x] `.claude/skills/se/SKILL.md` is identical to `clasi/plugin/skills/se/SKILL.md`
- [x] `.claude/skills/todo/SKILL.md` is identical to `clasi/plugin/skills/todo/SKILL.md`
- [x] `.claude/agents/team-lead/agent.md` is identical to `clasi/plugin/agents/team-lead/agent.md`
- [x] `uv run pytest` passes (no Python changes, but verify nothing broke)

## Implementation Plan

### Approach

Read each source file, make the targeted addition, then copy the updated content to the
corresponding `.claude/` path. Six file writes total. No Python code changes.

### Files to Modify

**`clasi/plugin/skills/se/SKILL.md`** (then mirror to `.claude/skills/se/SKILL.md`)

1. Add a `/se plan` row to the existing command table:
   ```
   | `/se plan` | Enter plan mode for a discussed TODO | Enter plan mode via `EnterPlanMode` |
   ```
2. Add a new section after the table:
   ```markdown
   ## When to use /se todo vs /se plan

   - `/se todo <text>`: Quick capture. The user has a clear idea and just
     wants it recorded. One statement → one TODO file.
   - `/se plan`: The user wants to discuss, explore, and refine an idea
     before capturing it. Enters plan mode for a conversation. On exit,
     the plan-to-todo hook automatically creates the TODO.
   ```

**`clasi/plugin/skills/todo/SKILL.md`** (then mirror to `.claude/skills/todo/SKILL.md`)

Add a note at the end of the file:
```markdown
## When to use this skill vs plan mode

This skill is for **quick capture** — the user has a clear idea and wants it recorded
as a TODO. If the user wants to discuss, explore options, or refine an idea before
capturing it, use plan mode (`EnterPlanMode`) instead. The plan-to-todo hook will
create the TODO automatically when plan mode exits.
```

**`clasi/plugin/agents/team-lead/agent.md`** (then mirror to `.claude/agents/team-lead/agent.md`)

Add a new scenario in the Process section before "Execute TODOs Through a Sprint":
```markdown
### Capture Ideas and Plans

**When:** The stakeholder has ideas or tasks they want to capture for future work,
but not execute now.

Two paths based on the stakeholder's intent:

1. **Quick capture** — The stakeholder gives a direct statement of what to do.
   Invoke the `todo` skill to create a TODO file.
   Example: "Add rate limiting to the API"

2. **Discussed planning** — The stakeholder wants to explore and discuss an idea.
   Enter plan mode (`EnterPlanMode`). Have the conversation, explore the codebase,
   ask clarifying questions, and write the plan. On `ExitPlanMode`, the plan-to-todo
   hook automatically creates the TODO. Do not implement after exit.
   Example: "Let's talk about how we should handle authentication"

**How to tell the difference:**
- Quick capture: imperative statement, single sentence, clear task
- Discussed planning: "let's talk about", "let's plan", "I want to discuss",
  exploratory language, questions about approach
```

### Testing Plan

No automated tests needed (markdown only). Manual verification:
1. Run `clasi init` on a test project — verify the updated files install correctly
2. Invoke `/se` with no args — verify `/se plan` appears in the command table
3. Invoke `/se plan` — verify it enters plan mode
4. Exit plan mode — verify TODO is created and the model stops (does not implement)

### Documentation Updates

The changes are themselves documentation. No additional docs needed.
