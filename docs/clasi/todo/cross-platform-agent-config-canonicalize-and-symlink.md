---
status: pending
---

# Cross-platform agent config — canonicalize on shared spec, symlink the rest

Reference + design TODO for how CLASI should structure cross-platform
installs going forward. Compiled from primary-source research
2026-04-30.

## What the user actually wants to solve

CLASI installs the SE-process content (skills, agent definitions,
rules, instructions) for multiple coding-agent platforms. Each
platform reads similar (or identical) content from different paths:

| Content | Claude Code | OpenAI Codex CLI | GitHub Copilot |
|---|---|---|---|
| Skills | `.claude/skills/<n>/SKILL.md` | `.agents/skills/<n>/SKILL.md` | reads all of `.github/skills/`, `.claude/skills/`, `.agents/skills/` |
| Instructions | `CLAUDE.md` | `AGENTS.md` (root + nested) | `AGENTS.md`, `.github/copilot-instructions.md` |
| Sub-agents | `.claude/agents/<n>/agent.md` (Markdown+YAML) | `.codex/agents/<n>.toml` (TOML) | `.github/agents/<n>.agent.md` (Markdown+YAML) |
| Rules | `.claude/rules/<n>.md` (`paths:` frontmatter) | nested `AGENTS.md` (no native scope) | `.github/instructions/<n>.instructions.md` (`applyTo:` glob) |
| MCP config | `.mcp.json` | `.codex/config.toml` | `.vscode/mcp.json` + repo Settings (cloud) |

Today CLASI duplicates skill content on disk for each platform that
gets installed. That's wasteful and prone to drift if anyone hand-
edits one copy.

## Findings (2026-04-30, primary sources cited inline)

### Cross-tool standards are real and growing

- **AGENTS.md** has ~23 named adopters: Codex, Cursor, Aider, Zed,
  Warp, VS Code, Copilot Coding Agent, Gemini CLI, Junie, Amp,
  Goose, OpenCode, Windsurf, Devin, Factory, Kilo, RooCode, Augment,
  Jules, etc. Claude Code is the conspicuous holdout — it reads
  `CLAUDE.md` natively. **The standard workaround is a `CLAUDE.md`
  -> `AGENTS.md` symlink.** ~60k+ public repos contain an AGENTS.md.
  <https://agents.md/>

- **Agent Skills** (agentskills.io, published by Anthropic Dec 2025,
  now under Agentic AI Foundation neutral governance) has 32 listed
  adopters as of March 2026 including Claude Code, Codex, Cursor,
  Gemini CLI, Copilot/VS Code, Amp, Goose, OpenHands, OpenCode,
  Firebender, plus ecosystem players (Google, JetBrains, Block,
  Snowflake, Databricks, ByteDance, Mistral, Spring AI). The spec
  itself is tiny: directory with `SKILL.md` containing `name` +
  `description` YAML frontmatter and Markdown body. ~85k public
  skills exist.
  <https://agentskills.io/specification>

- **`.agents/skills/`** is the **emerging de facto cross-tool
  location** but the spec doesn't authoritatively mandate a
  discovery path. Codex explicitly scans `.agents/skills/`; OpenCode
  and several others follow. Per-tool dirs (`.claude/skills/`,
  `.cursor/`, `.roo/`) persist alongside it.
  <https://developers.openai.com/codex/skills>

- **Sub-agents:** no spec, no consensus. Markdown+YAML is two-thirds
  of the surface (Claude Code + Copilot); Codex uses TOML.
  Cross-platform migration guides tell users to re-author.

- **MCP discovery:** no shared file; each tool reads its own.

### Lowest-common-denominator that works today

`AGENTS.md` (instructions) + `.agents/skills/<n>/SKILL.md` (skills).
Covers Codex, Copilot, Cursor, Gemini, Junie, Amp, Goose, OpenCode,
etc. Claude Code requires a shim.

### How others handle multi-platform install

Three real OSS projects worth studying as prior art:

