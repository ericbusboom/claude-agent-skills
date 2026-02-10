---
id: "004"
title: Create project-manager orchestrator agent
status: done
use-cases: [UC-001, UC-004]
depends-on: ["002", "003"]
---

# 004: Create Project-Manager Orchestrator Agent

## Description

Create `agents/project-manager.md` defining a top-level orchestrator that
drives projects through the full SE process by delegating to specialized
agents. Does not implement — only orchestrates.

## Acceptance Criteria

- [x] `agents/project-manager.md` exists with YAML frontmatter
- [x] Defines delegation map: which agent handles which phase
- [x] Describes how to determine current project state from artifacts
- [x] Describes the ticket execution loop
