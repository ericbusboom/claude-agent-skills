---
status: pending
---

# Plan: Generalized Cross-Platform Agent-Config How-To

## Context

CLASI's sprint-013 work (canonicalize on `.agents/`, symlink the rest, copy fallback for Windows/CI, render only when formats differ) produced a concrete recipe for installing the same content into Claude Code, Codex, and Copilot from one source. The TODO at [docs/clasi/todo/done/cross-platform-agent-config-canonicalize-and-symlink.md](docs/clasi/todo/done/cross-platform-agent-config-canonicalize-and-symlink.md) and the architecture at [docs/clasi/sprints/done/013-.../architecture-update.md](docs/clasi/sprints/done/013-cross-platform-shared-install-canonicalize-symlink-and-add-copilot/architecture-update.md) are CLASI-specific — they bake in SE-process vocabulary (sprints, tickets, team-lead) and CLASI's exact file layout.

The user wants a **generalized** version of this guidance: a how-to written *to another agent* who will build a different domain tool — e.g. a curriculum authoring system, a wireframing assistant — that needs the same multi-platform install behavior. The output should let that agent pick up the recipe and apply it to their own content (skills, instructions, sub-agents, MCP config) without needing CLASI domain knowledge.

The intended outcome: a single self-contained Markdown document the receiving agent can read once and implement against.

## Approach

Write one document at `docs/cross-platform-agent-install-guide.md` (project root `docs/` — sibling of `docs/design/` and `docs/clasi/`, not under `docs/clasi/` since this is meta-guidance, not a CLASI artifact). The document is targeted at a builder-agent, not at humans, and assumes the reader has read access to a codebase and can write Python (or equivalent).

### Document outline

1. **What you're building** — one paragraph: a system that installs the same logical content (skills, instructions, sub-agents, tool config) into each of N coding-agent platforms (Claude Code, Codex, Copilot, Cursor, etc.) from a single source, without on-disk drift.

