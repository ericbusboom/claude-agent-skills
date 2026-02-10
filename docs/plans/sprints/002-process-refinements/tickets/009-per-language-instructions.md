---
id: "009"
title: Create per-language instruction directory
status: todo
use-cases: [SUC-008]
depends-on: []
---

# Create Per-Language Instruction Directory

## Description

Create `instructions/languages/` as a subdirectory for language-specific
(or environment-specific) coding conventions. Each language gets one
markdown file with frontmatter. Start with Python as the first language.

These complement the general `coding-standards.md` — they do not
duplicate it. The general file covers universal conventions (naming,
imports, error handling). Language files cover language-specific patterns.

## Changes Required

1. Create `instructions/languages/python.md`:
   - Frontmatter: `name: Python`, `description: Python-specific coding
     conventions`
   - Content: Python-specific patterns beyond what's in coding-standards.md
     - Virtual environment conventions
     - `pyproject.toml` vs `setup.py` preferences
     - Type hint patterns (Protocol, TypeVar, generics)
     - Pytest-specific patterns (fixtures, parametrize, conftest)
     - Common Python idioms (context managers, generators, dataclasses)
     - Python-specific anti-patterns to avoid

2. Update `instructions/system-engineering.md`:
   - Add a note about per-language instructions in the directory layout
   - Reference `instructions/languages/` in the instructions section

3. Update `instructions/coding-standards.md`:
   - Add a note pointing to `instructions/languages/` for
     language-specific conventions

## Acceptance Criteria

- [ ] `instructions/languages/python.md` exists with frontmatter
- [ ] Content covers Python-specific conventions not in coding-standards.md
- [ ] SE instructions reference the per-language directory
- [ ] Coding standards reference the per-language directory
- [ ] File follows the same frontmatter format as other instructions
