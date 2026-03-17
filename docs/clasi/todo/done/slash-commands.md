# Slash Commands for Common Actions

Add slash commands (Claude Code skills) that map to common SE process
actions. The goal is quick, low-friction interaction — the user types a
short command and the AI knows what to do.

## Initial commands

- `/todo <text>` — Capture the rest of the message as a new TODO file in
  `docs/plans/todo/`. The AI should create the file, pick a reasonable
  filename from the content, and confirm.
- `/next` — Execute the next step of whatever process is active. The AI
  determines the current state (sprint phase, next ticket, etc.) and
  proceeds without the user having to spell it out.

## Discussion needed

Before implementing, we should discuss what other slash commands would be
useful. Some candidates to consider:

- `/status` — Run project-status skill, report where things stand
- `/review` — Trigger code review on current changes
- `/plan` — Start planning the next sprint
- `/close` — Close the current sprint
- `/split` — Run todo-split on the TODO directory

The implementation would use Claude Code's skill system (`.claude/skills/`
files) so they show up as real slash commands in the CLI.
