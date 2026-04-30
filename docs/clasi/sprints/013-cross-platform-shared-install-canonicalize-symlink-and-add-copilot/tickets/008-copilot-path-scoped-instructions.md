---
id: "013-008"
title: "Copilot: .github/instructions/<n>.instructions.md writer"
status: todo
sprint: "013"
use-cases:
  - SUC-005
depends-on:
  - "013-006"
---

# 013-008: Copilot: `.github/instructions/<n>.instructions.md` writer

## Description

Implement `_install_path_rules` and `_uninstall_path_rules` in `copilot.py`.

Path-scoped instruction files are the Copilot equivalent of Claude's
`.claude/rules/<n>.md` with `paths:` frontmatter. Each file has:
- YAML frontmatter with a single `applyTo:` glob field.
- A Markdown body sourced from `_rules.py`.

Files to write:

| Filename | `applyTo` glob | Rule body from `_rules.py` |
|---|---|---|
| `clasi-artifacts.instructions.md` | `"docs/clasi/**"` | `CLASI_ARTIFACTS_BODY` |
| `todo-dir.instructions.md` | `"docs/clasi/todo/**"` | `TODO_DIR_BODY` |
| `source-code.instructions.md` | `"clasi/**"` | `SOURCE_CODE_BODY` |
| `mcp-required.instructions.md` | `"**"` | `MCP_REQUIRED_BODY` |
| `git-commits.instructions.md` | `"**"` | `GIT_COMMITS_BODY` |

Note: `mcp-required` and `git-commits` with `applyTo: "**"` overlap with the content
in `copilot-instructions.md` (ticket 007). Implementer should decide whether to fold
the `applyTo: "**"` files into the global block only (avoiding duplication) or write
them as separate files for explicit path scoping. Either choice is acceptable; document
the decision in the ticket.

Files are full-file writes (not marker-managed). Uninstall removes them by name.

## Acceptance Criteria

- [ ] After `_install_path_rules(target)`, `.github/instructions/` contains one
      `.instructions.md` file per CLASI rule.
- [ ] Each file has valid YAML frontmatter with an `applyTo:` field followed by rule
      body content.
- [ ] Frontmatter is parseable by a YAML parser (no syntax errors).
- [ ] Re-running `_install_path_rules` overwrites the files idempotently.
- [ ] `_uninstall_path_rules(target)` removes all written instruction files. Does not
      remove user-created files in `.github/instructions/`.
- [ ] Parent directory `.github/instructions/` is created if absent on install.
- [ ] Parent directory is `rmdir`-if-empty on uninstall.
- [ ] Tests: round-trip parse each emitted file's frontmatter; assert `applyTo` value;
      assert body content matches `_rules.py` constants. Uninstall precision (only
      CLASI-written files removed).
- [ ] `python -m pytest --no-cov` green.

## Implementation Plan

### Approach

Define a list of `(filename, applyTo_glob, rule_body)` tuples and loop:

```python
_PATH_RULES = [
    ("clasi-artifacts.instructions.md", "docs/clasi/**", CLASI_ARTIFACTS_BODY),
    ("todo-dir.instructions.md", "docs/clasi/todo/**", TODO_DIR_BODY),
    ("source-code.instructions.md", "clasi/**", SOURCE_CODE_BODY),
    # Decision point: include global-scope rules here or rely on copilot-instructions.md
    ("mcp-required.instructions.md", "**", MCP_REQUIRED_BODY),
    ("git-commits.instructions.md", "**", GIT_COMMITS_BODY),
]

def _install_path_rules(target: Path) -> None:
    rules_dir = target / ".github" / "instructions"
    rules_dir.mkdir(parents=True, exist_ok=True)
    for fname, apply_to, body in _PATH_RULES:
        content = f'---\napplyTo: "{apply_to}"\n---\n\n{body}\n'
        (rules_dir / fname).write_text(content, encoding="utf-8")
        click.echo(f"  Wrote: .github/instructions/{fname}")
```

For uninstall, iterate the same filename list and unlink each; `rmdir` if empty.

### Files to Modify

- `clasi/platforms/copilot.py` — implement `_install_path_rules`, `_uninstall_path_rules`.
- `tests/unit/test_platform_copilot.py` — add path-rules tests.

### Testing Plan

Use `tmp_path`. After install, parse each file with `yaml.safe_load(frontmatter)`.
Assert `applyTo` field present and correct. Assert body text matches constant. After
uninstall, assert all five files are gone; assert that a user-created file in the same
directory is untouched.

### Documentation Updates

None at this stage.