- **lbb00/ai-rules-sync** — single Git source of truth, **symlinks**
  into each tool's directory ("Stop copying `.mdc` files around…
  sync via symbolic links"). Targets Cursor, Copilot, Claude Code,
  Trae, OpenCode, Codex, Gemini CLI, Warp, Windsurf, Cline.
  <https://github.com/lbb00/ai-rules-sync>

- **FrancyJGLisboa/agent-skill-creator** — **hybrid**: one canonical
  `SKILL.md`, symlinks into `~/.agents/skills/` for tools that read
  the standard, **format adapters** that render `.mdc` (Cursor) and
  `.md` rules (Windsurf) for tools that don't. 14 platforms.
  <https://github.com/FrancyJGLisboa/agent-skill-creator>

- **xingkongliang/skills-manager** — desktop GUI managing skills
  across 15+ tools via a shared workspace + symlinks.
  <https://github.com/xingkongliang/skills-manager>

- **TheQtCompanyRnD/agent-skills** — Qt's official cross-tool skill
  bundle, ships once for Claude/Codex/Copilot/Gemini/Cursor.
  <https://github.com/TheQtCompanyRnD/agent-skills>

**Manifest-driven generation** (one YAML → per-platform configs) is
rarer in OSS; the dominant pattern is **symlink-from-canonical** for
matching formats, **render-from-canonical** only when formats
genuinely differ (`.mdc`, TOML, etc.).

### Symlink trade-offs

- Windows requires Developer Mode or admin for `mklink`.
- Git on Windows handles symlinks only with `core.symlinks=true`.
- Some IDE indexers double-walk symlinked trees.

These are real but routine. Provide a `--copy` fallback for Windows
and CI sandboxes that can't symlink.

### Skills duplication specifically

The community has **converged on `.agents/skills/` as the canonical
install location** with symlinks (or duplicates) from
`.claude/skills/`, `.github/skills/`, etc. Codex reads
`.agents/skills/` natively; Claude Code as of April 2026 reads
`.claude/skills/` and surfaces project skills via plugins, **not**
`.agents/skills/` directly — so a symlink/copy is still required
for Claude.

Cost of duplicating SKILL.md text on disk is trivial — kilobyte-
scale Markdown. The real cost is **drift** when duplicates are
edited independently. Every serious project uses symlinks or a
render step rather than blind `cp`.

## TL;DR for CLASI

The community has an answer to the question. CLASI should adopt it:

1. **Canonicalize content where formats match.** Single source under
   `.agents/skills/<n>/SKILL.md`; symlink `.claude/skills/` →
   `.agents/skills/` rather than installing twice. Drop the
   `.claude/skills/` direct write path once Claude Code adopts
   `.agents/skills/` natively (track the open issue, OOP-able when
   it lands).

2. **Symlink `CLAUDE.md` → `AGENTS.md`.** Keep them as one file.
   AGENTS.md becomes the authoritative project-instructions file;
   CLAUDE.md is a shim until Claude Code reads AGENTS.md.

3. **Keep the Python-side render approach (`_rules.py`) only where
   formats genuinely differ.** Specifically:
   - Codex sub-agent TOML (`.codex/agents/<n>.toml`) — different
     format, render needed.
   - Copilot's `.github/instructions/*.instructions.md` `applyTo:`
     glob frontmatter — different metadata schema, render needed.
   - Don't render Markdown-to-Markdown (`.claude/agents/<n>/agent.md`
     and `.github/agents/<n>.agent.md`) when a symlink suffices —
     the body content is the same.

4. **Provide a `--copy` fallback** for Windows/CI environments where
   symlinks fail. Default is symlink, fall back on failure with a
   warning.

5. **Add a CI verifier** that detects drift between symlinked
   targets and copies. Single check: `find . -name SKILL.md` →
   assert all checksums match the canonical.

## Suggested ticket decomposition (for a future sprint)

1. **`clasi/platforms/_links.py`** — shared helper that does
   "symlink with copy fallback" and tracks operations for clean
   uninstall. Input: canonical path + alias path. Behavior: try
   symlink, fall back to copy if symlink fails. Test: both code
   paths.

