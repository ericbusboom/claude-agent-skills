---
name: git-workflow
description: Instructions for how agents interact with git during ticket execution — commits, messages, branches, and safety rules
---

# Git Workflow

## Core Rule

All work must be committed to git. Code that exists only in a conversation
context can be lost when the session ends. Commit early, commit with purpose.

## When to Commit

- **At ticket completion** (required): Before marking a ticket done, commit
  all changes from that ticket. This is the minimum.
- **At significant milestones** (recommended): If a ticket involves multiple
  substantial steps (e.g., implementing a module, then writing its tests),
  commit after each milestone. This protects against context window loss.
- **Never commit broken code**: All tests must pass before committing. If
  tests are failing, fix them first.

## Commit Message Format

Use conventional-style messages that reference the ticket ID:

```
<type>: <short summary> (#NNN)

<optional body explaining why, not what>
```

**Types**:
- `feat` — New feature or capability
- `fix` — Bug fix
- `refactor` — Code restructuring without behavior change
- `docs` — Documentation only
- `test` — Adding or updating tests
- `chore` — Maintenance tasks (deps, config, tooling)

**Examples**:
```
feat: add user authentication endpoint (#003)
fix: handle empty input in parser (#007)
docs: update technical plan for new scope (#010)
test: add golden file tests for report generator (#005)
chore: update dependencies to latest versions (#012)
```

The ticket ID in parentheses makes commits traceable to their tickets.

## Branch Strategy

This is a project-level decision. Two common approaches:

### Option A: Work on Main (Default for Solo Projects)

Commit directly to the main branch. Simple, no merge overhead. Appropriate
when there is one developer or one AI agent working at a time.

### Option B: Feature Branches (Default for Team Projects)

Create a branch per ticket:

```
git checkout -b ticket/NNN-slug
```

Merge back to main when the ticket is complete. Use this when multiple
people or agents work in parallel, or when you want PR-based review.

Choose one approach and document it in the project's README or contributing
guide. If no choice is documented, default to working on main.

## Safety Rules

- **Never force-push** unless explicitly instructed by the human.
- **Never skip hooks** (`--no-verify`) unless explicitly instructed.
- **Never rewrite published history** (amend, rebase on pushed commits).
- **Never commit secrets** (.env files, API keys, credentials). Check
  `.gitignore` before committing.
- **Always check `git status`** before committing to avoid including
  unintended files.

## Relationship to Tickets

- A ticket is not done until its changes are committed.
- The commit message must reference the ticket ID.
- If a ticket requires multiple commits (milestones), each commit should
  reference the same ticket ID.
- When completing a ticket, the final commit should include the ticket file
  move to `done/` and any frontmatter updates.
