---
id: "007"
title: "Add clasi/uninstall_command.py and clasi uninstall CLI command"
status: todo
use-cases:
  - SUC-007
  - SUC-008
  - SUC-009
depends-on:
  - "002"
  - "003"
  - "004"
github-issue: ""
todo: ""
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Add clasi/uninstall_command.py and clasi uninstall CLI command

## Description

Add `clasi uninstall` as a new CLI command with `--claude` and `--codex` flags.
Implement `clasi/uninstall_command.py` as a thin dispatcher that calls the appropriate
platform uninstaller(s) from `clasi/platforms/`. Interactive mode (no flag) inspects
installed CLASI platform files and prompts the user.

Depends on tickets 002 (Claude uninstall), 003 (detect), and 004 (Codex uninstall).

## Acceptance Criteria

- [ ] `clasi uninstall --claude` runs `clasi.platforms.claude.uninstall(target)`.
- [ ] `clasi uninstall --codex` runs `clasi.platforms.codex.uninstall(target)`.
- [ ] `clasi uninstall --claude --codex` runs both uninstallers.
- [ ] Interactive `clasi uninstall` (no flags, tty) inspects installed CLASI platform
      files and presents: "Uninstall: [1] Claude  [2] Codex  [3] Both".
- [ ] Non-interactive `clasi uninstall` with no flags exits with a clear error message
      asking for an explicit flag.
- [ ] Uninstall does not touch `docs/clasi/`, `.mcp.json`, or any non-CLASI content.
- [ ] Uninstalling a platform that was never installed is a no-op (idempotent, no error).
- [ ] Tests in `tests/unit/test_uninstall_command.py` cover:
  - `--claude` only removes Claude artifacts.
  - `--codex` only removes Codex artifacts.
  - `--claude --codex` removes both.
  - Non-interactive, no flag: exits with error.
  - Interactive, no flag: prompts (mocked).
  - Idempotency: running uninstall twice does not error.
  - User content preservation: `CLAUDE.md` user section and `AGENTS.md` user section
    survive uninstall.

## Implementation Plan

### Files to create

- `clasi/uninstall_command.py`
- `tests/unit/test_uninstall_command.py`

### Files to modify

- `clasi/cli.py` — register `clasi uninstall` command

### Approach

**`clasi/uninstall_command.py`**:

```python
def run_uninstall(target: str, claude: bool = False, codex: bool = False) -> None:
    target_path = Path(target).resolve()
    interactive = sys.stdin.isatty() and sys.stdout.isatty()

    if not claude and not codex:
        if interactive:
            choice = _prompt_uninstall(target_path)
            claude = choice in ("claude", "both")
            codex = choice in ("codex", "both")
        else:
            click.echo(
                "Error: specify --claude, --codex, or --claude --codex.", err=True
            )
            raise SystemExit(1)

    if claude:
        from clasi.platforms.claude import uninstall as claude_uninstall
        claude_uninstall(target_path)

    if codex:
        from clasi.platforms.codex import uninstall as codex_uninstall
        codex_uninstall(target_path)
```

`_prompt_uninstall(target)` uses `detect_platforms` to determine what is installed,
then prompts similarly to the init interactive path.

**`cli.py`**:

```python
@cli.command()
@click.argument("target", default=".", type=click.Path(exists=True))
@click.option("--claude", "uninstall_claude", is_flag=True, default=False)
@click.option("--codex", "uninstall_codex", is_flag=True, default=False)
def uninstall(target, uninstall_claude, uninstall_codex):
    """Remove CLASI-managed platform integration files."""
    from clasi.uninstall_command import run_uninstall
    run_uninstall(target, claude=uninstall_claude, codex=uninstall_codex)
```

### Testing plan

Use `tmp_path` and install both platforms before each test, then run uninstall to verify
specific files are removed and others are preserved.

```
uv run pytest tests/unit/test_uninstall_command.py -v
uv run pytest -x
```

### Documentation updates

Update `clasi/cli.py` `uninstall` docstring. No external docs required at this stage.
