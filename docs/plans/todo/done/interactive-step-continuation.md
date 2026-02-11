---
status: done
sprint: 008
---
# Interactive Step Continuation UI

When one process step completes (e.g., a ticket is done, a gate passes, a
sprint closes), present an `AskUserQuestion` UI with options like:

- "Continue to next step" (default/recommended)
- "Other" (free text for redirection)

This prevents the agent from barreling through the entire process without
giving the stakeholder a chance to intervene, redirect, or pause. The
`/next` skill use this pattern at
natural breakpoints.

Note that this is only going to be used in the between the initial project scope
and the first sprint and within the sprint from the sprint definition phase to
approval and architectural review, you're not going to use this between tickets.
Once the tickets are approved, then you just keep going. You don't check between
tickets.  You will ask before you start executing tickets, but not between
tickets. 

