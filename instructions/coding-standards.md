---
name: coding-standards
description: Shared coding conventions for project structure, error handling, logging, imports, and configuration
---

# Coding Standards

These conventions apply to all code written in this project. Dev agents
(python-expert and others) must follow these standards.



## Error Handling

- **Fail fast**: Raise exceptions at the point of failure rather than
  returning error codes or None.
- **Be specific**: Raise `ValueError`, `FileNotFoundError`, `TypeError`,
  etc. — not bare `Exception`.
- **Only catch what you handle**: Do not catch exceptions just to log and
  re-raise. Only catch when you can actually recover or add meaningful
  context.
- **Validate at boundaries**: Validate inputs at public function boundaries
  (user input, file I/O, external APIs). Internal functions can trust their
  callers.
- **No silent failures**: Never use bare `except:` or `except Exception: pass`.

```python
# Good — specific, at the boundary
def load_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    return json.loads(path.read_text())

# Bad — silent, generic
def load_config(path):
    try:
        return json.loads(open(path).read())
    except:
        return {}
```

## Logging

- Use the standard library `logging` module, not `print()` for operational
  messages.
- Get a logger per module: `logger = logging.getLogger(__name__)`
- Use appropriate levels:
  - `DEBUG` — Detailed diagnostic info (variable values, flow tracing)
  - `INFO` — Normal operation milestones (started, completed, loaded N items)
  - `WARNING` — Something unexpected but recoverable
  - `ERROR` — Something failed but the program continues
  - `CRITICAL` — Program cannot continue
- Keep `print()` only for user-facing CLI output, not for debugging or
  diagnostics.

## Import Ordering

Follow PEP 8 import ordering with blank lines between groups:

```python
# 1. Standard library
import os
import sys
from pathlib import Path

# 2. Third-party packages
import requests
from pydantic import BaseModel

# 3. Local/project imports
from .link_agents import get_repo_root
```

- Use absolute imports for top-level modules.
- Use relative imports within a package only when referring to siblings.
- Never use wildcard imports (`from module import *`).
- Sort imports alphabetically within each group.

## Dependency Management

- Declare all dependencies in `pyproject.toml` under `[project.dependencies]`.
- Pin to minimum compatible versions, not exact versions:
  `requests >= 2.28` not `requests == 2.28.1`.
- Minimize dependencies. Prefer the standard library when it's adequate.
- Never add a dependency for something trivially implementable (e.g., don't
  add a package just to flatten a list).

## Naming Conventions

- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions and variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: `_leading_underscore`
- Names should be descriptive. Avoid single-letter variables except in
  comprehensions and short lambdas (`i`, `x`, `k`, `v` are fine there).

## Type Hints

- Add type hints to all public function signatures.
- Use `from __future__ import annotations` for modern syntax in Python 3.7+.
- Use `Path` not `str` for file paths.
- Use `| None` (or `Optional[X]`) when a value can be None.
- Internal helper functions do not require type hints but benefit from them.

## Code Style

- Follow PEP 8.
- Maximum line length: 88 characters (Black default).
- Prefer f-strings over `.format()` or `%` formatting.
- Prefer `pathlib.Path` over `os.path`.
- Prefer list/dict/set comprehensions over `map()`/`filter()` for simple
  transformations.
- Keep functions short — if a function exceeds 30 lines, consider splitting.
- One return type per function. Avoid functions that sometimes return a value
  and sometimes return None unless the signature explicitly says so.
