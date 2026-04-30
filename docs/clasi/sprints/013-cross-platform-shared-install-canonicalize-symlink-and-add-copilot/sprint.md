---
id: "013"
title: "Cross-platform shared install: canonicalize, symlink, and add Copilot"
status: planning
branch: sprint/013-cross-platform-shared-install-canonicalize-symlink-and-add-copilot
use-cases:
  - SUC-001
  - SUC-002
  - SUC-003
  - SUC-004
  - SUC-005
  - SUC-006
  - SUC-007
  - SUC-008
todos:
  - docs/clasi/todo/cross-platform-agent-config-canonicalize-and-symlink.md
  - docs/clasi/todo/add-github-copilot-platform-support.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 013: Cross-platform shared install: canonicalize, symlink, and add Copilot

## Goals

1. **Canonicalize the shared install** — Write skill content once to the
   cross-tool standard location (`.agents/skills/<n>/SKILL.md`) and symlink
   platform-specific aliases instead of duplicating content on disk. Apply the
   same pattern to `CLAUDE.md` → `AGENTS.md`. Provide a `--copy` fallback for
   environments where symlinks fail (Windows without dev mode, sandboxed CI).

2. **Add Copilot as a third platform** — After the symlink machinery is in
   place, add `clasi init --copilot` to emit Copilot-specific files
   (`.github/copilot-instructions.md`, path-scoped instruction files,
   `.github/agents/<n>.agent.md`, `.vscode/mcp.json`). Copilot's skills and
   main instructions are free under the canonical model; only the unique files
   need writing.

The two goals are tightly ordered: canonicalize first so the Copilot installer
consumes the link helper from day one (no "render twice then refactor" cost).

## Problem

CLASI currently writes skill content independently for each platform. The
`.agents/skills/` canonical location (adopted by Codex, Copilot, Cursor, Gemini,
and ~30 other tools under the Agent Skills spec) is already being written by the
Codex installer, but Claude's `.claude/skills/` is a separate full copy. The
community pattern — and the approach used by every serious multi-platform install
tool (ai-rules-sync, agent-skill-creator, skills-manager) — is to write once and
symlink. Drift between independent copies is the real cost, not disk space.

`CLAUDE.md` is the analogous problem for instructions: ~23 agent tools have
adopted `AGENTS.md` as the cross-tool standard; `CLAUDE.md` is only needed as a
shim. The established workaround (~60k public repos) is a `CLAUDE.md` → `AGENTS.md`
symlink.

Copilot is the third major platform and shares enough of the `AGENTS.md` / Agent
Skills standard with what CLASI already installs that the marginal install cost is
small — most content is already on disk.

## Solution

### Track A — Canonicalize + symlink for existing platforms

1. New shared module `clasi/platforms/_links.py` with `link_or_copy(canonical,
   alias, copy_flag)`: try `os.symlink`, fall back to `shutil.copy2` if symlink
   fails or `--copy` is set. Tracks created operations for clean uninstall.

2. Verify that Codex already writes canonical `.agents/skills/` content (it does)
   and is the canonical owner; tighten any implementation drift.

3. Refactor `claude.py` skills install: replace the direct `.claude/skills/<n>/SKILL.md`
   copy with `link_or_copy(canonical=.agents/skills/<n>/SKILL.md,
   alias=.claude/skills/<n>/SKILL.md)`. The canonical is always written (by the
   `_links.py` layer, owned agnostically of platform flags) so `--claude`-only
   installs still work.

4. Refactor `claude.py` instructions: replace the direct `CLAUDE.md` write with
   `link_or_copy(canonical=AGENTS.md, alias=CLAUDE.md)`. Default: symlink.
   `CLAUDE.md` uninstall removes the symlink/copy; never `AGENTS.md`.

5. Add `--copy` flag to `clasi init` and `clasi uninstall`. Default: symlink-first
   with `--copy` fallback for Windows/CI.

6. Migration logic: detect existing direct-copy installs (`.claude/skills/<n>/` is
   a real directory matching canonical content) → convert to symlink after
   content-match confirmation, controlled by `--migrate` flag.

### Track B — Add Copilot platform

7. New module `clasi/platforms/copilot.py` mirroring claude.py/codex.py shape,
   using `_links.py` so `.github/skills/` symlinks to `.agents/skills/`.

8. `.github/copilot-instructions.md`: marker-managed, entry-point sentence +
   global rules content, analogous to Codex root AGENTS.md.

9. `.github/instructions/<n>.instructions.md`: path-scoped rule files with
   `applyTo:` glob frontmatter, sourced from `_rules.py`.

10. `.github/agents/<n>.agent.md`: sub-agent definitions (passthrough Markdown +
    YAML frontmatter rewrite). No TOML render needed (Copilot uses Markdown like
    Claude).

11. `.vscode/mcp.json`: JSON-merge writer (same pattern as `.mcp.json`).

12. Wire `--copilot` flag into `clasi init` / `clasi uninstall`. Update
    interactive prompt to offer Copilot as a fourth option.

13. Update `detect.py` to recognize Copilot signals.

### Track C — Verification and docs

14. End-to-end install correctness test for `--claude --codex --copilot`.

