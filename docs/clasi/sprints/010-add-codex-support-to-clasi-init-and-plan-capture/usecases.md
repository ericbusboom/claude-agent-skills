---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 010 Use Cases

## SUC-001: Default init preserves Claude-only behavior

- **Actor**: Developer (non-interactive, no platform flag)
- **Preconditions**: Running `clasi init` with no `--claude` or `--codex` flag in a
  non-interactive context (e.g., CI, piped stdin, script).
- **Main Flow**:
  1. Developer runs `clasi init` or `clasi install` with no platform flag.
  2. CLASI detects non-interactive context.
  3. CLASI installs Claude artifacts: `CLAUDE.md`, `.claude/rules/`, `.claude/skills/`,
     `.claude/agents/`, `.claude/settings.json`, `.claude/settings.local.json`,
     `.mcp.json`, `docs/clasi/todo/`, `docs/clasi/log/.gitignore`.
  4. No Codex artifacts are created.
- **Postconditions**: Project is configured for Claude only; no `.codex/`, `.agents/skills/`,
  or `AGENTS.md` created by CLASI.
- **Acceptance Criteria**:
  - [ ] Default `clasi init` (no flag, non-interactive) does not create `.codex/` or `.agents/`.
  - [ ] `clasi install` is accepted as a synonym and produces the same result.

---

## SUC-002: Explicit `--claude` flag installs Claude platform

- **Actor**: Developer
- **Preconditions**: Developer supplies `--claude` flag (interactive or non-interactive).
- **Main Flow**:
  1. Developer runs `clasi init --claude [target]` or `clasi install --claude [target]`.
  2. CLASI runs the existing Claude install path unconditionally.
  3. Claude artifacts are written; Codex artifacts are not touched.
- **Postconditions**: Project is configured for Claude. Same output as the default path.
- **Acceptance Criteria**:
  - [ ] `clasi init --claude` installs the existing Claude project setup.
  - [ ] No Codex artifacts are created when only `--claude` is supplied.

---

## SUC-003: Explicit `--codex` flag installs Codex platform

- **Actor**: Developer
- **Preconditions**: Developer supplies `--codex` flag.
- **Main Flow**:
  1. Developer runs `clasi init --codex [target]`.
  2. CLASI runs the Codex install path:
     a. Creates or updates `AGENTS.md` with a CLASI marker-managed section.
     b. Writes `.codex/config.toml` with `[mcp_servers.clasi]` using the detected MCP
        command and `codex_hooks = true`.
     c. Writes `.codex/hooks.json` with a `Stop` entry calling
        `clasi hook codex-plan-to-todo`.
     d. Writes `.agents/skills/se/SKILL.md` sourced from bundled plugin content.
  3. Idempotent: re-running updates CLASI-managed sections without clobbering user content.
- **Postconditions**: Project is configured for Codex. Claude artifacts are not touched.
- **Acceptance Criteria**:
  - [ ] `clasi init --codex` creates `AGENTS.md`, `.codex/config.toml`,
        `.codex/hooks.json`, and `.agents/skills/se/SKILL.md`.
  - [ ] Re-running `clasi init --codex` is idempotent and preserves unrelated config in
        each file.
  - [ ] Claude-specific files (`CLAUDE.md`, `.claude/`) are not created or modified.

---

## SUC-004: Combined `--claude --codex` installs both platforms

- **Actor**: Developer
- **Preconditions**: Developer supplies both `--claude` and `--codex` flags.
- **Main Flow**:
  1. Developer runs `clasi init --claude --codex [target]`.
  2. CLASI runs the Claude install path, then the Codex install path.
  3. Both sets of artifacts are written in one invocation.
- **Postconditions**: Project is configured for both Claude and Codex.
- **Acceptance Criteria**:
  - [ ] `clasi init --claude --codex` installs both platform integrations in one run.
  - [ ] Each platform installer operates independently; Claude install does not fail if
        Codex install has not run previously, and vice versa.

---

## SUC-005: `install` synonym for `init`

- **Actor**: Developer
- **Preconditions**: Developer types `clasi install` instead of `clasi init`.
- **Main Flow**:
  1. Developer runs `clasi install [flags] [target]`.
  2. CLI routes `install` to the same handler as `init`, with the same options.
