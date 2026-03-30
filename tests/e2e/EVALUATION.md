# E2E Test Evaluation Guide

## What You're Checking

The e2e test proves that the full dispatch chain works: team-lead
dispatches to planners and executors, executors dispatch to code-monkey,
and every dispatch produces a log entry. If any level does the work
itself instead of dispatching, the test has failed — even if the code
output looks correct.

## Three Sources of Truth

You must cross-check these three at every checkpoint:

### 1. MCP Server Log (`docs/clasi/log/mcp-server.log`)

Every significant action goes through an MCP tool call. You should see:

- `CALL get_version` and `CALL get_se_overview` at startup
- `CALL dispatch_to_requirements_narrator` (once)
- `CALL dispatch_to_sprint_planner` (once per sprint, mode=detail)
- `CALL dispatch_to_sprint_executor` (once per sprint)
- `CALL dispatch_to_code_monkey` (**once per ticket** — this is critical)
- `CALL create_sprint`, `advance_sprint_phase`, `create_ticket`,
  `move_ticket_to_done`, `close_sprint` (lifecycle tools)

Every CALL must have a matching OK or FAIL line.

### 2. Dispatch Log Directory (`docs/clasi/log/`)

Every dispatch_to_* call produces a markdown file:

```
docs/clasi/log/
├── adhoc/
│   └── 001.md              # requirements-narrator dispatch
└── sprints/
    ├── 001-project-.../
    │   ├── sprint-planner-001.md
    │   ├── sprint-executor-001.md
    │   └── code-monkey-001.md   # <-- MUST EXIST for each ticket
    ├── 002-.../
    │   ├── sprint-planner-001.md
    │   ├── sprint-executor-001.md
    │   └── code-monkey-001.md
    ...
```

**If sprint-executor-001.md exists but code-monkey-001.md does not,
the executor bypassed dispatch.**

### 3. Project Code Directory

New `.py` files appear as tickets are executed:

```
guessing_game/
├── __init__.py
├── __main__.py
├── number_game.py
├── color_game.py
└── city_game.py
tests/
├── test_main.py
├── test_number_game.py
├── test_color_game.py
└── test_city_game.py
```

**Every new .py file MUST have a corresponding dispatch_to_code_monkey
in the MCP log.** If you see a new file but no dispatch, the executor
is writing code directly.

## Checkpoint Procedure (every 60-90 seconds)

Run this check:

```bash
cd tests/e2e/project

# 1. Count dispatch calls by type
echo "=== DISPATCHES ==="
grep "CALL dispatch" docs/clasi/log/mcp-server.log | \
  sed 's/.*CALL //' | sed 's/(.*//' | sort | uniq -c

# 2. Count dispatch log files
echo "=== DISPATCH LOGS ==="
find docs/clasi/log -name "*.md" | sort

# 3. Count code files
echo "=== CODE FILES ==="
find . -name "*.py" -not -path "./.claude/*" -not -path "./docs/*" \
  -not -path "*__pycache__*" -not -path "./.venv/*"

# 4. Check for code-monkey dispatches
echo "=== CODE MONKEY DISPATCHES ==="
grep "dispatch_to_code_monkey" docs/clasi/log/mcp-server.log | wc -l
```

## Failure Conditions — STOP IMMEDIATELY

1. **Code files exist but no dispatch_to_code_monkey calls.**
   The executor is writing code directly. Kill the test.

2. **dispatch_to_sprint_executor returned OK but no code-monkey
   dispatch log exists.** The executor did the work itself. Kill.

3. **MCP server log shows zero tool calls after startup.** The agent
   isn't connected to the MCP server. Kill.

4. **dispatch_to_* calls return error repeatedly (>2 consecutive).**
   The dispatch infrastructure is broken. Kill and diagnose.

5. **Sprint closed but tickets not in done/.** State is inconsistent.
   Report but don't necessarily kill — close_sprint may self-repair.

## Success Criteria

The test passes when ALL of these are true:

- [ ] 4 sprints in `docs/clasi/sprints/done/`
- [ ] All tickets in `tickets/done/` with status: done
- [ ] MCP log shows dispatch_to_code_monkey for every ticket
- [ ] Dispatch log files exist for every dispatch (planner, executor,
      code-monkey per sprint)
- [ ] `pytest` passes in the project directory
- [ ] No code files exist without a corresponding code-monkey dispatch
- [ ] dispatch_to_sprint_planner results are `valid` (contract passes)
- [ ] dispatch_to_sprint_executor results are `valid` (contract passes)
- [ ] dispatch_to_code_monkey results are `valid` (contract passes)

## What "valid" vs "invalid" vs "error" Means

- **valid** — subagent returned JSON matching the contract schema, and
  output files exist with correct frontmatter. This is the goal.
- **invalid** — subagent did the work but returned JSON that doesn't
  match the contract. The work happened but the contract needs tuning.
- **error** — the dispatch itself failed (query() crashed, SDK error,
  etc.). The work did NOT happen through dispatch.
