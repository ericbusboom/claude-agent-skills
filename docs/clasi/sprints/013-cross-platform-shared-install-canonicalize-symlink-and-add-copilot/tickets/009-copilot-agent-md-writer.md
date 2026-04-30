---
id: "013-009"
title: "Copilot: .github/agents/<n>.agent.md writer"
status: todo
sprint: "013"
use-cases:
  - SUC-005
depends-on:
  - "013-006"
---

# 013-009: Copilot: `.github/agents/<n>.agent.md` writer

## Description

Implement `_install_agents` and `_uninstall_agents` in `copilot.py`.

Each active CLASI agent (team-lead, sprint-planner, programmer) gets a
`.github/agents/<name>.agent.md` file. These are GitHub Copilot custom agent
definitions (Markdown + YAML frontmatter; see GitHub docs for the custom agents
configuration spec).

Required frontmatter field: `description`. Optional: `name`, `model`, `tools`,
`mcp-servers`, `metadata`.

Body content: sourced from `plugin/agents/<name>/agent.md` (the same source used by
the Claude installer for `.claude/agents/<name>/agent.md`). The frontmatter is
rewritten to the Copilot schema. Body phrasing (e.g., "dispatch via Agent tool") is
preserved as-is per established precedent — the implementer may adjust if the phrasing
is obviously incorrect for Copilot, but no forced translation pass is required.

Note: unlike Codex, Copilot agents use Markdown (not TOML), so the content transform
is minimal: read frontmatter from `plugin/agents/<name>/agent.md`, map fields to
Copilot schema, write `<copilot-frontmatter>\n\n<body>`.

## Acceptance Criteria

- [ ] After `_install_agents(target)`, `.github/agents/` contains one `.agent.md` file
      per active CLASI agent (team-lead, sprint-planner, programmer).
- [ ] Each file has valid YAML frontmatter with a `description` field.
- [ ] `description` is sourced from the agent's `plugin/agents/<name>/agent.md`
      frontmatter (or a reasonable fallback if absent in the source).
- [ ] The body (after the frontmatter block) is the agent Markdown content from
      `plugin/agents/<name>/agent.md`.
- [ ] Files parse cleanly as Markdown with YAML frontmatter.
- [ ] `_uninstall_agents(target)` removes the per-agent files. User-created files in
      `.github/agents/` are preserved. Directory `rmdir`-if-empty.
- [ ] Tests: round-trip parse frontmatter of each emitted file; assert `description`
      present; assert body non-empty. Uninstall precision (only CLASI-written files
      removed; user file preserved).
- [ ] `python -m pytest --no-cov` green.

## Implementation Plan

### Approach

Mirror the Codex `_install_agents` pattern but write Markdown instead of TOML:

```python
_AGENT_NAMES = ["team-lead", "sprint-planner", "programmer"]

def _install_agents(target: Path) -> None:
    agents_dir = target / ".github" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    for agent_name in _AGENT_NAMES:
        agent_md = _PLUGIN_DIR / "agents" / agent_name / "agent.md"
        if not agent_md.exists():
            click.echo(f"  Warning: plugin/agents/{agent_name}/agent.md not found, skipping")
            continue
        # Parse source frontmatter
        fm, body = _parse_frontmatter(agent_md.read_text(encoding="utf-8"))
        description = fm.get("description", f"CLASI {agent_name} agent")
        # Build Copilot frontmatter
        copilot_fm = {"description": description}
        if "model" in fm:
            copilot_fm["model"] = fm["model"]
        content = "---\n" + yaml.dump(copilot_fm, default_flow_style=False) + "---\n\n" + body
        dest = agents_dir / f"{agent_name}.agent.md"
        dest.write_text(content, encoding="utf-8")
        click.echo(f"  Wrote: .github/agents/{agent_name}.agent.md")
```

Use the existing `clasi.frontmatter` module for parsing (or yaml/re — check what the
codebase already uses in `codex.py`'s `_install_agents`).

### Files to Modify

- `clasi/platforms/copilot.py` — implement `_install_agents`, `_uninstall_agents`.
- `tests/unit/test_platform_copilot.py` — add agent writer tests.

### Testing Plan

Use `tmp_path`. Assert `.github/agents/team-lead.agent.md` exists and has
`description` in frontmatter. Assert body contains the agent role text. After
uninstall, assert files are removed and a user-created `.github/agents/my-agent.md`
is untouched.

### Documentation Updates

None at this stage.
