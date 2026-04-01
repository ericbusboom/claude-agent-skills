---
id: '012'
title: Multi-Platform and Cleanup
status: done
branch: sprint/012-multi-platform-and-cleanup
use-cases: []
---

# Sprint 012: Multi-Platform and Cleanup

## Goals

Extend `clasi init` to support multiple AI agent platforms and clean up
the init workflow.

## Problem

`clasi init` currently targets Claude Code only (`.claude/` directory)
with a partial Copilot mirror. Other platforms (ChatGPT Codex, generic
agent frameworks) are unsupported. Additionally, installed files lack
`.gitignore` entries, so they get committed to target repos unintentionally.

## Solution

1. Generate an `AGENTS.md` with a high-level SE process overview that
   any agent platform can read.
2. Replace the `.github/copilot/instructions/` mirror with `AGENTS.md`.
3. Symlink `.claude` to `.codex` for ChatGPT Codex support.
4. Append `.gitignore` entries for all installed files.

## Queued TODOs

- `docs/plans/todo/multi-agent-platform-support-in-clasi-init.md` —
  AGENTS.md, .codex symlink, remove copilot mirror
- `docs/plans/todo/add-gitignore-entries-for-clasi-init-files.md` —
  Add .gitignore entries for files installed by `clasi init`
