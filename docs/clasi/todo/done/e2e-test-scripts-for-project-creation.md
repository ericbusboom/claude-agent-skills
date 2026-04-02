---
status: done
sprint: '001'
tickets:
- '001'
---

# E2E Test Scripts for Project Creation via Claude Code

Create test scripts in `tests/e2e/` that automate the end-to-end workflow of:

1. **Project creation** — Kick off creating a new project in `tests/e2e/` using the CLASI project initiation process, driven by the project specification.
2. **Claude Code instance** — Spin up a Claude Code instance (CLI or SDK) that runs the project based on the specification, exercising the SE process from init through execution.

The scripts should cover the full lifecycle: project setup, specification ingestion, and validating that the generated artifacts match expectations.
