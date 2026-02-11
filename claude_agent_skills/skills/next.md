---
name: next
description: Determine the next process step and execute it
---

# Next Step Skill

This skill determines what needs to happen next in the SE process
and begins executing it.

## Process

1. Run the **project-status** skill to understand current state.
2. Based on the current stage, determine the next action:
   - No brief → Start requirements elicitation
   - Brief but no use cases → Continue requirements
   - Use cases but no technical plan → Start architecture
   - Technical plan, no sprint → Plan a sprint
   - Active sprint with todo tickets → Execute next ticket
   - All tickets done → Close the sprint
3. **Breakpoint check** — before executing the action, check whether a
   stakeholder confirmation is needed:

   a. **Before sprint planning**: If the action is "Plan a sprint"
      (technical plan exists, no active sprint), present an
      `AskUserQuestion`:
      - "Plan a new sprint" (recommended)
      - "Review project status first"

      If the stakeholder chooses to review, present the status report
      and stop. Otherwise proceed to sprint planning.

   b. **Before first ticket execution**: If the action is "Execute next
      ticket" AND no tickets are in-progress or done yet (all are todo —
      this is the first ticket of the sprint), present an
      `AskUserQuestion`:
      - "Start executing tickets" (recommended)
      - "Review tickets first"

      If the stakeholder chooses to review, list the tickets and stop.
      Otherwise proceed to execute the first ticket.

   c. **All other cases**: Proceed without asking. This includes:
      - Mid-execution (some tickets already in-progress or done)
      - Sprint closing
      - Requirements and architecture stages

   **IMPORTANT**: Do NOT add breakpoints between individual tickets.
   Once ticket execution has started (at least one ticket is in-progress
   or done), continue executing tickets without interruption until all
   are done.

4. Execute the determined action using the appropriate skill and agent.

## Output

Announce what was determined as the next step, then begin execution.
