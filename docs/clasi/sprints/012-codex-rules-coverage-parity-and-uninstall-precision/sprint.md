---
id: "012"
title: "Codex rules-coverage parity and uninstall precision"
status: planning
branch: sprint/012-codex-rules-coverage-parity-and-uninstall-precision
use-cases:
  - SUC-001
  - SUC-002
  - SUC-003
  - SUC-004
  - SUC-005
  - SUC-006
  - SUC-007
  - SUC-008
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 012: Codex rules-coverage parity and uninstall precision

## Goals

1. **Codex rules-coverage parity (Track A)**: The Codex installer currently mirrors
   only a subset of the five Claude path-scoped rules. This sprint brings full parity:
   all five rules appear in the appropriate nested AGENTS.md files, with a second named
   marker block on root AGENTS.md for the two global-scope rules (`mcp-required`,
   `git-commits`). Rule content is extracted into a shared `clasi/platforms/_rules.py`
   module consumed by both the Claude and Codex installers.

2. **Uninstall precision (Track B)**: Both platform uninstallers currently over-delete.
   The Claude uninstaller uses `shutil.rmtree` for skill and agent subdirectories,
   clobbering user-added files. The Codex uninstaller cascades `rmdir` up to `.agents/`,
   which is a cross-tool shared root that CLASI should not remove. This sprint replaces
   both with file-level deletion that mirrors the install set exactly.

## Problem

**Track A**: Sprint 011 ticket 005 installed two nested AGENTS.md files
(`docs/clasi/AGENTS.md`, `clasi/AGENTS.md`) but left three of the five Claude rules
without a Codex equivalent: `mcp-required` is only partially covered (missing from root
scope), `clasi-artifacts` is missing the active-sprint and phase checks, `todo-dir` has
no AGENTS.md at all, and `git-commits` is completely absent. A Codex agent doing git
operations has no knowledge of the git-commits rule; one touching `docs/clasi/todo/`
gets no guidance about using the `todo` skill.

**Track B**: `shutil.rmtree(target_skill)` and `shutil.rmtree(target_agent)` in
`claude.py` uninstall remove entire subdirectories even if the user placed extra files
there. `codex.py` uninstall cascades rmdir up to `.agents/`, removing a shared root
that other tools (Cursor, Gemini, Copilot, Windsurf) may depend on.

## Solution

**Track A**:
- Extract all rule content from `claude.py`'s `RULES` dict into a new
  `clasi/platforms/_rules.py` module. Both `claude.py` and `codex.py` import from it.
- Extend `clasi/platforms/_markers.py` to support a second named marker block
  (e.g. `<!-- CLASI:RULES:START --> ... <!-- CLASI:RULES:END -->`), distinct from the
  existing `<!-- CLASI:START --> ... <!-- CLASI:END -->` block, so both blocks can
  coexist in root AGENTS.md without interfering.
- Write the two global-scope rules (`mcp-required`, `git-commits`) into that second
  marker block on root AGENTS.md via the Codex installer.
- Update `docs/clasi/AGENTS.md` content to the full `clasi-artifacts` rule
  (active-sprint check, phase check, MCP-tools-only) sourced from `_rules.py`.
- Add `docs/clasi/todo/AGENTS.md` for the `todo-dir` rule, sourced from `_rules.py`.
- Keep `clasi/AGENTS.md` (source-code rule) — update to source from `_rules.py`.

**Track B**:
- Replace `shutil.rmtree(target_skill)` in Claude uninstall with per-file deletion
  mirroring the install set (SKILL.md only), followed by leaf rmdir-if-empty.
- Replace `shutil.rmtree(target_agent)` in Claude uninstall with per-file deletion
  of `*.md` files that were copied at install time, followed by leaf rmdir-if-empty.
- Drop the cascading `rmdir` of `.agents/skills/` and `.agents/` in Codex uninstall.
  Per-skill leaf rmdir-if-empty stays.

## Success Criteria

- All 5 Claude rules have a Codex-native equivalent at the correct path scope.
- Root AGENTS.md carries both the CLASI entry-point block and the global-rules block;
  both blocks survive repeated install/uninstall round-trips without interference.
