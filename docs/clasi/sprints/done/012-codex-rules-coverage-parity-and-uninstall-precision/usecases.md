---
sprint: "012"
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Use Cases — Sprint 012

## SUC-001: Codex agent operating in project root sees global rules

**Actor**: Codex agent performing git operations or general project work.

**Trigger**: Agent begins a task that involves committing code or verifying the MCP server.

**Pre-conditions**: `clasi init --codex` has been run. Root `AGENTS.md` exists with
both the CLASI entry-point block and a second named rules block.

**Main Flow**:
1. Codex resolves `AGENTS.md` upward from the working directory to the project root.
2. Root `AGENTS.md` contains the `mcp-required` rule and the `git-commits` rule
   inside the named rules marker block.
3. Agent applies both rules before committing or calling CLASI MCP tools.

**Post-conditions**: Agent applies both global-scope rules without any path-specific context.

**Acceptance Criteria**:
- [ ] Root `AGENTS.md` contains a second marker block (`<!-- CLASI:RULES:START -->`)
      distinct from the entry-point block (`<!-- CLASI:START -->`).
- [ ] The rules block contains the full text of `mcp-required` and `git-commits` rules.
- [ ] Uninstall strips only the rules block; entry-point block survives (and vice versa).

---

## SUC-002: Codex agent operating in `docs/clasi/` sees full SE artifact rules

**Actor**: Codex sprint-planner agent creating or modifying sprint artifacts.

**Trigger**: Agent begins work in `docs/clasi/`.

**Pre-conditions**: `clasi init --codex` has been run. `docs/clasi/AGENTS.md` exists
with the full `clasi-artifacts` rule content.

**Main Flow**:
1. Codex resolves `AGENTS.md` upward; finds `docs/clasi/AGENTS.md`.
2. The file contains the complete rule: confirm active sprint, check sprint phase before
   ticketing, use MCP tools only.
3. Agent verifies sprint status and phase before creating or modifying artifacts.

**Post-conditions**: Agent does not create planning artifacts manually or bypass MCP tools.

**Acceptance Criteria**:
- [ ] `docs/clasi/AGENTS.md` includes the active-sprint check and phase check steps.
- [ ] Content matches the canonical rule in `_rules.py` (no partial mirror).

---

## SUC-003: Codex agent operating in `docs/clasi/todo/` sees todo-dir rule

**Actor**: Codex agent reviewing or closing TODOs.

**Trigger**: Agent begins work in `docs/clasi/todo/`.

**Pre-conditions**: `clasi init --codex` has been run. `docs/clasi/todo/AGENTS.md` exists.

**Main Flow**:
1. Codex resolves `AGENTS.md` upward; finds `docs/clasi/todo/AGENTS.md` first.
2. The file instructs the agent to use the CLASI `todo` skill or `move_todo_to_done`
   MCP tool — not the generic TodoWrite tool.
3. Agent uses `move_todo_to_done` instead of direct file manipulation.

**Post-conditions**: TODO lifecycle is managed through CLASI tooling.

**Acceptance Criteria**:
- [ ] `docs/clasi/todo/AGENTS.md` exists after `clasi init --codex`.
- [ ] Its content matches the `todo-dir` rule from `_rules.py`.
- [ ] Uninstall removes it.

---

## SUC-004: Rule content has a single canonical definition

**Actor**: Developer maintaining the CLASI codebase.

**Trigger**: A rule needs a wording update.

**Pre-conditions**: `_rules.py` exists; both `claude.py` and `codex.py` import from it.

**Main Flow**:
1. Developer edits the rule constant in `_rules.py`.
2. `claude.py` `RULES` dict reflects the change automatically (imports from `_rules.py`).
3. `codex.py` nested AGENTS.md content reflects the change automatically.

**Post-conditions**: One edit propagates to both platforms with no divergence risk.

