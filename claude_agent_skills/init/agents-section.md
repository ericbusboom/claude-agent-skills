<!-- CLASI:START -->
## CLASI Software Engineering Process

This project uses the **CLASI** (Claude Agent Skills Instructions)
software engineering process, managed via an MCP server.

**The SE process is the default.** When asked to build a feature, fix a
bug, or make any code change, follow this process unless the stakeholder
explicitly says "out of process" or "direct change".

### Process

Work flows through four stages organized into sprints:

1. **Requirements** — Elicit requirements, produce overview and use cases
2. **Architecture** — Produce technical plan
3. **Ticketing** — Break plan into actionable tickets
4. **Implementation** — Execute tickets

Use `/se` or call `get_se_overview()` for full process details and MCP
tool reference.

### MANDATORY: Ticket and Sprint Completion

**Agents MUST complete these steps. No exceptions. No skipping.**

Agents have repeatedly failed to move tickets to done and close sprint
branches. This creates inconsistent state. These rules are non-negotiable.

**After finishing a ticket's code changes, you MUST:**

1. Set ticket `status` to `done` in YAML frontmatter.
2. Check off all acceptance criteria (`- [x]`).
3. Move the ticket file to `tickets/done/` — use `move_ticket_to_done`.
4. Move the ticket plan file to `tickets/done/` if it exists.
5. Commit the moves: `chore: move ticket #NNN to done`.

**Finishing the code is NOT finishing the ticket.** The ticket is not done
until the file is in `tickets/done/` and committed.

**After finishing all tickets in a sprint, you MUST close the sprint:**

1. Merge the sprint branch into main.
2. Call `close_sprint` MCP tool (archives directory, releases lock).
3. Commit the archive.
4. Push tags (`git push --tags`).
5. Delete the sprint branch (`git branch -d sprint/NNN-slug`).

**Never merge a sprint branch without archiving the sprint directory.**
**Never leave a sprint branch dangling after the sprint is closed.**

### Stakeholder Corrections

When the stakeholder corrects your behavior or expresses frustration
("that's wrong", "why did you do X?", "I told you to..."):

1. Acknowledge the correction immediately.
2. Run `get_skill_definition("self-reflect")` to produce a structured
   reflection in `docs/plans/reflections/`.
3. Continue with the corrected approach.

Do NOT trigger on simple clarifications, new instructions, or questions
about your reasoning.
<!-- CLASI:END -->
