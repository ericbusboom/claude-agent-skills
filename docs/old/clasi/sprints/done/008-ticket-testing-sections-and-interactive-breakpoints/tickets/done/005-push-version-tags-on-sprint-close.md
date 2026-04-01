---
id: '005'
title: Push version tags on sprint close
status: done
use-cases:
- UC-013
depends-on: []
---

# Push version tags on sprint close

## Description

The `close-sprint` skill's step 7 commits the version bump and archive,
but never pushes the git tag. Since `git push` doesn't push tags by
default, version tags created by `tag_version` stay local and are lost
if the local repo is cleaned up. Add a step to push tags after the
commit.

## Acceptance Criteria

- [ ] `close-sprint.md` includes a step to push tags (e.g., `git push --tags`)
- [ ] The push-tags step comes after the commit step and before branch
      deletion

## Testing

- **Existing tests to run**: `uv run pytest` (full suite)
- **New tests to write**: None (content-only markdown change)
- **Verification command**: `uv run pytest`