- **Postconditions**: Behavior is identical to `clasi init` with the same arguments.
- **Acceptance Criteria**:
  - [ ] `clasi install` is recognized as a valid command by the CLI.
  - [ ] `clasi install --claude`, `clasi install --codex`, and
        `clasi install --claude --codex` all behave identically to the equivalent
        `clasi init` invocations.

---

## SUC-006: Interactive platform prompt when no flag is supplied

- **Actor**: Developer (interactive terminal)
- **Preconditions**: CLASI is run interactively with no `--claude` or `--codex` flag.
- **Main Flow**:
  1. Developer runs `clasi init` in a terminal with no flags.
  2. CLASI inspects advisory platform signals: `.claude/`, `CLAUDE.md`, `.codex/`,
     `.agents/skills/`, `AGENTS.md`, installed commands (`claude`, `codex`), home config
     directories (`~/.claude`, `~/.codex`), and environment variable names only
     (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc., values never read or printed).
  3. CLASI determines a recommendation based on signals (project-configured platform
     preferred; if none, user-level signals used; if both, recommend both).
  4. CLASI presents a prompt: "Install for: [1] Claude  [2] Codex  [3] Both  (recommended: X)"
  5. Developer selects an option.
  6. CLASI installs the selected platform(s).
- **Postconditions**: Selected platform(s) are installed. No secret values are read or
  printed.
- **Acceptance Criteria**:
  - [ ] Interactive `clasi init` presents Claude, Codex, and both as choices with a
        detected recommendation.
  - [ ] Non-interactive `clasi init` (no flag) does not prompt; defaults to Claude only.
  - [ ] Platform detection reads only file presence, command availability, home config
        directories, and environment variable names — never values.
  - [ ] If both platforms are detected at project level, both are recommended.

---

## SUC-007: Uninstall removes selected platform's CLASI-managed files

- **Actor**: Developer
- **Preconditions**: CLASI has been installed on one or both platforms. Developer specifies
  `--claude`, `--codex`, or both.
- **Main Flow**:
  1. Developer runs `clasi uninstall --claude`, `--codex`, or `--claude --codex`.
  2. For the Claude platform, CLASI removes:
     - CLASI section from `CLAUDE.md` (marker-managed block).
     - CLASI-managed `.claude/skills/`, `.claude/agents/`, `.claude/rules/`.
     - CLASI hook entries in `.claude/settings.json`.
     - CLASI MCP permission entry in `.claude/settings.local.json`.
  3. For the Codex platform, CLASI removes:
     - CLASI section from `AGENTS.md` (marker-managed block).
     - CLASI-managed `.agents/skills/`.
     - CLASI hook entries in `.codex/hooks.json`.
     - CLASI MCP server entry in `.codex/config.toml`.
  4. Shared artifacts (`docs/clasi/`, `.mcp.json`) are preserved.
- **Postconditions**: Selected platform's CLASI-managed artifacts are removed. User-owned
  content in the same files is preserved.
- **Acceptance Criteria**:
  - [ ] `clasi uninstall --claude` removes only Claude CLASI-managed artifacts.
  - [ ] `clasi uninstall --codex` removes only Codex CLASI-managed artifacts.
  - [ ] `clasi uninstall --claude --codex` removes both.
  - [ ] Uninstall of a platform that was never installed is a no-op (idempotent).

---

## SUC-008: Uninstall preserves user-owned and shared content

- **Actor**: Developer
- **Preconditions**: Files contain both CLASI-managed sections and user-owned content.
- **Main Flow**:
  1. Developer runs `clasi uninstall --claude` or `--codex`.
  2. In marker-managed files (`CLAUDE.md`, `AGENTS.md`), only the `<!-- CLASI:START -->`
     to `<!-- CLASI:END -->` block is removed.
  3. In structured files (`.codex/config.toml`, `.codex/hooks.json`,
     `.claude/settings.json`), only CLASI-specific keys or entries are removed.
  4. Files that contain only CLASI-managed content and nothing else may be deleted.
  5. Shared project artifacts (`docs/clasi/todo/`, sprint history, `.mcp.json`) are never
     removed.
- **Postconditions**: User content is intact. Only CLASI-managed sections/entries removed.
- **Acceptance Criteria**:
  - [ ] `clasi uninstall` preserves TODOs, sprint artifacts, logs, and existing
        `.claude/`, `.codex/`, `.agents/`, `CLAUDE.md`, and `AGENTS.md` user content.
  - [ ] If a config file contains both CLASI and user entries, only the CLASI entry is
        removed; the file is not deleted.

