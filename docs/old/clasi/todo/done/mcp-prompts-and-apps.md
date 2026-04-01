# MCP Prompts and Apps

Researched 2026-02-10. Conclusion: **wait and see**.

## Findings

- **MCP Prompts** register as `/mcp__servername__promptname` slash commands in
  Claude Code. Verbose naming makes them less useful than thin skill stubs
  (`/todo` vs `/mcp__clasi__todo`). Model can't see available prompts to
  suggest them (GitHub #11054). Stubs give better UX.
- **MCP Resources** could serve artifacts as `@clasi:sprint://004/status`
  context, but tools already serve the same data.
- **MCP Apps** (interactive HTML UIs) — Claude Code doesn't support them.
- **Sampling, Elicitation** — Claude Code doesn't support them.
- **MCP Instructions** — could replace `.claude/rules/` file but current
  approach works fine.

## Decision

No action. Revisit when Claude Code adds support for apps/sampling/elicitation,
or if the MCP prompt naming convention improves.
