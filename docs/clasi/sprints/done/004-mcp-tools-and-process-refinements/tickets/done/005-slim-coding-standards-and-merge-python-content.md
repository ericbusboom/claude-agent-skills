---
id: '005'
title: Slim coding standards and merge Python content
status: done
use-cases:
- SUC-003
depends-on: []
---

# Slim coding standards and merge Python content

## Description

Keep `coding-standards.md` with only language-agnostic principles. Move
Python-specific content into `languages/python.md`.

### Stays in coding-standards.md

- Error handling philosophy (fail fast, be specific, validate at boundaries)
- Dependency management principles (minimize deps, pin to minimum compatible)
- General naming guidance (descriptive names, avoid catch-all modules)

### Moves to languages/python.md

- Project Structure, Logging, Import Ordering, Naming Conventions,
  Type Hints, Code Style (merge with existing sections, no duplication)

### References to update

- `ACTIVITY_GUIDES` in `process_tools.py`
- `instructions/system-engineering.md`

## Acceptance Criteria

- [ ] `coding-standards.md` contains only language-agnostic principles
- [ ] Python-specific content merged into `languages/python.md`
- [ ] No content lost
- [ ] `ACTIVITY_GUIDES` updated
- [ ] All tests pass
