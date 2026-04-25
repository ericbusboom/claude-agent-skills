---
status: pending
---

# Add Codex Support to CLASI Init and Plan Capture

Add opt-in Codex support to CLASI so `clasi init --codex` configures Codex
alongside the existing Claude setup.

## Summary

CLASI currently initializes Claude-oriented project files: `CLAUDE.md`,
`.claude/`, MCP configuration, hooks, skills, and TODO directories. Extend
initialization so Codex can use the same CLASI process without changing the
default Claude behavior.

Per CLASI's planning flow, discussed plans should become pending TODOs in
`docs/clasi/todo/` and then stop. Claude already does this through the
`ExitPlanMode` plan-to-todo hook. Codex support should add equivalent capture
for accepted `<proposed_plan>` output.

## Key Changes

- Keep `CLAUDE.md` and `.claude/` as Claude-specific install targets.
- Add a marker-managed CLASI section to `AGENTS.md` for Codex.
- Add `.codex/config.toml` with `[mcp_servers.clasi]` using the existing
  detected MCP command, plus `codex_hooks = true`.
- Install Codex-readable CLASI skills under `.agents/skills/`, sourced from
  the same bundled plugin content.
- Add `.codex/hooks.json` with a `Stop` hook calling
  `clasi hook codex-plan-to-todo`.
- Extend plan-to-todo logic so the Codex hook extracts
  `<proposed_plan>...</proposed_plan>` from `last_assistant_message`, writes a
  pending TODO, de-dupes by content hash, and stops without implementation.

## Interfaces

- CLI: add `clasi init --claude [target]`, `clasi init --codex [target]`,
  and allow `clasi init --claude --codex [target]`.
- CLI: add `clasi uninstall --claude [target]`,
  `clasi uninstall --codex [target]`, and allow
  `clasi uninstall --claude --codex [target]`.
- Preserve backward compatibility: when neither platform flag is supplied in a
  non-interactive context, keep the current Claude install behavior.
- In an interactive context where neither platform flag is supplied, inspect
  advisory platform signals and prompt the user to choose Claude, Codex, or
  both.
- In an interactive `clasi uninstall` call where neither platform flag is
  supplied, inspect installed CLASI-managed platform files and prompt the user
  to remove Claude, Codex, or both.
- Hooks: add `clasi hook codex-plan-to-todo`.
- Dependencies: add Python 3.10-compatible TOML read/write support, such as
  `tomli` for Python versions before 3.11 and `tomli-w`.
- TODO frontmatter remains compatible, with optional `source: codex-plan` and
  `source_hash`.

## Uninstall Behavior

`clasi uninstall` should remove only CLASI-managed platform integration files
or marker-managed sections. It must not delete unrelated user content.

- Claude uninstall removes the CLASI section from `CLAUDE.md`, CLASI-managed
  `.claude/skills/`, `.claude/agents/`, `.claude/rules/`, `.claude/settings.json`
  hooks, and `.claude/settings.local.json` MCP permission entries when they are
  still CLASI-owned.
- Codex uninstall removes the CLASI section from `AGENTS.md`, CLASI-managed
  `.agents/skills/`, `.codex/hooks.json` entries, and `.codex/config.toml`
  `clasi` MCP server / hook feature settings when they are still CLASI-owned.
- Shared project artifacts such as `docs/clasi/todo/`, sprint history, logs,
  and existing `.mcp.json` should not be removed by default.
- If a file contains both CLASI-managed and user-managed content, remove only
  the marker-managed CLASI block or CLASI-specific entry.

## Platform Detection

Use detection only to recommend a default, not to silently make irreversible
decisions. Safe signals include:

- Project files: `.claude/`, `CLAUDE.md`, `.codex/`, `.agents/skills/`,
  `AGENTS.md`.
- Installed commands: `claude`, `codex`.
- User config directories: `~/.claude`, `~/.codex`.
- Environment variable names only: `ANTHROPIC_API_KEY`, `CLAUDE_*`,
  `OPENAI_API_KEY`, `CODEX_*`.

If both platforms are detected, present both and recommend the platform already
configured in the project; if neither is project-configured but both user
platforms are present, recommend both. Do not read or print secret values, and
do not run interactive login checks.

## Acceptance Criteria

- [ ] Default `clasi init` behavior remains unchanged for Claude.
- [ ] `clasi init --claude` explicitly installs the existing Claude project
      setup.
- [ ] If neither `--claude` nor `--codex` is supplied interactively, CLASI
      presents Claude, Codex, and both as choices with a detected recommendation.
- [ ] If neither platform flag is supplied non-interactively, CLASI preserves
      the current Claude-only default.
- [ ] `clasi init --codex` creates or updates `AGENTS.md`,
      `.codex/config.toml`, `.codex/hooks.json`, and
      `.agents/skills/se/SKILL.md`.
- [ ] `clasi init --claude --codex` installs both platform integrations in one
      run.
- [ ] `clasi uninstall --claude`, `clasi uninstall --codex`, and
      `clasi uninstall --claude --codex` remove only the selected
      CLASI-managed platform integration files or sections.
- [ ] Interactive `clasi uninstall` presents Claude, Codex, and both as choices
      based on detected installed CLASI platform integrations.
- [ ] `clasi uninstall` preserves TODOs, sprint artifacts, logs, unrelated
      `.claude/`, `.codex/`, `.agents/`, `CLAUDE.md`, and `AGENTS.md` content.
- [ ] Re-running `clasi init --codex` is idempotent and preserves unrelated
      config.
- [ ] Codex plan capture writes one pending TODO under `docs/clasi/todo/`.
- [ ] Duplicate plan capture is avoided by content hash.
- [ ] Existing Claude `ExitPlanMode` plan-to-todo behavior still passes.

## Test Plan

- [ ] Add or update tests proving default `clasi init` still does not create
      `.codex` or `.agents`.
- [ ] Add tests for explicit `--claude`, explicit `--codex`, and combined
      `--claude --codex` CLI behavior.
- [ ] Add tests for `clasi uninstall` platform selection, idempotency, and
      preservation of user-owned files/content.
- [ ] Add tests for platform detection recommendations using temporary project
      files, mocked command lookup, mocked home config directories, and
      environment variable names without values.
- [ ] Add tests for Codex init output files and idempotency.
- [ ] Add tests for the Codex Stop hook: no-op without a proposed plan,
      create one TODO with a proposed plan, and avoid duplicate TODOs.
- [ ] Run
      `uv run pytest tests/unit/test_init_command.py tests/unit/test_hook_handlers.py tests/unit/test_plan_to_todo.py -v`.

## Assumptions

- Scope is local Codex CLI and IDE support for instructions, MCP, skills,
  hooks, and plan capture.
- Replacing the Claude Agent SDK dispatch backend is out of scope and should
  become a separate TODO if needed.
- Codex project guidance should use `AGENTS.md`, not `@CLAUDE.md`
  indirection.
