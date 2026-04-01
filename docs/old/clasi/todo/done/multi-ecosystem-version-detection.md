---
status: done
sprint: '010'
consumed-by: sprint-010
---

# Multi-Ecosystem Version Detection

## Problem

The `tag_version` MCP tool currently hardcodes version bumping to
`pyproject.toml`. When CLASI is used in non-Python projects (e.g.,
JavaScript/Node), there's no mechanism to detect or update the correct
version file.

## Proposed Solution

Auto-detect the project's version file by checking for known markers in
priority order:

1. `pyproject.toml` — Python projects (current behavior)
2. `package.json` — JavaScript/Node projects
3. `Cargo.toml` — Rust projects
4. `go.mod` — Go projects (version via git tags only, no file to update)
5. Other ecosystems as needed

The version tool should:

- Scan the project root for recognized version files
- Read the current version from the detected file
- Write the new version back to the same file
- Fall back to git-tag-only if no version file is found

## Notes

- Some projects have multiple version files (e.g., `pyproject.toml` +
  `package.json` in a monorepo). Need a strategy for that — maybe a
  config option or convention.
- The `<major>.<YYYYMMDD>.<build>` format may not suit all ecosystems
  (e.g., npm expects semver). May need ecosystem-aware formatting.
