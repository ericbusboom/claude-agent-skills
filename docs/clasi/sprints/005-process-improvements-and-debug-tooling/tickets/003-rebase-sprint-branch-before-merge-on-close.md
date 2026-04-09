---
id: '003'
title: Rebase Sprint Branch Before Merge on Close
status: done
use-cases:
- SUC-003
depends-on: []
github-issue: ''
todo: plan-rebase-sprint-branch-before-merge-on-close.md
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Rebase Sprint Branch Before Merge on Close

## Description

When closing a sprint, `merge_branch()` merges the sprint branch into master with
`--no-ff`. If master has advanced since the sprint branch was created (e.g. from OOP
fixes or version bumps during planning), the sprint commits appear as a side branch
inside the merge bubble rather than sitting cleanly on top of master.

This ticket inserts a `git rebase main_branch branch_name` step before the checkout and
merge, producing clean linear history inside each sprint's merge bubble. The rebase is
aborted on failure with a descriptive `RuntimeError`. The reported `merge_strategy` in
`artifact_tools.py` is updated to reflect the new two-step process.

## Acceptance Criteria

- [x] `merge_branch()` in `clasi/sprint.py` runs `git rebase main_branch branch_name` before `git checkout main_branch`
- [x] If the rebase fails (non-zero return code), `git rebase --abort` is called and a `RuntimeError` is raised describing the failure
- [x] If the rebase succeeds, the existing checkout + `--no-ff` merge sequence runs unchanged
- [x] `artifact_tools.py` reports `merge_strategy: "rebase + --no-ff"` (was `"--no-ff"`)
- [x] A new unit test in `tests/unit/test_sprint.py` verifies: given master has a commit after branching, `merge_branch()` produces linear sprint commits inside the merge bubble
- [x] Existing `merge_branch()` tests continue to pass (update subprocess mocks as needed to include the rebase call)
- [x] `uv run pytest` passes

## Implementation Plan

### Approach

Insert the rebase `subprocess.run` call after the `is_ancestor` guard and before the
existing `checkout` call. Handle failure by aborting and raising. Update the
`merge_strategy` string. Add a test that uses a real temporary git repo (tmpdir) to
verify the resulting log shape.

### Files to Modify

**`clasi/sprint.py`** — `merge_branch()` method

After the `is_ancestor` block (line ~299) and before the `checkout` `subprocess.run`,
insert:

```python
# Rebase sprint branch onto main before merging.
# Two-argument form: git rebase <upstream> <branch> avoids requiring a checkout first.
rebase = subprocess.run(
    ["git", "rebase", main_branch, branch_name],
    capture_output=True,
    text=True,
)
if rebase.returncode != 0:
    subprocess.run(["git", "rebase", "--abort"], capture_output=True)
    raise RuntimeError(
        f"Rebase of {branch_name} onto {main_branch} failed: "
        f"{rebase.stderr.strip()}"
    )
```

The existing checkout and merge blocks remain unchanged after the inserted rebase.

**`clasi/tools/artifact_tools.py`** — line ~1131

Find the line reporting `merge_strategy` and change the string value from `"--no-ff"`
to `"rebase + --no-ff"`. Read the file first to locate the exact line before editing.

**`tests/unit/test_sprint.py`** — add a new test

Add a test that:
1. Creates a temporary git repo with `git init` and an initial commit (use `tmp_path` fixture)
2. Creates the sprint branch from that commit
3. Checks out master and adds a new commit (simulating divergence during planning)
4. Constructs a `Sprint` object pointing at the temp repo
5. Calls `merge_branch()`
6. Runs `git log --oneline master` and asserts the sprint commit appears between the initial commit and the merge commit (linear, not criss-cross)

Also review existing `merge_branch` tests: if they mock `subprocess.run`, add a mock
for the new rebase call (expected args: `["git", "rebase", main_branch, branch_name]`
with returncode 0).

### Testing Plan

- **New test**: real git repo in `tmp_path`, verifies linear history after merge
- **Existing tests**: update any subprocess mocks that patch the sequence of calls in `merge_branch()` to include the rebase call
- **Verification**: `uv run pytest tests/unit/test_sprint.py -v`

### Documentation Updates

Add a comment in `merge_branch()` above the rebase call explaining the two-argument
rebase idiom, since `git rebase <upstream> <branch>` is less commonly known than
the checked-out-branch form.
