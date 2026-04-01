---
status: done
sprint: '012'
tickets:
- '004'
---

# Add .gitignore entries for files installed by `clasi init`

`clasi init` installs several files into the target project (`.claude/`,
`.github/copilot/instructions/`, `.mcp.json`, etc.). These are generated
config files that shouldn't be committed to the target project's repo.

`clasi init` should append appropriate `.gitignore` entries so these
installed files are excluded from version control by default.