2. **The five content types you must handle** (table form, platform-agnostic, derived from the TODO's table):
    - Skills — body content + minimal YAML.
    - Top-level instructions — entry-point file the agent reads at session start.
    - Path-scoped rules / sub-instructions — content that should activate only in certain directories.
    - Sub-agents — agent definitions the harness can dispatch.
    - Tool / MCP config — JSON or TOML config the platform uses to find tools.

   For each, list (a) what each platform calls it, (b) the format(s) in use, (c) whether formats match across platforms (so symlink works) or differ (so render is needed).

3. **The core recipe** — three rules:
    - **Canonicalize where formats match.** One source of truth at a cross-tool path (`.agents/skills/`, `AGENTS.md`).
    - **Symlink the aliases.** `.claude/skills/`, `.github/skills/`, `CLAUDE.md` etc. point at the canonical.
    - **Render only when formats genuinely differ.** Codex TOML, Copilot `applyTo:` frontmatter, Cursor `.mdc` — these require a render step, not a symlink.

4. **Module layout the builder should produce** — generalized from CLASI's `clasi/platforms/`:
    - `_links.py` (or equivalent) — the symlink-with-copy-fallback primitive. Single function `link_or_copy(canonical, alias, copy=False) -> "symlink" | "copy"`. Counterpart `unlink_alias(alias)`. Migration helper `migrate_to_symlink(canonical, alias)`. **Leaf node, no upward imports.**
    - `_markers.py` — for marker-block-managed writes into shared files (like AGENTS.md) so multiple installers and humans can share the file without overwriting each other. Pattern: `<!-- BEGIN BLOCK -->...<!-- END BLOCK -->`. Provide `write_section`, `strip_section`, plus named-block variants.
    - `_content.py` (or `_rules.py`) — the canonical bodies of your domain content, kept as Python constants or template files. The single source of every rule/skill/agent body the system installs.
    - `platforms/<name>.py` — one module per platform. Each exposes `install(target, config, copy=False)` and `uninstall(target)`. Each module imports `_links`, `_markers`, `_content`, and writes only into that platform's directories.
    - `detect.py` — read-only probe that recognizes which platforms are present (file signals + binaries on PATH).
    - `init_command.py` — the CLI orchestrator. Threads flags (`--copy`, `--migrate`, per-platform flags) into the installers. Owns the interactive prompt.

5. **Critical invariants** the builder must enforce, generalized from sprint 013's design rationale:
    - **Canonical write is platform-flag-agnostic.** The canonical location is always written, even if only one platform is installed. (Otherwise drift returns when the user later adds another platform.)
    - **Aliases never own the canonical.** Uninstalling a platform removes its aliases, never the canonical (unless that platform is the canonical owner — and then only after checking no other platform's aliases still depend on it).
    - **Marker-block writes preserve user content.** Never overwrite a shared file (AGENTS.md, copilot-instructions.md) wholesale; always rewrite only the block between markers.
    - **Symlink is best-effort.** On OSError fall back to copy with a warning. Never fail the install for a symlink-only failure.
    - **Drift verifier in CI.** A test that walks every (canonical, alias) pair and asserts symlink-or-byte-identical. Catches the case where copy-fallback ran and humans later edited the alias.

6. **Cross-platform pitfalls** — Windows symlink permission, Git `core.symlinks=true`, IDE indexers double-walking symlinked trees, JSON-merge for tool config files (never overwrite — always parse, merge the system's key, write back; bail on parse failure rather than corrupt).

7. **Platform reference table** — for each of the major platforms, the exact paths and formats to write into. The receiving agent extends this table when adding a new platform. Keep CLASI's working set as the seed: Claude Code, Codex, Copilot, with notes on Cursor, Gemini CLI, Windsurf, Aider as drop-in candidates because they read AGENTS.md + `.agents/skills/`.

8. **Suggested implementation sequence** — generalized from the sprint-013 ticket decomposition:
    1. Build the `_links` primitive and unit-test both code paths.
    2. Build the `_markers` primitive and unit-test idempotent writes.
    3. Build one platform installer end-to-end (recommend starting with the AGENTS.md-native one — Codex or Copilot — since it has no shim work).
    4. Build the second platform installer; introduce the canonical/alias split here.
    5. Build the third; verify three-way install round-trips.
    6. Add the drift verifier as a CI test.
    7. Add `--copy` and `--migrate` flags after the symlink path is solid.

9. **What this guide is NOT** — not a spec, not a manifest format. The recipe is a code structure and a set of invariants. Different domains will have different content; the install machinery is what generalizes.

### Files to write

- `docs/cross-platform-agent-install-guide.md` — new file, the guide itself.

### Files to read while writing (already gathered)

- [docs/clasi/todo/done/cross-platform-agent-config-canonicalize-and-symlink.md](docs/clasi/todo/done/cross-platform-agent-config-canonicalize-and-symlink.md) — primary source, has the platform table and community-pattern citations.
- [docs/clasi/sprints/done/013-.../architecture-update.md](docs/clasi/sprints/done/013-cross-platform-shared-install-canonicalize-symlink-and-add-copilot/architecture-update.md) — module shapes, invariants, design rationale, dependency graph (mermaid). Strip CLASI vocabulary when generalizing.
- [clasi/platforms/_links.py](clasi/platforms/) — verify the actual implemented signatures match what the architecture promised before quoting them.

### Verification

This is a documentation deliverable. Verification is a read-through:
- The guide must be self-contained — a builder-agent who has never heard of CLASI must be able to implement against it.
- No CLASI-domain leaks (no "sprint", "ticket", "team-lead", "SE process").
- Every invariant in section 5 must be motivated by a concrete failure mode (e.g. "without this, drift returns when the user adds a second platform").
- The platform table in section 7 must list paths the builder can write to without further research.
