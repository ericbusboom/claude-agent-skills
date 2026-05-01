---
sprint: "013"
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 013 Use Cases

## SUC-001: Canonical skill location at `.agents/skills/` with `.claude/skills/` as symlinks

**Actor**: Developer running `clasi init --claude` (with or without `--codex`)

**Precondition**: A project directory exists. CLASI plugin skills are bundled.

**Main Flow**:
1. Developer runs `clasi init --claude` (optionally with `--codex`).
2. CLASI writes each skill to `.agents/skills/<n>/SKILL.md` as the canonical location.
3. CLASI creates `.claude/skills/<n>/SKILL.md` as a symlink pointing at the canonical.
4. Claude Code discovers skills from `.claude/skills/` (its native path) and reads the
   canonical content via the symlink.
5. Any other tool that reads `.agents/skills/` (Codex, Copilot, Cursor, etc.) also
   finds the same content without duplication.

**Alternate Flow — `--copy` flag**:
- If `--copy` is specified or symlink creation fails, CLASI copies the file instead and
  emits a warning that drift detection is recommended.

**Postcondition**: Skill content exists in exactly one place on disk. `.claude/skills/`
aliases it rather than duplicating it.

**Acceptance Criteria**:
- [ ] `.agents/skills/<n>/SKILL.md` is written for every bundled skill.
- [ ] `.claude/skills/<n>/SKILL.md` is a symlink (default) or identical copy (`--copy`)
      pointing at `.agents/skills/<n>/SKILL.md`.
- [ ] `clasi init --claude` without `--codex` still writes the canonical.
- [ ] Symlink failure falls back to copy with a warning, not an error exit.

---

## SUC-002: `CLAUDE.md` as a symlink to `AGENTS.md`

**Actor**: Developer running `clasi init --claude`

**Precondition**: Project directory exists. `AGENTS.md` will be created if absent.

**Main Flow**:
1. Developer runs `clasi init --claude`.
2. CLASI writes (or updates) `AGENTS.md` with the CLASI entry-point block.
3. CLASI creates `CLAUDE.md` as a symlink to `AGENTS.md` (or a copy under `--copy`).
4. Claude Code reads `CLAUDE.md` via the symlink and sees the `AGENTS.md` content.
5. All other tools that read `AGENTS.md` directly also see the same content.

**Alternate Flow — Claude-only install**:
- `AGENTS.md` is written by the `_links.py` layer even if `--codex` is not active,
  so the symlink target always exists.

**Postcondition**: `CLAUDE.md` and `AGENTS.md` point to the same content.

**Acceptance Criteria**:
- [ ] `CLAUDE.md` is a symlink to `AGENTS.md` after `clasi init --claude`.
- [ ] `clasi uninstall --claude` removes the `CLAUDE.md` symlink but not `AGENTS.md`.
- [ ] `--copy` mode produces an identical regular file at `CLAUDE.md`.
- [ ] If `CLAUDE.md` already exists as a regular file not matching `AGENTS.md`,
      CLASI refuses and suggests `--migrate`.

---

## SUC-003: `--copy` fallback when symlinks fail

**Actor**: Developer on Windows without Developer Mode, or in a sandboxed CI environment

**Precondition**: Symlink creation is unavailable or `--copy` flag is set.

**Main Flow**:
1. Developer runs `clasi init --claude --copy` (or CLASI detects symlink failure).
2. CLASI uses `shutil.copy2` instead of `os.symlink` for all alias operations.
3. CLASI emits a notice: copies were used; run CI drift verifier to detect divergence.
4. Install completes successfully with identical file content at all alias paths.

**Postcondition**: Install succeeds with file copies. Drift verifier available for CI.

**Acceptance Criteria**:
- [ ] `clasi init --copy` produces regular files (not symlinks) at all alias paths.
- [ ] Content of alias files is byte-for-byte identical to the canonical.
- [ ] A notice is printed distinguishing copy mode from symlink mode.
- [ ] `clasi uninstall --copy` removes the copies, not the canonicals.

---

## SUC-004: CI drift verifier detects symlink-vs-canonical mismatch

**Actor**: CI pipeline or developer running the test suite

**Precondition**: CLASI has been installed (with symlinks or copies).

**Main Flow**:
1. CI runs the drift verifier (test or standalone script).
2. The verifier finds all `(canonical, alias)` pairs expected by the install.
3. For each pair: if alias is a symlink, assert it resolves to the canonical; if a
   regular file, assert content matches the canonical byte-for-byte.
4. Any mismatch is reported with affected paths and suggested remediation.

**Postcondition**: CI fails with a clear error on drift; passes on consistency.

**Acceptance Criteria**:
- [ ] Verifier detects a manually edited alias file and reports the mismatch.
- [ ] Verifier passes on a clean symlink install.
- [ ] Verifier passes on a clean `--copy` install (identical content).
- [ ] Verifier is invocable from the test suite without manual setup.

---

## SUC-005: `clasi init --copilot` writes Copilot-specific files

**Actor**: Developer running `clasi init --copilot`

**Precondition**: Project directory exists. CLASI plugin content is bundled.

