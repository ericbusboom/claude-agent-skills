# MCP Frontmatter Tools and Transparent done/ Path Resolution

Two related improvements to the MCP tool layer.

## 1. Frontmatter read/write MCP tools

Add MCP tools that let agents read and write YAML frontmatter on any
document without having to parse the file format themselves.

- `read_frontmatter(path)` — Returns the frontmatter dict as JSON for
  the given file.
- `write_frontmatter(path, updates)` — Merges the given key-value pairs
  into the file's existing frontmatter. Creates frontmatter if none exists.

The `frontmatter.py` module already has `read_frontmatter` and
`write_frontmatter` functions — these MCP tools would be thin wrappers.

## 2. Transparent done/ path resolution

When an MCP tool receives a path to a ticket, sprint, or TODO file, it
should find the file even if it has been moved to a `done/` subdirectory.
Currently, if you reference `tickets/003-add-auth.md` after it was moved
to `tickets/done/003-add-auth.md`, the tool fails with "not found."

The fix: implement a path resolution function used by all file-accepting
MCP tools. The function should:

1. Check the given path first.
2. If not found, check if inserting `/done/` before the filename finds it.
3. If not found, check if removing `/done/` from the path finds it.
4. Return the resolved path, or raise an error if neither location works.

This should be a single shared function (e.g., `resolve_artifact_path`)
used consistently across `artifact_tools.py` and any other MCP tools that
accept file paths. This way agents can reference artifacts by their
original path regardless of completion status.
