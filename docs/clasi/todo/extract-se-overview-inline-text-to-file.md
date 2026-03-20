---
status: pending
---

# Extract Inline Process Text from get_se_overview() to a File

**Do not implement yet.**

## Problem

`get_se_overview()` in `claude_agent_skills/process_tools.py` (lines
131-194) contains hardcoded inline text for two sections:

1. **Process Stages** (lines 155-166) -- a numbered list describing the
   five stages of the SE process, which skills and agents map to each.
2. **MCP Tools Quick Reference** (lines 179-194) -- a categorized list
   of all MCP tools and their signatures.

The stakeholder directive is: "get_se_overview() should not have any
inline process overview. All text like this must be removed from the
code and read from a file."

The dynamically generated sections (agent/skill/instruction listings)
are fine -- those are built from frontmatter at runtime. The problem is
the static prose that is baked into the Python source.

## Proposed Solution

Create a content file (e.g., `content/se-overview.md` inside the
package) that contains the full template for the SE overview, with
placeholders for the dynamic sections. The function reads this file at
runtime and interpolates the dynamic content.

Alternatively, split into two files:

- `content/process-stages.md` -- the Process Stages section
- `content/tools-reference.md` -- the MCP Tools Quick Reference section

The function would read these files and assemble the final output,
keeping the dynamic agent/skill/instruction listings generated in code.

## Files to Modify

```
claude_agent_skills/process_tools.py   (remove inline text, load from file)
claude_agent_skills/content/           (new directory for extracted text files)
```

## Open Questions

- Single template file with placeholders, or multiple fragment files?
- Should `get_activity_guide()` (line 374) also be checked for inline
  text that should be externalized, or is that a separate concern?
- Where exactly in the package should the content file(s) live?
  `content/` subdirectory is one option; reusing the existing
  `instructions/` directory is another.
