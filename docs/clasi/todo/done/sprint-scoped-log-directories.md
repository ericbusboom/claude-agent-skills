---
status: done
sprint: '002'
tickets:
- '003'
---

# Sprint-Scoped Log Directories

Logging stopped using sprint directories. The logs associated with a sprint are supposed to go into a subdirectory for the sprint, not a flat `docs/clasi/log/` directory. Fix the subagent and task hook handlers to write logs into the active sprint's directory structure.
