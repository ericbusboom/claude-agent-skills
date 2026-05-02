---
id: '001'
title: 'Package skeleton: pyproject.toml + clasr entry point'
status: done
use-cases:
- SUC-001
depends-on: []
github-issue: ''
todo: clasr-standalone-cross-platform-agent-config-renderer.md
completes_todo: false
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Package skeleton: pyproject.toml + clasr entry point

## Description

Create the `clasr/` Python package alongside the existing `clasi/` package in the same
repository. Update `pyproject.toml` to register the new package and `clasr` CLI entry
point. After this ticket, `pip install -e .` produces a working `clasr --help` command
in addition to `clasi`.

This ticket establishes the skeleton only: `clasr/__init__.py`, `clasr/cli.py` (stub
with `--help` and `--instructions` support), and the necessary `pyproject.toml` changes.
Markdown data files (`instructions.md`, `SCHEMA.md`, `README.md`) are also created here
as stubs.

## Acceptance Criteria

- [x] `clasr/` directory exists with `__init__.py` and `cli.py`
- [x] `clasr/cli.py` has a `main()` function registered as `clasr = clasr.cli:main` in
      `pyproject.toml`
- [x] `clasr --help` works after `pip install -e .` and shows `install`, `uninstall`,
      and `--instructions` in the help text
- [x] `clasr/__init__.py` exports a version string or is importable without error
- [x] `pyproject.toml` includes `clasr*` in `[tool.setuptools.packages.find]` include list
- [x] `pyproject.toml` includes a `[tool.setuptools.package-data]` section for `clasr`
      covering `*.md`
- [x] `clasr/instructions.md`, `clasr/SCHEMA.md`, and `clasr/README.md` exist as stubs
- [x] `tests/clasr/__init__.py` exists (empty, marks test directory)
- [x] `clasr` does NOT import from `clasi` (verify with a grep or import check)
- [x] All existing `clasi` tests pass: `uv run pytest tests/unit/` is green

## Implementation Plan

### Approach

1. Create `clasr/` directory with `__init__.py` (set `__version__ = "0.1.0"` or import
   from package metadata).
2. Create `clasr/cli.py` with `argparse`-based `main()`:
   - Top-level `--instructions` flag: load and print `clasr/instructions.md` via
     `importlib.resources`, then exit.
   - Subcommands: `install` and `uninstall` (stubs that print "not yet implemented").
3. Create stub Markdown files:
   - `clasr/instructions.md`: placeholder text explaining the `asr/` layout
   - `clasr/SCHEMA.md`: placeholder for union frontmatter spec
   - `clasr/README.md`: placeholder overview
4. Update `pyproject.toml`:
   - Add `clasr = "clasr.cli:main"` to `[project.scripts]`
   - Change `include = ["clasi*"]` to `include = ["clasi*", "clasr*"]`
   - Add `[tool.setuptools.package-data]` `clasr = ["*.md"]`
   - Extend `[tool.coverage.run]` source or `addopts` to include `clasr`
5. Create `tests/clasr/__init__.py`.

### Files to Create

- `clasr/__init__.py`
- `clasr/cli.py`
- `clasr/instructions.md` (stub)
- `clasr/SCHEMA.md` (stub)
- `clasr/README.md` (stub)
- `tests/clasr/__init__.py`

### Files to Modify

- `pyproject.toml`

### Testing Plan

- Run `pip install -e . --quiet && clasr --help` and inspect output.
- Run `uv run pytest tests/unit/` to verify no regressions in existing tests.
- No new tests required for the skeleton; test infrastructure is established here.

### Documentation Updates

- `clasr/README.md` stub content should include the one-line description of what clasr is.