2. **Codex installer** — make `.agents/skills/` the canonical write
   path (already is). Update install/uninstall to reflect canonical
   ownership.

3. **Claude installer** — replace direct `.claude/skills/<n>/SKILL.md`
   write with a symlink-or-copy pointing at the canonical
   `.agents/skills/<n>/SKILL.md`. Requires `--codex` (or implicit
   `.agents/skills/` install) to have run first; if not, install
   the canonical content alongside.

4. **`CLAUDE.md` → `AGENTS.md` symlink** for project-local instructions.
   Replace the project-CLAUDE.md write with a symlink to AGENTS.md
   when both `--claude` and an AGENTS.md-aware platform are being
   installed. Add a `--no-claude-md-symlink` escape hatch for users
   who genuinely want CLAUDE.md to differ.

5. **Sub-agents** — Codex TOML stays rendered. For Claude (Markdown)
   and Copilot (Markdown), the content body is identical; symlink
   `.github/agents/<n>.agent.md` → `.claude/agents/<n>/agent.md` (or
   to a canonical agent-source). Frontmatter schema differs slightly
   (Copilot has `applyTo` for instructions, not agents) so verify
   compatibility before symlinking.

6. **CI drift verifier** — script + GitHub Action that checks all
   "should be symlinks or identical content" pairs hold their
   invariant. Useful for the CLASI repo itself (since we dogfood)
   and exportable as a CLI subcommand for end-user projects.

7. **Tests + README update** documenting the canonicalize+symlink
   strategy and the `--copy` fallback flag.

## Open questions for the planner

- **Default behavior on install conflict:** if `.claude/skills/se/`
  already exists as a regular directory (from an older CLASI
  install), the new symlink-based install needs to either replace
  it (lose user edits) or refuse. Suggest: detect, show a clear
  error with a `--migrate` flag that converts legacy copies into
  symlinks after a content match check.
- **Uninstall semantics:** removing the symlink should never remove
  the canonical `.agents/skills/<n>/`. Mirror the precision-uninstall
  work from sprint 012 — only delete what install created.
- **Order dependence:** if a user runs `clasi init --claude` without
  `--codex`, where does the canonical `.agents/skills/` content
  live? Two options: always write `.agents/skills/` (regardless of
  flag) and have `--claude` symlink in; or keep platform-scoped
  ownership and only symlink when both flags are active. The first
  is simpler and matches the community pattern (`.agents/skills/`
  is universal anyway).
- **Track Claude Code's `.agents/skills/` adoption.** Once Claude
  Code reads it natively, drop the symlink entirely.

## What this is NOT

- Not a sprint plan — this is reference + design. Implementation
  belongs in a future sprint.
- Not a request to refactor everything immediately. Current sprint
  012 architecture (per-platform installers, shared `_rules.py`)
  is fine; the canonicalize+symlink work is a follow-on
  improvement.
- Not a replacement for the Copilot platform support TODO (which
  remains the next concrete install-extension task). This TODO
  changes HOW we install, not WHAT we install.

## Related TODOs

- [add-github-copilot-platform-support.md](add-github-copilot-platform-support.md)
  — Copilot platform install. The work here might warrant landing
  Copilot first, then doing the canonicalize+symlink refactor
  across all three platforms in one pass.
- [multi-agent-system-best-practices-research-compilation.md](multi-agent-system-best-practices-research-compilation.md)
  — orthogonal (orchestrator/sub-agent best practices, not
  cross-platform install).

## Origin

Stakeholder asked: "do research on how you deal with the fact that
the skills that Claude uses are the same structure as the skills
that Copilot uses, but they're in different directories." Research
dispatched. Primary findings: community has converged on
canonicalize-on-`.agents/skills/`-and-symlink-the-rest, with format
adapters only for genuinely different formats (Cursor `.mdc`, Codex
TOML, etc.). CLASI's current "render twice" approach for matching
formats (e.g., the SKILL.md files themselves) is at odds with the
community pattern.
