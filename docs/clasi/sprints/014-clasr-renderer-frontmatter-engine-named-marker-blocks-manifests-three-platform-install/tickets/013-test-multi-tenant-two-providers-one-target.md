---
id: '013'
title: 'Test: multi-tenant (two providers, one target)'
status: done
use-cases:
- SUC-006
depends-on:
- '011'
github-issue: ''
todo: ''
completes_todo: true
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Test: multi-tenant (two providers, one target)

## Description

Write `tests/clasr/test_multi_tenant.py` — the test that validates multi-tenant
coexistence: two different providers (`provider_a` and `provider_b`) install into the
same target directory. Both manifests coexist. Both named marker blocks coexist in the
same file. Uninstalling one provider leaves the other's files and blocks intact.

This is the critical test for the "multi-tenant by design" requirement from the TODO spec.

## Acceptance Criteria

### Multi-tenant coexistence (marker blocks and manifests)

- [x] `tests/clasr/test_multi_tenant.py` exists and passes
- [x] Provider A and Provider B each have their own `asr/` source directories
- [x] Both providers install into the same target directory (same `.claude/`)
- [x] After both installs: `.claude/.clasr-manifest/provider_a.json` exists
- [x] After both installs: `.claude/.clasr-manifest/provider_b.json` exists
- [x] After both installs: `AGENTS.md` contains `<!-- BEGIN clasr:provider_a -->` block
- [x] After both installs: `AGENTS.md` contains `<!-- BEGIN clasr:provider_b -->` block
      (both blocks coexist in the same file)
- [x] After both installs: `CLAUDE.md` contains both blocks
- [x] Uninstall Provider A: `provider_a.json` manifest deleted
- [x] After uninstalling Provider A: `provider_b.json` manifest still exists
- [x] After uninstalling Provider A: Provider B's skills, agents, rules still present
- [x] After uninstalling Provider A: `<!-- BEGIN clasr:provider_b -->` block in AGENTS.md
      is intact; `<!-- BEGIN clasr:provider_a -->` block is stripped
- [x] Skills from both providers coexist in `.claude/skills/` (different skill names)
- [x] All existing `clasi` tests still pass

### JSON-merge install (new — Q2 resolution)

- [x] Provider A ships `asr/claude/settings.json` with `{"mcpServers": {"svc_a": {...}}}`;
      Provider B ships `asr/claude/settings.json` with `{"mcpServers": {"svc_b": {...}}}`.
      After both installs: `.claude/settings.json` contains both `svc_a` and `svc_b` keys.
- [x] Provider A's manifest records `kind: "copy"` for `settings.json` (first writer);
      Provider B's manifest records `kind: "json-merged"` with `"keys": ["mcpServers"]`.
- [x] When provider B's key conflicts with provider A's key in the same JSON file,
      a WARNING is emitted to stderr naming both providers.

### JSON-merge uninstall — per-provider key removal (new — Q2 resolution)

- [x] Non-overlapping keys (keyA / keyB): uninstalling provider_b removes keyB but leaves
      keyA intact (provider_a's contribution survives).
- [x] `.claude/settings.json` still exists after uninstalling provider_b (keyA remains).
- [x] After uninstalling both providers: `.claude/settings.json` is deleted entirely.

### Non-JSON passthrough collision (new — Q2 resolution)

- [x] Provider A ships `asr/claude/commands/foo.md`. Installing Provider B with the same
      `asr/claude/commands/foo.md` target raises a RuntimeError naming both providers.
      Provider A's file is not overwritten.

## Implementation Plan

### Approach

Create two fixture `asr/` directories with different provider names and skill names.
Both include a `claude/settings.json` passthrough (with different but non-overlapping
`mcpServers` keys so the first test is conflict-free, and a second variant with the same
key for the conflict-warning test).

Call `claude.install()` for provider_a, then for provider_b (same target tmpdir). Assert
coexistence (marker blocks and merged JSON). Call `claude.uninstall(provider="provider_a")`.
Assert per-key removal — provider_b's keys survive. Call `claude.uninstall(provider_b)`.
Assert file deleted.

Add a separate test for the non-JSON collision error path.

### Files to Create

- `tests/clasr/test_multi_tenant.py`

If a shared `conftest.py` was not created in ticket 012, create it here for the
`make_asr_dir(provider_name, skill_names, settings_keys=None)` fixture factory helper.
The helper should accept optional `settings_keys` to control which `mcpServers` keys
appear in the generated `settings.json`.
