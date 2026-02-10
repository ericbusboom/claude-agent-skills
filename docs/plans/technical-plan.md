---
status: draft
---

# Technical Plan

## Architecture Overview

A single Python package (`claude-agent-skills`) containing:

```
claude-agent-skills/
├── agents/              # Agent definitions (shared)
├── skills/              # Skill definitions (shared)
├── instructions/        # SE process & testing instructions (shared)
├── docs/plans/          # SE artifacts for THIS project (not shared)
├── claude_agent_skills/ # Python package with linking script
│   ├── __init__.py
│   └── link_agents.py
└── pyproject.toml       # Package metadata & entry point
```

The CLI command `link-claude-agents` is the sole entry point. It reads source
directories from the installed package location and creates symlinks in a
target repository.

## Technology Stack

- Python 3.7+
- setuptools (build system)
- No runtime dependencies beyond the standard library

## Component Design

### Component: Linking Script (`link_agents.py`)

**Purpose**: Create symlinks from a target repo to the shared definitions in
this repo.

**Use Cases Addressed**: UC-001, UC-002, UC-003, UC-004

**Key Functions**:
- `get_repo_root()` — Locates the source repo via `__file__`
- `link_directory()` — Creates a directory symlink, replacing stale links
- `link_file()` — Creates a file symlink, replacing stale links
- `link_claude_skills()` — Handles Claude's `<name>/SKILL.md` structure
- `link_agents_and_skills()` — Orchestrates all linking for both tools

**Target Layout per Tool**:

| Source | Copilot Target | Claude Code Target |
|--------|---------------|-------------------|
| `agents/` | `.github/copilot/agents/` (dir symlink) | `.claude/agents/` (dir symlink) |
| `skills/` | `.github/copilot/skills/` (dir symlink) | `.claude/skills/<name>/SKILL.md` (file symlinks) |
| `instructions/` | `.github/copilot/instructions/` (dir symlink) | `.claude/rules/` (dir symlink) |

### Component: Agent Definitions (`agents/`)

Markdown files with YAML frontmatter (`name`, `description`, `tools`).
Identical format works for both Copilot and Claude Code agents.

### Component: Skill Definitions (`skills/`)

Markdown files with YAML frontmatter (`name`, `description`). For Copilot,
linked as-is. For Claude Code, each file is symlinked as
`<skill-name>/SKILL.md` to match Claude's expected structure.

### Component: Instructions (`instructions/`)

Markdown files with YAML frontmatter (`name`, `description`). Linked as
`.claude/rules/` for Claude Code and `.github/copilot/instructions/` for
Copilot. Both tools auto-discover markdown files in these directories.

## Deployment Strategy

Installed via pip or pipx:

```bash
# Development (editable)
pip install -e .

# Or via pipx for isolated install
pipx install .
```

The `link-claude-agents` command is registered as a console script entry
point in `pyproject.toml`.

## Open Questions

- Should the script also update target `.gitignore` to exclude symlinked
  directories?
- Should there be an `unlink` command to remove symlinks?
