---
status: pending
---

# Ensure CLAUDE.md Identifies Agent as Main Controller

## Problem

The top-level Claude session does not know it IS the main-controller.
CLAUDE.md and AGENTS.md describe the process but never say "you are
the main-controller, you dispatch, you do not write files directly."
This was documented in reflection 2026-03-19-main-controller-not-dispatching.md.

## Changes Needed

1. **CLAUDE.md** — Add a section (inside the CLASI block) that says:
   "When you start a session in this project, you are the main-controller.
   Your role is to dispatch to subagents. You do not write code,
   documentation, or planning artifacts directly. See the main-controller
   agent definition for your full role description."

2. **AGENTS.md** — Ensure it has an `@CLAUDE.md` reference so agents
   loaded from AGENTS.md also see the CLAUDE.md identity binding.
   (Currently CLAUDE.md has `@AGENTS.md` but not the reverse.)
