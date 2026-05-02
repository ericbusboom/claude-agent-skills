---
id: '014'
title: "clasr renderer \u2014 frontmatter engine, named marker blocks, manifests,\
  \ three-platform install"
status: done
branch: sprint/014-clasr-renderer-frontmatter-engine-named-marker-blocks-manifests-three-platform-install
use-cases:
- SUC-001
- SUC-002
- SUC-003
- SUC-004
- SUC-005
- SUC-006
- SUC-007
- SUC-008
- SUC-009
- SUC-010
todo:
- clasr-standalone-cross-platform-agent-config-renderer.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 014: clasr renderer — frontmatter engine, named marker blocks, manifests, three-platform install

## Goals

Build a new `clasr` CLI as a sub-tool inside the existing `clasi` package. `clasr` renders
a source `asr/` directory into per-platform agent-config installs for Claude Code, Codex,
and GitHub Copilot. It implements named provider-scoped marker blocks, per-platform
per-provider manifests, union frontmatter projection, and symlink-with-copy-fallback
install semantics.

`clasi/platforms/` code is NOT modified. All existing CLASI tests keep passing.

## Problem

`clasi init` currently hard-codes CLASI's own plugin content into platform installers.
There is no generic mechanism for other tools to render their own `asr/` source directories
into agent-config installs. As CLASI's agent-config approach matures (and tools like
`curik` emerge as consumers), a reusable renderer layer is needed that:
- Supports multiple providers installing into the same platform directory without collision
- Projects union frontmatter to per-platform target format
- Records what it installed (manifests) for clean, scoped uninstall
- Handles Windows symlink limitations gracefully

## Solution

New top-level Python package `clasr/` alongside `clasi/` in the same repo. Single
`pyproject.toml`; second `console_scripts` entry. Core infrastructure modules (`links.py`,
`markers.py`, `frontmatter.py`, `manifest.py`) implement the primitives. Three platform
modules (`platforms/claude.py`, `platforms/codex.py`, `platforms/copilot.py`) implement
the per-platform install logic using only those primitives. `cli.py` wires everything
together. `clasr` has a strict one-way dependency: it never imports from `clasi`.

## Success Criteria

- `pip install -e .` produces working `clasr` CLI alongside `clasi` CLI
- `clasr install --source <asr> --provider test --claude --codex --copilot` against a
  fixture `asr/` directory produces correct files in all three platform directories
- Named marker blocks from two different providers coexist in the same AGENTS.md
- `clasr uninstall --provider test --claude` removes only that provider's entries
- All three per-platform manifests exist and are valid JSON
- `clasr --instructions` prints the bundled instructions.md
- All existing CLASI tests continue to pass
- Test coverage: unit, per-platform, three-platform roundtrip, multi-tenant

## Scope

### In Scope

- New `clasr/` package with modules: `links.py`, `markers.py`, `frontmatter.py`,
  `manifest.py`, `merge.py`, `cli.py`, `platforms/claude.py`, `platforms/codex.py`,
  `platforms/copilot.py`, `platforms/detect.py`
- Markdown data files shipped via `importlib.resources`: `instructions.md`, `SCHEMA.md`, `README.md`
- Source `asr/` layout: `AGENTS.md`, `skills/<n>/SKILL.md`, `agents/<n>.md`,
  `rules/<n>.md`, per-platform passthrough subdirs `claude/`, `codex/`, `copilot/`
- AGENTS.md and CLAUDE.md both get the same named marker block (not a symlink)
- Skills: always symlink with `--copy` / OSError fallback
- Agents and rules: render frontmatter (union → per-platform); body verbatim
- Per-platform subdirs: tree-copy straight through, no transform
- Per-platform per-provider manifests: `.claude/.clasr-manifest/<provider>.json` etc.,
  atomic writes via `.tmp` then `os.replace`
- `clasr --instructions` prints bundled instructions.md via importlib.resources
- `pyproject.toml` changes: second entry point, include `clasr*` packages, update coverage
- Tests: `tests/clasr/` directory with unit, platform, roundtrip, and multi-tenant tests

### Out of Scope

