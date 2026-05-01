---
id: 013-012
title: End-to-end three-platform install test, CI drift verifier, and README update
status: done
sprint: '013'
use-cases:
- SUC-004
- SUC-006
depends-on:
- 013-003
- 013-004
- 013-007
- 013-008
- 013-009
- 013-010
- 013-011
---

# 013-012: End-to-end three-platform install test, CI drift verifier, and README update

## Description

This is the verification and documentation ticket. It depends on all Track A and Track B
tickets being complete. Three deliverables:

1. **End-to-end install correctness test** for `--claude --codex --copilot` combined.
2. **CI drift verifier** asserting all canonical/alias pairs hold their invariant.
3. **README update** documenting the shared-canonical-symlink pattern, Copilot install
   footprint, and cloud-agent MCP manual step.

## Acceptance Criteria

### End-to-End Test

- [x] A test `test_three_platform_install_end_to_end` exists in
      `tests/unit/test_init_command.py` (or `test_platform_copilot.py`).
- [x] The test runs `clasi init --claude --codex --copilot` against a `tmp_path`.
- [x] Asserts all canonical files exist:
  - `.agents/skills/<n>/SKILL.md` for every bundled skill.
  - `AGENTS.md` with CLASI marker block.
- [x] Asserts all symlink aliases:
  - `.claude/skills/<n>/SKILL.md` is a symlink to `.agents/skills/<n>/SKILL.md`.
  - `CLAUDE.md` is a symlink to `AGENTS.md`.
  - `.github/skills/` is a symlink to `.agents/skills/`.
- [x] Asserts no SKILL.md content duplication (no regular file copies at alias paths
      in default mode).
- [x] Asserts all three platforms' unique files are present:
  - `.claude/rules/*.md` (5 files)
  - `.codex/agents/*.toml` (3 agents)
  - `.github/copilot-instructions.md`
  - `.github/instructions/*.instructions.md` (5 files)
  - `.github/agents/*.agent.md` (3 agents)
  - `.mcp.json`, `.vscode/mcp.json`, `.codex/config.toml`
- [x] Round-trip parses YAML frontmatter for all `.instructions.md` and `.agent.md` files.
- [x] Round-trip parses `.vscode/mcp.json` as valid JSON with `servers.clasi` present.
- [x] Test exits green.

### CI Drift Verifier

- [x] A test function `test_drift_verifier` (or a helper callable from CI) asserts:
  - For each `(canonical, alias)` pair in a CLASI install:
    - If `alias` is a symlink: assert `alias.resolve() == canonical.resolve()`.
    - If `alias` is a regular file: assert `alias.read_bytes() == canonical.read_bytes()`.
- [x] Covered pairs:
  - `.agents/skills/<n>/SKILL.md` ↔ `.claude/skills/<n>/SKILL.md`
  - `.agents/skills/<n>/SKILL.md` ↔ `.github/skills/<n>/SKILL.md` (via directory symlink)
  - `AGENTS.md` ↔ `CLAUDE.md`
- [x] The verifier reports all mismatches (not just the first) with clear path output.
- [x] A test invokes the verifier against a clean three-platform install and asserts pass.
- [x] A test manually breaks one alias (edit file content) and asserts the verifier
      reports the mismatch.

### README Update

- [x] README section added (or updated) describing:
  - The shared-canonical-symlink pattern: "CLASI writes skills once to `.agents/skills/`
    and symlinks platform-specific aliases."
  - The `--copy` flag for environments where symlinks are unavailable.
  - The `--migrate` flag for converting legacy installs.
  - Copilot install footprint: list of files written by `clasi init --copilot`.
  - Cloud-agent MCP manual step: what to do in GitHub Settings after `--copilot` install.
- [x] Existing README content is not removed or broken.

### Final Gate

- [x] Full test suite `python -m pytest --no-cov` green after all ticket 012 changes.

## Implementation Plan

### Approach

The end-to-end test is a straightforward integration test against a `tmp_path`. Use
`subprocess.run` or call `init_command.init_command` directly (whichever the existing
end-to-end tests use — follow the pattern in `test_codex_install_end_to_end`).

The drift verifier is a helper function `check_drift(target: Path) -> list[str]`
(returns list of mismatch messages). Tests call it and assert the list is empty (no
drift) or non-empty (drift detected).

The README update is a plain Markdown addition to the appropriate section in
`README.md` (or `docs/` if the project uses a docs directory — check existing README
location).

### Files to Modify

- `tests/unit/test_init_command.py` (or new `test_platform_copilot.py`) — add
  `test_three_platform_install_end_to_end` and `test_drift_verifier`.
- `README.md` (or appropriate docs file) — add canonicalize+symlink and Copilot sections.

### Testing Plan

The tests ARE the deliverable for this ticket. No additional meta-testing needed.

### Documentation Updates

README update is a primary deliverable of this ticket.
