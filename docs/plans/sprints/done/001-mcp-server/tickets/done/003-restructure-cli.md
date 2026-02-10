---
id: "003"
title: Restructure CLI and pyproject.toml
status: done
use-cases: [SUC-001]
depends-on: []
---

# Restructure CLI and pyproject.toml

Create `claude_agent_skills/cli.py` with click-based subcommand structure.
Update pyproject.toml for the new entry point, dependencies, and Python
version.

## Description

Replace the current argparse-based `link_agents.py:main` entry point with
a click-based CLI registered as `clasi`. The CLI has subcommands: `init`
and `mcp`. This ticket sets up the CLI skeleton — the actual init and mcp
implementations come in later tickets.

## Acceptance Criteria

- [ ] `claude_agent_skills/cli.py` exists with a click group and stub
      subcommands (`init`, `mcp`)
- [ ] pyproject.toml entry point changed to `clasi = "claude_agent_skills.cli:cli"`
- [ ] Old `link-claude-agents` entry point removed
- [ ] Dependencies added: `mcp`, `pyyaml`, `click`
- [ ] `requires-python` bumped to `>=3.10`
- [ ] `pip install -e .` succeeds and `clasi --help` shows both subcommands
- [ ] `clasi init --help` shows `--global` flag and optional target argument
- [ ] `clasi mcp --help` works (stub that prints "not implemented yet")
