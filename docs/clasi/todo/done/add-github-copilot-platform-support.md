---
status: done
sprint: '013'
tickets:
- '006'
- '007'
- 008
- 009
- '010'
- '011'
- '012'
---

# Add GitHub Copilot platform support (`clasi init --copilot`)

Installer module covering all three Copilot variants: cloud Coding
Agent, IDE Copilot (VS Code / JetBrains / Visual Studio), and
Workspaces / Codespaces.

## Why

CLASI currently supports Claude Code (`.claude/...`) and OpenAI Codex
CLI (`.codex/...`, `.agents/skills/`, `AGENTS.md`). Copilot is the
third major surface and shares enough of the agents.md / Agent Skills
standard with what we already install that the marginal cost is
small. Plus the user wants their CLASI workflows to continue working
when they (or collaborators) drive any Copilot variant.

## What Copilot actually reads (research summary, 2026-04-30)

| Variant | Instruction files | Skills | Sub-agents | MCP | Hooks |
|---|---|---|---|---|---|
| **Cloud Coding Agent** (`@copilot` in PRs/issues) | `AGENTS.md` (root + nested), `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md` (path-scoped via `applyTo:`) | `.github/skills/`, `.claude/skills/`, `.agents/skills/` | `.github/agents/<name>.agent.md` (Markdown + YAML) | Repo Settings UI (not a committed file); `mcp-servers` frontmatter in custom agents | None |
| **IDE Copilot** (VS Code / JetBrains / Visual Studio) | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `AGENTS.md` (VS Code) | Same set as cloud (VS Code agent mode) | Same `.github/agents/*.agent.md` | `.vscode/mcp.json` (workspace) or user `mcp.json` | None |
| **Workspaces / Codespaces** | Codespaces hosts IDE Copilot (no extra surface). Workspace itself: no documented unique config beyond cloud-agent paths. | Inherits from cloud / IDE | Inherits | Inherits | None |

### Already covered incidentally (no new install work)

- `AGENTS.md` (root + nested `docs/clasi/AGENTS.md`,
  `docs/clasi/todo/AGENTS.md`, `clasi/AGENTS.md`) — Copilot reads them all.
- `.agents/skills/<name>/SKILL.md` — Copilot reads them.
- `.claude/skills/<name>/SKILL.md` — Copilot also reads these per the
  Agent Skills spec, so dual-platform installs already supply skills
  to Copilot.

### Missing for full Copilot coverage

- `.github/copilot-instructions.md` — legacy/secondary instructions
  (still active).
- `.github/instructions/<name>.instructions.md` with `applyTo:` glob
  frontmatter — path-scoped rules. This is the closest GitHub
  equivalent of Claude's `.claude/rules/<name>.md` with `paths:`.
- `.github/agents/<name>.agent.md` — sub-agent definitions (Markdown
  body + YAML frontmatter). Required field: `description`. Optional:
  `name`, `target`, `tools`, `model`, `mcp-servers`, `metadata`.
- `.vscode/mcp.json` — for IDE-Copilot users; shape is
  `{ "servers": { "clasi": { "command": "clasi", "args": ["mcp"] } } }`
  (verify exact key during implementation).
- Cloud-agent MCP is **not** committable. Document the manual repo-
  Settings step or add an opt-in `gh api` automation.

## Proposed fix (sprint-sized; suggested ticket decomposition)

1. **Add `clasi/platforms/copilot.py`** with `install(target,
   mcp_config)` and `uninstall(target)` mirroring `claude.py` and
   `codex.py`. Reuse shared rule content from
   `clasi/platforms/_rules.py` and the marker-block helpers from
   `clasi/platforms/_markers.py`.

2. **`.github/copilot-instructions.md`** — emit a CLASI-marker-managed
   file containing the entry-point sentence (a `_COPILOT_ENTRY_POINT`
   analogous to the Claude/Codex ones, pointing at
   `.github/agents/team-lead.agent.md`) plus the global-scope rules
   content (mcp-required + git-commits) — same composition we just
   landed for Codex AGENTS.md.

3. **`.github/instructions/<name>.instructions.md`** for each
   path-scoped Claude rule:
   - `clasi-artifacts.instructions.md` with `applyTo: "docs/clasi/**"`
   - `todo-dir.instructions.md` with `applyTo: "docs/clasi/todo/**"`
   - `source-code.instructions.md` with `applyTo: "clasi/**"`
   - Plus `mcp-required` and `git-commits` with `applyTo: "**"` (or
     fold into copilot-instructions.md global block — implementer
     decides which is cleaner for `applyTo: "**"` content).
   - Source content from `_rules.py` so it stays canonical.