15. CI drift verifier: script + test-suite invocation that asserts all
    "should be symlinks or identical content" pairs hold their invariant.

16. README update: shared-canonical-symlink pattern, Copilot install footprint,
    cloud-agent MCP manual step.

## Success Criteria

- `clasi init --claude --codex --copilot` produces a complete, non-redundant
  multi-platform install in a clean tmp directory.
- `.claude/skills/<n>/SKILL.md` is a symlink to `.agents/skills/<n>/SKILL.md`
  (or an identical copy under `--copy`).
- `CLAUDE.md` is a symlink to `AGENTS.md` (or an identical copy under `--copy`).
- `clasi uninstall --claude --codex --copilot` removes only what install created;
  canonical `.agents/skills/` content is preserved.
- All new Copilot files round-trip parse their schema (YAML frontmatter, JSON).
- CI drift verifier detects any symlink-vs-canonical mismatch.
- Full test suite green.

## Scope

### In Scope

- `clasi/platforms/_links.py` — new shared symlink-with-copy-fallback module
- Refactor `claude.py` skills install to use `_links.py` (symlink to canonical)
- Refactor `claude.py` `CLAUDE.md` write to use `_links.py` (symlink to `AGENTS.md`)
- `--copy` flag on `clasi init` and `clasi uninstall`
- Migration logic for existing direct-copy installs (`--migrate` flag)
- `clasi/platforms/copilot.py` with full install/uninstall
- `.github/copilot-instructions.md` writer (marker-managed)
- `.github/instructions/<n>.instructions.md` writer with `applyTo:` glob
- `.github/agents/<n>.agent.md` writer
- `.vscode/mcp.json` JSON-merge writer
- `--copilot` flag wired into CLI
- `detect.py` Copilot signal recognition
- End-to-end three-platform install test
- CI drift verifier
- README update

### Out of Scope

- VS Code chat modes (`.github/chatmodes/*.chatmode.md`) and prompt files
- Cloud-agent MCP automation via `gh api` (manual-step message only)
- JetBrains-specific testing
- `--all` shortcut for `clasi init --claude --codex --copilot`
- Claude Code adoption of `.agents/skills/` natively (tracked separately)
- Multi-agent system best-practices research (deferred by stakeholder)

## Test Strategy

- Unit tests for `_links.py`: both symlink and copy code paths; uninstall path
  removes alias but not canonical.
- Unit tests for migration logic: content-match detection, symlink conversion.
- Claude installer unit tests updated for symlink-based skill/CLAUDE.md install.
- Copilot installer unit tests: round-trip parse all emitted files; marker
  preservation for `copilot-instructions.md`; JSON merge for `.vscode/mcp.json`;
  detection tests.
- End-to-end three-platform install correctness test (analogue to existing
  `test_codex_install_end_to_end`).
- CI drift verifier test.

## Architecture Notes

- Canonical ownership: `.agents/skills/` is platform-agnostic and always written
  regardless of which platform flags are active. The `_links.py` layer owns the
  canonical write. Platform installers create aliases.
- Dependency direction: `claude.py`, `codex.py`, `copilot.py` all import
  `_links.py`; `_links.py` is a leaf (no CLASI imports).
- `CLAUDE.md` symlink uninstall semantics: remove the symlink/copy; never remove
  `AGENTS.md` (owned by the Codex installer or standalone).
- Sub-agent formats: Codex TOML stays rendered; Claude and Copilot Markdown bodies
  are identical — `.github/agents/<n>.agent.md` can be a symlink to
  `.claude/agents/<n>/agent.md` if frontmatter schemas are compatible (verify
  during ticket execution).
- Open question deferred to implementer: does the `.github/agents/` body need a
  translation pass to drop Claude-Code-specific phrasing? Established precedent
  says defer.

## GitHub Issues

(None linked at sprint creation.)

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan

## Tickets

| # | Title | Depends On | Group |
|---|-------|------------|-------|
| 001 | New module `_links.py`: symlink-with-copy-fallback helper | — | 1 |
| 002 | Add `--copy` flag to `clasi init` and `clasi uninstall` CLI | — | 1 |
| 003 | Refactor `claude.py` skills install to use `_links.py` | 001, 002 | 2 |
| 004 | Refactor `claude.py` CLAUDE.md write to symlink AGENTS.md | 001, 002 | 2 |
| 005 | Migration logic for existing direct-copy installs | 001 | 2 |
| 006 | New module `copilot.py` with install/uninstall skeleton | 001 | 2 |
| 007 | Copilot: `.github/copilot-instructions.md` writer | 006 | 3 |
| 008 | Copilot: `.github/instructions/<n>.instructions.md` writer | 006 | 3 |
| 009 | Copilot: `.github/agents/<n>.agent.md` writer | 006 | 3 |
| 010 | Copilot: `.vscode/mcp.json` JSON-merge writer | 006 | 3 |
| 011 | Wire `--copilot` flag into CLI and update `detect.py` | 006 | 3 |
| 012 | End-to-end three-platform install test and CI drift verifier | 003, 004, 007, 008, 009, 010, 011 | 4 |

**Groups**: Tickets in the same group can execute in parallel.
Groups execute sequentially (1 before 2, etc.).
