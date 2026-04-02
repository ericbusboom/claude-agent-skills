---
status: done
sprint: '002'
tickets:
- '001'
---

# Implement Task Lifecycle Hooks

The TaskCreated and TaskCompleted handlers in `clasi/hook_handlers.py` are stubs (`sys.exit(0)` with TODO comments). Implement them to log programmer task lifecycle the same way SubagentStart/SubagentStop log sprint-planner activity — create log files in `docs/clasi/log/` with frontmatter, prompt, result, and transcript.

Also need to register `TaskStart` hook in settings.json (currently only `TaskCompleted` is registered, and it's a no-op).