4. **`.github/agents/<name>.agent.md`** for each active CLASI agent
   (team-lead, sprint-planner, programmer). YAML frontmatter must
   include `description`; body is the agent role text from
   `clasi/plugin/agents/<name>/agent.md`. This is *Markdown*, not
   TOML like Codex — so almost passthrough the source `.md` file with
   frontmatter rewritten.

5. **`.vscode/mcp.json`** — JSON-merge with existing user content;
   only add the `clasi` server entry (mirrors how `.mcp.json` merge
   works on the Claude side).

6. **Wire `--copilot` flag into `clasi init` and `clasi uninstall`**
   ([clasi/cli.py](../../../clasi/cli.py),
   [clasi/init_command.py](../../../clasi/init_command.py),
   [clasi/uninstall_command.py](../../../clasi/uninstall_command.py)).
   Allow `clasi init --claude --codex --copilot` (any combination).
   Default behavior with no flag stays Claude-only (backward compat).
   Update the interactive prompt to offer Copilot as a fourth option.

7. **Update `clasi/platforms/detect.py`** to recognize Copilot signals:
   `.github/copilot-instructions.md`, `.github/agents/`,
   `.github/instructions/`, `code` / `codium` / `gh` on PATH
   (advisory). Add to `PlatformSignals` dataclass.

8. **Cloud-agent MCP**: not auto-installable (repo Settings UI).
   Two options to discuss during planning:
   - **(a)** Print a clear post-install message telling the user to
     add it manually with the JSON snippet to paste.
   - **(b)** Ship a `clasi copilot setup-cloud-mcp` helper that uses
     `gh api` to set the repo Copilot MCP config (requires `gh` and
     appropriate scope).
   - Default to (a) for simplicity.

9. **Uninstall** symmetric to install: marker-managed sections
   stripped from `.github/copilot-instructions.md`, instruction/agent
   files we wrote get unlinked (mirror Claude's per-name iteration
   pattern that landed in sprint 012/003-004), `.vscode/mcp.json`
   gets the `clasi` key removed, no whole-directory deletes.

10. **Tests**:
    - End-to-end install correctness test analogous to
      `test_codex_install_end_to_end` — round-trip parse every
      emitted file against its actual schema.
    - User-content preservation tests for
      `.github/copilot-instructions.md` (marker-managed) and
      `.vscode/mcp.json` (JSON merge).
    - Detection tests in `test_platform_detect.py`.

11. **Docs**: README section describing the copilot install
    footprint and the cloud-agent-MCP manual step.

## Open questions for the planner

- Should `.claude/skills/` continue to be written by `--claude` only,
  or should `--copilot` also write `.claude/skills/` on the
  assumption that Copilot reads it? Probably **only `--claude` writes
  `.claude/skills/`** — keep each platform installer scoped to its
  own paths — and Copilot users get skills via `.agents/skills/`
  (Copilot reads both, so either source works).
- Should `.github/agents/<name>.agent.md` content be the verbatim
  Claude `agent.md` body, or rewritten to drop Claude-Code-specific
  phrasing ("dispatch via Agent tool")? Same open question as Codex
  sub-agent content — defer to implementer per established precedent.
- Does the sprint scope include the optional `gh api` cloud-MCP
  automation, or is that a follow-on? Recommend follow-on to keep
  this sprint focused.
- VS Code chat modes (`.github/chatmodes/*.chatmode.md`) and prompts
  (`.github/prompts/*.prompt.md`) — out of scope for first cut.
  Could be a future "expose CLASI skills as Copilot slash commands"
  sprint.

## Verification

1. `python -m pytest --no-cov` — full suite green.
2. Install in a tmp dir: `clasi init --copilot`. Inspect emitted
   files match the spec; round-trip parse `.vscode/mcp.json`,
   `.github/agents/team-lead.agent.md` frontmatter, etc.
3. Smoke: open the tmp dir as a project in VS Code with Copilot
   agent mode, confirm Copilot picks up the `team-lead` custom agent
   and the path-scoped instructions fire when touching
   `docs/clasi/todo/...`.

## Out of scope (track separately if needed)

- VS Code chat modes / prompt files exposing CLASI skills as
  `/<name>` slash commands.
- Cloud-agent MCP automation via `gh api`.
- JetBrains-specific testing (we'd rely on JetBrains reading the
  same `.github/copilot-instructions.md` per docs).
- A possible `--all` shortcut for `clasi init --claude --codex
  --copilot`.

## Origin

Stakeholder asked: "do a plan for how to set up GitHub co-pilots to
operate on the agents and rules and skills." Research dispatched to
confirm Copilot's actual read paths across cloud, IDE, and Workspaces
variants — primary sources cited inline above (links in original
research; key items: `AGENTS.md` cloud-agent support 2025-08-28,
Agent Skills 2025-12-18, custom agents config reference at
docs.github.com/en/copilot/reference/custom-agents-configuration).
