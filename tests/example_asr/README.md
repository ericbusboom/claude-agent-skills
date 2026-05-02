# tests/example_asr/

A complete `asr/` source directory for trying out `clasr` by hand. It
exercises every piece: skills, agents, rules with platform-specific
frontmatter, per-platform passthrough subdirs (`claude/`, `codex/`,
`copilot/`), and JSON files that get merged when multiple providers
ship them.

## Try it

From the repo root, install all three platforms into a throwaway
target:

```sh
mkdir -p /tmp/clasr-demo
clasr install \
  --source tests/example_asr \
  --provider example \
  --target /tmp/clasr-demo \
  --claude --codex --copilot
```

Look at what got written:

```sh
find /tmp/clasr-demo -type f -o -type l | sort
```

You should see:

- `/tmp/clasr-demo/AGENTS.md`, `/tmp/clasr-demo/CLAUDE.md` — both
  contain a `<!-- BEGIN clasr:example -->` marker block.
- `/tmp/clasr-demo/.github/copilot-instructions.md` — same block,
  written only by the copilot installer.
- `/tmp/clasr-demo/.claude/skills/code-review/SKILL.md` — symlink to
  the canonical at `.agents/skills/code-review/SKILL.md`.
- `/tmp/clasr-demo/.claude/agents/reviewer.md`,
  `/tmp/clasr-demo/.github/agents/reviewer.agent.md`,
  `/tmp/clasr-demo/.codex/agents/reviewer.md` — three different
  rendered files from the same source, with platform-projected
  frontmatter.
- `/tmp/clasr-demo/.github/instructions/python-style.instructions.md`
  — Copilot rule with `applyTo:` preserved.
- `/tmp/clasr-demo/.claude/settings.json`,
  `/tmp/clasr-demo/.codex/notes.md`,
  `/tmp/clasr-demo/.github/.vscode/mcp.json` — passthrough files
  copied straight from the platform-specific source subdirs. Note
  that Copilot passthrough is rooted at `.github/`, so a source path
  of `copilot/.vscode/mcp.json` lands at `.github/.vscode/mcp.json`,
  not the target root.
- `/tmp/clasr-demo/.claude/.clasr-manifest/example.json` (and one
  under each platform dir) — what `clasr` wrote, used for clean
  uninstall.

## Multi-tenant demo

Run the install a second time with a different provider name to see
multi-tenant in action:

```sh
clasr install --source tests/example_asr --provider example2 \
  --target /tmp/clasr-demo --claude
```

`AGENTS.md` and `CLAUDE.md` will now contain TWO marker blocks
(`clasr:example` and `clasr:example2`). `settings.json` will be JSON-
merged.

## Clean up

```sh
clasr uninstall --provider example --target /tmp/clasr-demo \
  --claude --codex --copilot
clasr uninstall --provider example2 --target /tmp/clasr-demo --claude
rm -rf /tmp/clasr-demo
```

## Read the docs

```sh
clasr --instructions
```
