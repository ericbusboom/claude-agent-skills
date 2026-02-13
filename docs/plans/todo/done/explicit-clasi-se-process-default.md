---
status: done
sprint: '011'
tickets:
- '001'
---

# Make CLASI SE process rules more explicit as the default

Update `.claude/rules/clasi-se-process.md` to state very directly that the
CLASI SE process is the **default process for all requests to implement code
changes**. The agent should always follow this process unless the human
explicitly opts out using phrases like:

- "out of process"
- "direct"
- "just do it" (in the context of skipping process, not auto-approve)
- Or similar language indicating the change should bypass the SE process

This removes any ambiguity about when to use the process.