**Main Flow**:
1. Developer runs `clasi init --copilot`.
2. CLASI writes/updates `.github/copilot-instructions.md` with marker-managed
   entry-point + global rules block.
3. CLASI writes `.github/instructions/<n>.instructions.md` for each path-scoped rule
   with `applyTo:` glob frontmatter. Content from `_rules.py`.
4. CLASI writes `.github/agents/<n>.agent.md` for team-lead, sprint-planner,
   programmer (YAML frontmatter + Markdown body).
5. CLASI merges CLASI server entry into `.vscode/mcp.json`.
6. CLASI creates `.github/skills/` as a symlink to `.agents/skills/` (or copy).
7. Post-install: CLASI prints cloud-agent MCP manual-step message with JSON snippet.

**Postcondition**: Copilot Cloud, IDE Copilot, and Workspaces have full CLASI coverage.

**Acceptance Criteria**:
- [ ] `.github/copilot-instructions.md` exists with CLASI marker block; user content
      outside the block is preserved on re-install.
- [ ] `.github/instructions/` contains one file per path-scoped rule, each with valid
      `applyTo:` frontmatter.
- [ ] `.github/agents/team-lead.agent.md` has a `description` field and valid body.
- [ ] `.vscode/mcp.json` contains the `clasi` server entry; existing user keys preserved.
- [ ] Cloud-agent MCP notice is printed to stdout after install.

---

## SUC-006: `clasi init --claude --codex --copilot` produces a complete multi-platform install

**Actor**: Developer wanting full three-platform CLASI coverage

**Precondition**: Clean project directory.

**Main Flow**:
1. Developer runs `clasi init --claude --codex --copilot`.
2. Canonical content written once: `.agents/skills/<n>/SKILL.md`, `AGENTS.md`,
   nested `AGENTS.md` files.
3. Platform-specific aliases created: `.claude/skills/` symlinks, `CLAUDE.md` symlink,
   `.github/skills/` symlink.
4. Platform-unique files written: `.claude/rules/`, `.codex/agents/*.toml`,
   `.github/copilot-instructions.md`, `.github/instructions/`, `.github/agents/`,
   `.mcp.json`, `.vscode/mcp.json`, `.codex/config.toml`.
5. Each platform agent can discover skills and instructions through its native paths.

**Postcondition**: Three-platform install with zero skill content duplication.

**Acceptance Criteria**:
- [ ] Running `clasi init --claude --codex --copilot` in a clean directory exits 0.
- [ ] Skill SKILL.md files exist only at `.agents/skills/<n>/SKILL.md` (not duplicated).
- [ ] `.claude/skills/<n>/SKILL.md` and `.github/skills/<n>/SKILL.md` are symlinks.
- [ ] `CLAUDE.md` is a symlink to `AGENTS.md`.
- [ ] All three platforms' unique files are present.
- [ ] Full test suite is green after the combined install.

---

## SUC-007: `clasi uninstall` removes only what install created (precision uninstall)

**Actor**: Developer running `clasi uninstall` with any combination of platform flags

**Precondition**: CLASI was previously installed.

**Main Flow**:
1. Developer runs `clasi uninstall --claude` (or other flags).
2. For symlink aliases: the symlink is removed. Canonical file untouched.
3. For copy aliases: the copy is removed. Canonical untouched.
4. Canonical `.agents/skills/` content removed only if `--codex` uninstalled AND no
   other platform consumer remains.
5. `AGENTS.md` is never removed by `--claude` uninstall.
6. User files in CLASI-managed directories that CLASI did not create are preserved.
7. Leaf directories get `rmdir`-if-empty. Parent dirs (`.agents/`, `.github/`) not touched.

**Postcondition**: Only CLASI-installed files removed. No user content lost.

**Acceptance Criteria**:
- [ ] After `clasi uninstall --claude`, canonical `.agents/skills/` files still exist.
- [ ] After `clasi uninstall --claude`, `AGENTS.md` still exists (not removed).
- [ ] User files added to `.claude/skills/<n>/` are preserved.
- [ ] `.agents/` and `.github/` parent directories are not deleted even if empty of
      CLASI content.

---

## SUC-008: Cloud-agent MCP manual-step messaging (post-install)

**Actor**: Developer who has just run `clasi init --copilot`

**Precondition**: Copilot install completed. Cloud-agent MCP is not auto-committable.

**Main Flow**:
1. After `copilot.install()` completes, CLASI prints a post-install notice.
2. Notice explains: cloud-agent MCP requires a manual step in GitHub repo Settings
   under "Copilot" → "MCP servers".
3. Notice includes the exact JSON snippet and the Settings URL pattern.
4. Notice is emitted for any install that includes `--copilot`.

**Postcondition**: Developer has actionable instructions to complete cloud-agent MCP.

**Acceptance Criteria**:
- [ ] Post-install notice is printed to stdout after any `--copilot` install.
- [ ] Notice includes the JSON snippet for the MCP server entry.
- [ ] Notice includes the GitHub Settings URL pattern.
- [ ] Notice is not skipped in combined installs (`--claude --codex --copilot`).