**Acceptance Criteria**:
- [ ] `claude.py` imports rule content from `_rules.py` (no duplicate hardcoding).
- [ ] `codex.py` imports rule content from `_rules.py` (no duplicate hardcoding).
- [ ] No behavior change on Claude side (pure refactor — rule text identical before/after).

---

## SUC-005: `clasi uninstall --claude` preserves user-added files in skill subdirs

**Actor**: Developer who added a personal `notes.md` to `.claude/skills/se/`.

**Trigger**: Developer runs `clasi uninstall --claude`.

**Pre-conditions**: CLASI Claude platform is installed. User has added
`.claude/skills/se/notes.md`.

**Main Flow**:
1. Uninstaller removes `.claude/skills/se/SKILL.md` (the only file install copied).
2. `.claude/skills/se/` is not empty (`notes.md` remains) so directory is preserved.
3. Output reports partial removal with a message noting user files are preserved.

**Post-conditions**: `notes.md` survives; `SKILL.md` is gone.

**Acceptance Criteria**:
- [ ] Test: install, add `notes.md` inside skill dir, uninstall, assert `notes.md` exists
      and `SKILL.md` is gone.
- [ ] Skill dir itself remains because it is non-empty.

---

## SUC-006: `clasi uninstall --claude` preserves user-added files in agent subdirs

**Actor**: Developer who added a personal `contract.yaml` to `.claude/agents/team-lead/`.

**Trigger**: Developer runs `clasi uninstall --claude`.

**Pre-conditions**: CLASI Claude platform is installed. User has added
`.claude/agents/team-lead/contract.yaml`.

**Main Flow**:
1. Uninstaller iterates `*.md` files that install copied for `team-lead` and removes them.
2. `.claude/agents/team-lead/` still contains `contract.yaml`, so directory is preserved.
3. Output reports partial removal.

**Post-conditions**: `contract.yaml` survives; CLASI-installed `.md` files are gone.

**Acceptance Criteria**:
- [ ] Test: install, add `custom.md` (or non-md file) inside agent dir, uninstall, assert
      user file exists and CLASI `.md` files are gone.
- [ ] Agent dir itself remains because it is non-empty.

---

## SUC-007: `clasi uninstall --codex` does not delete `.agents/` or `.agents/skills/`

**Actor**: Developer who has other tools also using `.agents/`.

**Trigger**: Developer runs `clasi uninstall --codex`.

**Pre-conditions**: CLASI Codex platform is installed. `.agents/` contains a file from
another tool.

**Main Flow**:
1. Uninstaller removes `.agents/skills/se/SKILL.md`; leaf dir rmdir-if-empty stays.
2. `.agents/skills/` is NOT cascaded-rmdir'd.
3. `.agents/` is NOT cascaded-rmdir'd.
4. Other-tool file in `.agents/` survives.

**Post-conditions**: Other tools' content in `.agents/` is intact.

**Acceptance Criteria**:
- [ ] Test: install codex, add `.agents/other-tool-content.md`, uninstall, assert
      `.agents/` still exists and `other-tool-content.md` is intact.
- [ ] `.agents/skills/` may remain empty but is not removed.

---

## SUC-008: Root AGENTS.md survives repeated install/uninstall without block interference

**Actor**: Developer running `clasi init --codex` multiple times.

**Trigger**: Multiple install/uninstall cycles on the same project.

**Pre-conditions**: Root `AGENTS.md` may contain user content outside the CLASI blocks.

**Main Flow**:
1. First install: both the entry-point block and the rules block are written.
2. Uninstall: both blocks stripped independently; user content preserved.
3. Re-install: both blocks restored correctly, user content still intact.

**Post-conditions**: User content outside marker blocks is never damaged; blocks do not
bleed into each other.

**Acceptance Criteria**:
- [ ] Round-trip test for `_markers.py`: both named blocks coexist in the same file;
      stripping one does not touch the other.
- [ ] Both blocks survive a re-install idempotently (no duplication).
