# Sprint Review Gates

The sprint planning process has review gates (architecture review, stakeholder
approval) that are easily skipped by AI agents. When an agent is asked to "plan
a sprint," it tends to generate all artifacts (brief, use cases, technical plan,
tickets) in a single batch, bypassing the gates entirely.

Problems to fix:

1. **No "Definition of Ready" checklist for sprints**: Tickets have a Definition
   of Done with checkboxes, but there is no equivalent "Definition of Ready"
   checklist that must be satisfied before tickets can be created. Add one to
   the system-engineering instructions and the plan-sprint skill.

2. **Sprint status is too coarse**: The `status` field has `planning | active |
   done` but "planning" covers everything from "just created directory" to
   "tickets created and ready to execute." Consider finer-grained status values
   or a checklist in the sprint frontmatter (e.g., `architecture_review: pending`,
   `stakeholder_approval: pending`).

3. **The `create_sprint` tool doesn't enforce the lifecycle**: It creates the
   full directory structure and all template files in one call. Consider splitting
   this into phases, or at minimum having the tool NOT create tickets — tickets
   should only be created after the review gate passes.

4. **Instructions are narrative, not checklist-gated**: The sprint lifecycle is
   a numbered list, but there is no hard gate. Convert the critical steps into
   explicit checklists with checkboxes in the sprint.md template, similar to how
   ticket acceptance criteria work.

5. **The plan-sprint skill should explicitly require pausing for human input**
   at the review gate. The skill description says "wait for approval" but should
   emphasize that generating tickets before approval is a process violation.
