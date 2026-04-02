---
status: done
sprint: '002'
tickets:
- '010'
---

# Sprint Should Own Branch and Worktree Lifecycle

The Sprint class should have the logic for creating and merging a sprint git branch, or using a git worktree. Currently this is scattered across tool code. The Sprint model should own methods like:

- Create the sprint branch
- Merge the sprint branch back to main
- Optionally create/manage a worktree for isolated execution

This keeps git branching strategy as a concern of the Sprint domain object rather than the tool layer.
