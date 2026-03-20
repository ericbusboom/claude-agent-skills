---
status: pending
---

# Missing Sub-Dispatch Logs in E2E Output

**Do not implement yet.**

## Problem

The e2e test project (`tests/e2e/project/docs/clasi/log/`) shows that
only team-lead-level dispatches are logged. Sub-dispatches from
sprint-executor and sprint-planner are completely absent despite the
agent definitions requiring them.

### What IS logged (per sprint)

Each sprint directory under `log/sprints/<sprint>/` contains exactly
two files:

- `sprint-planner-001.md` -- team-lead -> sprint-planner (planning)
- `sprint-planner-002.md` -- team-lead -> sprint-executor (execution)

Plus one adhoc log: `log/adhoc/001.md` -- team-lead -> requirements-narrator.

That is the complete set. Nine log files total across four sprints plus
one adhoc dispatch.

### What is MISSING

**Sprint-executor -> code-monkey logs (ticket execution):**
The sprint-executor dispatches code-monkey for each ticket. Across four
sprints with ~6 tickets total, there should be at least 6
`ticket-<NNN>-001.md` files. There are zero. The `log_dispatch` routing
in `dispatch_log.py` supports `ticket_id` and would create these files
at `log/sprints/<sprint>/ticket-<ticket>-NNN.md`, but sprint-executor
never calls `log_subagent_dispatch`.

**Sprint-planner -> architect/reviewer/technical-lead logs (ticket creation):**
The sprint-planner dispatches architect, architecture-reviewer, and
technical-lead during planning. These sub-dispatches are also not logged.
The current `sprint-planner-NNN.md` prefix in `dispatch_log.py` routing
only applies when there is no `ticket_id`, which means planner
sub-dispatches would also get the `sprint-planner-` prefix -- but there
is no mechanism to distinguish team-lead -> sprint-planner from
sprint-planner -> architect. A prefix based on the child agent name
would be clearer.

### Root cause

Sprint 024 ticket 009 ("All Dispatching Agents Must Log Subagent
Dispatches") added logging instructions to the sprint-executor and
sprint-planner agent definitions. The instructions are present in:

- `claude_agent_skills/agents/domain-controllers/sprint-executor/agent.md`
  (steps 3c, 3e, and the final rule)
- `claude_agent_skills/agents/domain-controllers/sprint-planner/agent.md`
  (steps 3, 6, 9, and the final rule)

However, the e2e output proves the agents are not following these
instructions. The instructions exist but they are not effective. Possible
reasons:

1. **Context window pressure** -- by the time the agent is deep in
   ticket execution, the logging instruction from the agent definition
   may have scrolled out of effective context or been deprioritized
   relative to implementation work.
2. **No enforcement** -- the verify.py e2e checker (`_check_dispatch_logs`)
   only checks that *some* log files exist and are non-empty. It does not
   verify that sub-dispatch logs exist. So the e2e test passes even with
   the gap.
3. **Log routing for planner sub-dispatches** -- `dispatch_log.py` routes
   sprint-level dispatches (no ticket_id) to `sprint-planner-NNN.md`
   regardless of the child agent. Sprint-planner's sub-dispatches to
   architect, architecture-reviewer, and technical-lead would all get
   the same prefix, making them indistinguishable from team-lead's
   dispatch to the sprint-planner itself.

## Proposed Solution

### 1. Strengthen the e2e verification

Update `tests/e2e/verify.py` `_check_dispatch_logs` to assert:

- For each sprint, at least one `ticket-*` log file exists (proving
  sprint-executor logged code-monkey dispatches).
- For each sprint, more than 2 `sprint-planner-*` or child-agent-named
  log files exist (proving sprint-planner logged its sub-dispatches).

This turns the gap from invisible to a test failure.

### 2. Fix log routing for planner sub-dispatches

Update `dispatch_log.py` `log_dispatch` routing so that when
`sprint_name` is set and `ticket_id` is not, the filename prefix uses
the child agent name instead of hardcoding `sprint-planner`. For
example:

- team-lead -> sprint-planner: `sprint-planner-001.md`
- sprint-planner -> architect: `architect-001.md`
- sprint-planner -> architecture-reviewer: `architecture-reviewer-001.md`
- sprint-planner -> technical-lead: `technical-lead-001.md`

This is a one-line change: replace `prefix = "sprint-planner"` with
`prefix = child`.

### 3. Consider programmatic enforcement

If agent-definition-level instructions continue to be ignored, consider
making `log_subagent_dispatch` a required step in the dispatch skill
itself, or adding a wrapper that automatically logs before and after
any Task/subagent invocation.

## Files Involved

```
tests/e2e/verify.py                                          (strengthen checks)
claude_agent_skills/dispatch_log.py                          (fix prefix routing)
claude_agent_skills/agents/domain-controllers/sprint-executor/agent.md  (already has instructions)
claude_agent_skills/agents/domain-controllers/sprint-planner/agent.md   (already has instructions)
tests/e2e/project/docs/clasi/log/                            (evidence of the gap)
```

## Related

- `docs/clasi/todo/done/subagent-dispatch-logging-at-all-levels.md` --
  the previous TODO that added logging instructions to agent definitions
  (sprint 024, ticket 009). This TODO addresses the fact that those
  instructions are not being followed.
- `docs/clasi/todo/append-subagent-response-to-dispatch-log.md` --
  related TODO about logging the subagent response text (not just the
  dispatch prompt).
