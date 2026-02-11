---
status: draft
---

# Sprint 010 Technical Plan

## Architecture Overview

This sprint adds four independent features: scold detection with self-
reflection, auto-approve mode, multi-ecosystem version detection, and
VSCode MCP configuration. The features are independent and can be
implemented in any order.

## Component Design

### Component: Scold Detection and Self-Reflection

**Use Cases**: SUC-001

Two artifacts:

**1. Always-on instruction** — a CLAUDE.md rule file at
`.claude/rules/scold-detection.md` that tells the agent to watch for
stakeholder corrections and invoke the self-reflection skill when detected.

```markdown
# Scold Detection

When the stakeholder corrects your behavior, produces frustration signals,
or explicitly points out an error in your approach:

1. Acknowledge the correction immediately.
2. Run the **self-reflect** skill to produce a structured reflection.
3. Continue with the corrected approach.

Detection signals:
- Direct correction ("no", "that's wrong", "you shouldn't have")
- Process critique ("why did you do X?", "that's not how it works")
- Frustration ("I told you to...", "you keep doing...")
- Explicit instruction to reflect
```

**2. Self-reflection skill** — `claude_agent_skills/skills/self-reflect.md`:

Process:
1. Capture what action the agent took that was wrong.
2. Identify what the correct action should have been.
3. Analyze root cause (missing instruction, ambiguous skill, ignored rule).
4. Propose a fix (new instruction, skill update, TODO for future sprint).
5. Write reflection to `docs/plans/reflections/YYYY-MM-DD-slug.md` with
   YAML frontmatter (date, sprint, category).
6. If the root cause suggests a process fix, also create a TODO.

### Component: Auto-Approve Mode

**Use Cases**: SUC-002

An always-on instruction at `.claude/rules/auto-approve.md` that defines
the behavior:

```markdown
# Auto-Approve Mode

When the stakeholder says "auto-approve", "run without asking", or similar:

1. Acknowledge that auto-approve is active.
2. At every `AskUserQuestion` breakpoint in a skill, select the first
   (recommended) option automatically.
3. Log each auto-approval: "Auto-approved: [option selected] at [skill step]"
4. Continue until stakeholder says "stop auto-approving" or the session ends.

This is session-scoped — it does NOT persist across conversations.
```

No code changes needed. This is purely an instruction that modifies how
the agent interprets breakpoint steps in skills.

### Component: Multi-Ecosystem Version Detection

**Use Cases**: SUC-003

Refactor `claude_agent_skills/versioning.py`:

**New function** `detect_version_file(project_root: Path) -> tuple[Path, str] | None`:
- Checks for version files in priority order:
  1. `pyproject.toml` → type `"pyproject"`
  2. `package.json` → type `"package_json"`
- Returns `(path, type)` or `None` if no version file found.

**New function** `update_version_file(path: Path, file_type: str, version: str) -> None`:
- Dispatches to the appropriate updater based on `file_type`:
  - `"pyproject"` → existing `update_pyproject_version` logic
  - `"package_json"` → update `"version"` field in JSON

**Modify** `tag_version` MCP tool in `artifact_tools.py`:
- Call `detect_version_file` instead of hardcoding `pyproject.toml`.
- If no version file found, still create git tag (tag-only mode).
- Return the detected file type in the response.

**Tests** (in `tests/unit/test_versioning.py`):
- `test_detect_version_file_pyproject` — finds pyproject.toml
- `test_detect_version_file_package_json` — finds package.json when no
  pyproject.toml
- `test_detect_version_file_priority` — pyproject.toml wins when both exist
- `test_detect_version_file_none` — returns None when neither exists
- `test_update_package_json_version` — updates version field in JSON
- `test_tag_version_tag_only` — creates tag without version file

### Component: VSCode MCP Configuration

**Use Cases**: SUC-004

Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "clasi": {
      "type": "stdio",
      "command": "clasi",
      "args": [
        "mcp"
      ]
    }
  },
  "inputs": []
}
```

Single file creation, no code changes.

## Decisions

No open questions — all four features have clear, independent designs.