- `docs/clasi/AGENTS.md` contains the full clasi-artifacts rule content.
- `docs/clasi/todo/AGENTS.md` exists with the todo-dir rule content.
- Rule content has a single canonical definition in `_rules.py`.
- `clasi uninstall --claude` preserves user-added files in skill and agent subdirs.
- `clasi uninstall --codex` does not remove `.agents/` or `.agents/skills/`.
- All new behavior is verified by tests (four new Claude tests, two new Codex tests,
  one end-to-end Codex install correctness test).
- Full test suite passes.

## Scope

### In Scope

- `clasi/platforms/_rules.py` — new shared module for rule content
- `clasi/platforms/_markers.py` — second named marker block support
- `clasi/platforms/claude.py` — refactor RULES dict to import from `_rules.py`;
  replace rmtree in uninstall with file-level deletion
- `clasi/platforms/codex.py` — write global-rules block on root AGENTS.md;
  update nested AGENTS.md content from `_rules.py`; add `docs/clasi/todo/AGENTS.md`;
  drop cascading rmdir in uninstall
- `tests/unit/test_init_command.py` — Claude uninstall precision tests
- `tests/unit/test_platform_codex.py` — Codex uninstall precision + end-to-end tests

### Out of Scope

- Translation layer for Claude-specific phrasing in agent TOML `developer_instructions`
  (deferred from sprint 011, still deferred)
- Installing global rules to `~/.codex/hooks.json` (out of scope, noted in sprint 011)
- Cleanup of dead `clasi/plugin/rules/*.md` files (separate cleanup decision)
- Single-source-of-truth for install/uninstall skill+agent paths (manifest module);
  only rule content moves to `_rules.py` this sprint

## Test Strategy

- Unit tests for `_markers.py` named-block support: round-trip both blocks coexisting
  in the same file; verify `strip_named_section` removes only the target block.
- Unit tests for Claude uninstall: install, drop user file, uninstall, assert user file
  survives and CLASI-installed files are gone. Separate tests for skill and agent dirs.
- Unit tests for Codex uninstall: install, drop user file in `.agents/`, uninstall,
  assert `.agents/` and user file survive.
- End-to-end Codex install test: run full `codex.install()`, assert all expected
  AGENTS.md files exist with correct content, assert second marker block present on
  root AGENTS.md.
- Full suite (`pytest --no-cov -q`) must stay green.

## Architecture Notes

See `architecture-update.md` for the full design. Key decisions:
- Named marker blocks via `_markers.py` extension (not a parallel module).
- Rule content centralized in `_rules.py`; each installer renders to its native format.
- No manifest module for skill/agent install paths — symmetry is maintained by both
  sides walking the same `plugin/...` iterator.

## TODO References

- `docs/clasi/todo/codex-install-rules-coverage-gap.md`
- `docs/clasi/todo/plan-make-uninstall-delete-only-what-install-copied-no-whole-directory-deletes.md`

## GitHub Issues

(None yet.)

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan

## Tickets

| # | Title | Depends On | Group |
|---|-------|------------|-------|
| 001 | Extract rule content into shared `_rules.py` module | — | 1 |
| 002 | Extend `_markers.py` with named marker block support | — | 1 |
| 003 | Claude uninstall: replace rmtree for skills with file-level deletion | — | 1 |
| 004 | Claude uninstall: replace rmtree for agents with file-level deletion | — | 1 |
| 005 | Codex uninstall: drop cascading rmdir of `.agents/skills/` and `.agents/` | — | 1 |
| 006 | Codex installer: write global-rules block on root AGENTS.md | 001, 002 | 2 |
| 007 | Codex installer: expand `docs/clasi/AGENTS.md` and add `docs/clasi/todo/AGENTS.md` | 001 | 2 |
| 008 | End-to-end Codex install correctness test | 006, 007 | 3 |

**Groups**: Tickets in the same group can execute in parallel.
Groups execute sequentially (1 before 2, etc.).
