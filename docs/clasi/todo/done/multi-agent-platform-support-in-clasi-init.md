---
status: done
sprint: '012'
tickets:
- '001'
- '002'
- '003'
---

# Multi-agent platform support in `clasi init`

Extend `clasi init` to support multiple AI coding agent platforms beyond
Claude Code:

1. **AGENTS.md**: Install a top-level `AGENTS.md` file containing the
   high-level project instructions (the content that currently goes into
   `.claude/rules/`). This is the standard location for agent instructions
   recognized by several platforms.

2. **Remove `.github/copilot/instructions/`**: Instead of copying rule
   files into `.github/copilot/instructions/`, rely on `AGENTS.md` for
   Copilot instruction delivery.

3. **ChatGPT Codex (`.codex`)**: Symlink `.claude` to `.codex` so that
   ChatGPT Codex picks up the same skills, rules, and settings without
   file duplication.


The agents.md file should have a relatively detailed rundown of what the software engineering process is, including what are the major steps and what the agent should do in certain circumstances. I think you want to say:
- If you're starting a project, do <this>.
- If you are opening a sprint, do <this>.
- If you are working on a ticket, do <this>.

You don't need to provide all the details of how those steps go, of course,
because you're going to refer them to the actual skill agent or rule. You want
to put all the stuff right up front so that if the agent has a goal that it
understands that it needs to use the software engineering process to accomplish
that goal and where to go next to get more information about that goal. 

