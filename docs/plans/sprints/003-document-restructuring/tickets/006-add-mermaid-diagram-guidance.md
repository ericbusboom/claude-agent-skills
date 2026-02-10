---
id: '006'
title: Add Mermaid diagram guidance
status: in-progress
use-cases:
- SUC-006
depends-on: []
---

# Add Mermaid diagram guidance

## Description

Add guidance to instructions on when and how to include Mermaid diagrams in
technical plans. Update `skills/create-technical-plan.md` to reference the
guidance.

### Guidance content

**When to use diagrams:**
- Subsystem/component interaction diagrams (flowchart or C4-style)
- Module dependency diagrams
- Data flow diagrams for complex pipelines

**When NOT to use diagrams:**
- Swim lane diagrams unless multi-system sequencing
- Exhaustive class diagrams (too detailed, go stale quickly)
- Diagrams that just restate the text

**Best practices:**
- Diagrams show target state at sprint end
- Keep diagrams small (5-10 nodes max)
- Use Mermaid syntax (renders in GitHub, VS Code, etc.)

## Acceptance Criteria

- [x] Mermaid diagram guidance added to instructions (in SE instructions or
      as a section in coding-standards)
- [x] Guidance covers when to use and when not to use diagrams
- [x] Covers subsystem interaction and module dependency diagram types
- [x] `skills/create-technical-plan.md` references the guidance
