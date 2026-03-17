---
status: done
sprint: '005'
---
# Rename Process and Agent

The process is currently called "Systems Engineering Process" but should be
called **"Software Engineering Process"**. The agent `systems-engineer.md`
should be renamed to **"Technical Lead"** (`technical-lead.md`).

## Changes Needed

- Rename `agents/systems-engineer.md` to `agents/technical-lead.md`
- Update all references from "Systems Engineering" to "Software Engineering"
  throughout instructions, agent definitions, skill definitions, and the
  `init_command.py` instruction content
- Update the `get_se_overview` tool output (SE acronym still works for
  "Software Engineering")
- Update any CLASI description text (the "S" in CLASI stands for "Skills"
  not "Systems", so no change needed there)
- Grep for "systems engineer" / "Systems Engineering" across the codebase
  and update consistently


When you rename agents, make sure that you update any instructions or skills that refer to those agents. 