---

## SUC-009: Interactive uninstall detects installed platforms and prompts

- **Actor**: Developer (interactive terminal)
- **Preconditions**: Developer runs `clasi uninstall` with no platform flag interactively.
- **Main Flow**:
  1. CLASI inspects installed CLASI-managed platform files to determine which platforms are
     installed.
  2. CLASI presents choices: "Uninstall: [1] Claude  [2] Codex  [3] Both" with detected
     installed platforms highlighted.
  3. Developer selects.
  4. CLASI runs the selected uninstall path(s).
- **Postconditions**: Selected platform(s) are uninstalled.
- **Acceptance Criteria**:
  - [ ] Interactive `clasi uninstall` (no flag) presents a prompt based on detected
        installed CLASI platform integrations.
  - [ ] Non-interactive `clasi uninstall` (no flag) exits with an error asking for an
        explicit flag.

---

## SUC-010: Codex Stop hook captures `<proposed_plan>` as a pending TODO

- **Actor**: Codex agent (Stop hook trigger)
- **Preconditions**: Codex completes a session that produced a `<proposed_plan>` block in
  `last_assistant_message`.
- **Main Flow**:
  1. Codex fires the `Stop` hook, invoking `clasi hook codex-plan-to-todo`.
  2. Handler reads `last_assistant_message` from stdin JSON.
  3. Handler extracts the content inside `<proposed_plan>...</proposed_plan>`.
  4. Handler computes a content hash of the extracted plan.
  5. Handler checks `docs/clasi/todo/` for an existing file with the same `source_hash`.
  6. If no match: writes a new TODO file with `status: pending`, `source: codex-plan`,
     `source_hash: <hash>`, and the plan body.
  7. If match: skips creation (de-dupe).
  8. Handler exits 0 (no blocking).
- **Postconditions**: Exactly one pending TODO exists per unique plan content.
- **Acceptance Criteria**:
  - [ ] `clasi hook codex-plan-to-todo` with no `<proposed_plan>` in the message is a
        no-op (exits 0, no TODO created).
  - [ ] `clasi hook codex-plan-to-todo` with a `<proposed_plan>` block creates one pending
        TODO under `docs/clasi/todo/`.
  - [ ] Re-running the hook with the same plan content does not create a duplicate TODO
        (de-dupe by content hash).
  - [ ] TODO frontmatter includes `source: codex-plan` and `source_hash`.

---

## SUC-011: Existing Claude `ExitPlanMode` plan-to-todo behavior is preserved

- **Actor**: Claude Code (PostToolUse hook, ExitPlanMode)
- **Preconditions**: Claude Code fires the `plan-to-todo` hook after ExitPlanMode.
- **Main Flow**:
  1. Claude Code fires `clasi hook plan-to-todo`.
  2. Handler reads the plan file path from the hook payload.
  3. Handler copies the plan to `docs/clasi/todo/` with `status: pending` frontmatter.
  4. Handler blocks further implementation via exit 2.
- **Postconditions**: Plan is captured as TODO; Claude stops implementation.
- **Acceptance Criteria**:
  - [ ] Existing `clasi hook plan-to-todo` behavior is unchanged and all existing tests
        continue to pass.
  - [ ] The `source` and `source_hash` frontmatter fields added for Codex are optional
        and absent from Claude-originated TODOs unless explicitly set.

---

## SUC-012: TOML dependency added for Python 3.10 compatibility

- **Actor**: Programmer / CI environment
- **Preconditions**: Project targets Python >= 3.10.
- **Main Flow**:
  1. `tomli` is added as a conditional dependency (`python_requires < "3.11"`) in
     `pyproject.toml`.
  2. `tomli-w` is added as an unconditional dependency.
  3. Codex install and uninstall code reads/writes `.codex/config.toml` using
     `tomllib` (stdlib, 3.11+) or `tomli` (3.10 fallback) for reading and `tomli-w`
     for writing.
- **Postconditions**: TOML read/write works on Python 3.10 and 3.11+.
- **Acceptance Criteria**:
  - [ ] `pyproject.toml` declares `tomli` as a Python < 3.11 dependency and `tomli-w`
        unconditionally.
  - [ ] Code that reads TOML uses a try/import shim compatible with both versions.
  - [ ] TOML write uses `tomli_w.dumps()` unconditionally.