- Migrating `clasi/platforms/` to use clasr (CLASI existing code untouched)
- Splitting clasr into a separate PyPI distribution
- Cursor / Gemini / Windsurf / Aider / Zed platform support
- Converting `clasi/platforms/_rules.py` Python constants into `asr/` files

## Test Strategy

- **Unit tests** (`tests/clasr/`): `test_links.py`, `test_markers.py`,
  `test_frontmatter.py`, `test_manifest.py`, `test_merge.py` — cover edge cases in each
  infrastructure module independently with tmp directories
- **Platform tests**: `test_platform_claude.py`, `test_platform_codex.py`,
  `test_platform_copilot.py` — each covers install + uninstall + manifest verification
  against a fixture `asr/`
- **Three-platform roundtrip** (`test_three_platform_roundtrip.py`): install all three
  from a single fixture `asr/`, verify outputs and manifests, uninstall one platform,
  verify the other two are intact
- **Multi-tenant** (`test_multi_tenant.py`): two providers (`provider_a`, `provider_b`)
  install into the same target tmp dir; assert both manifests coexist and both marker
  blocks coexist; assert JSON passthrough files deep-merge (both providers' keys present);
  uninstall one; assert the other's files, blocks, and JSON keys survive; assert file
  is deleted when the last provider uninstalls
- **Source-dir immutability**: tests assert `asr/` is byte-identical before and after install

## Architecture Notes

See `architecture-update.md` for the full design. Key decisions:

- `clasr` uses a fresh `links.py` (Option B — independent copy of `_links.py` logic).
  `_markers.py` lift is infeasible because the marker format differs (`BEGIN/END` vs
  `START/END`) and `_markers.py` imports from `clasi.templates`. Two independent
  implementations; a follow-up TODO will converge them.
- Named marker format: `<!-- BEGIN clasr:<provider> -->` / `<!-- END clasr:<provider> -->`
  (distinct from CLASI's `<!-- CLASI:{name}:START -->` format)
- One-way dependency: `clasr` MUST NOT import from `clasi`
- Manifests live inside the platform directory they describe (multi-tenant by design)
- **Copilot marker block target (Q1):** `.github/copilot-instructions.md` ONLY —
  no write to root `AGENTS.md` for the Copilot platform.
- **Multi-provider JSON passthrough (Q2):** JSON-merge via new `clasr/merge.py`; manifest
  uses `kind: "json-merged"` with `"keys"` list for per-provider uninstall. Non-JSON
  passthrough collisions are errors.
- **Codex unscoped rules (Q3):** Rules with no `applyTo`/`paths` frontmatter are injected
  into the root `AGENTS.md` marker block content.

## GitHub Issues

None.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [x] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

| # | Title | Depends On | Group |
|---|-------|------------|-------|
| 001 | Package skeleton: pyproject.toml + clasr entry point | — | 1 |
| 002 | clasr/links.py — symlink-with-copy-fallback | 001 | 2 |
| 003 | clasr/markers.py — named provider marker blocks | 001 | 2 |
| 004 | clasr/frontmatter.py — union frontmatter parser and projector | 001 | 2 |
| 005 | clasr/manifest.py — per-platform per-provider manifests | 001 | 2 |
| 006 | clasr/cli.py skeleton — install/uninstall subcommands + --instructions | 001 | 2 |
| 014 | clasr/merge.py — JSON deep-merge for multi-provider passthrough | 001 | 2 |
| 007 | clasr/platforms/claude.py — Claude platform installer | 002, 003, 004, 005, 006, 014 | 3 |
| 008 | clasr/platforms/codex.py — Codex platform installer | 002, 003, 004, 005, 006, 014 | 3 |
| 009 | clasr/platforms/copilot.py — Copilot platform installer | 002, 003, 004, 005, 006, 014 | 3 |
| 010 | clasr/platforms/detect.py — platform detection | 007, 008, 009 | 4 |
| 011 | Wire CLI install/uninstall to platform modules | 007, 008, 009 | 4 |
| 012 | Test: three-platform roundtrip | 011 | 5 |
| 013 | Test: multi-tenant (two providers, one target) | 011 | 5 |

**Groups**: Tickets in the same group can execute in parallel.
Groups execute sequentially (1 before 2, etc.).
