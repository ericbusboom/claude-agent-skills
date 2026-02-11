---
name: create-technical-plan
description: Produces a technical plan from a brief and use cases, covering architecture, components, and design decisions
---

# Create Technical Plan Skill

This skill produces a technical plan from a completed brief and use cases
using the architect agent.

## Agent Used

**architect**

## Inputs

- `docs/plans/brief.md` (must exist)
- `docs/plans/usecases.md` (must exist)

## Process

1. **Read artifacts**: Read the brief and use cases.
2. **Analyze requirements**: Identify constraints, technology needs, and
   key design decisions from the brief and use cases.
3. **Design architecture**: Determine components, technology stack, data
   model, APIs, deployment strategy, and security considerations.
4. **Write technical plan**: Produce `docs/plans/technical-plan.md` with
   all sections. Each component must list which use cases it addresses.
   Include Mermaid diagrams where they clarify structure (see "Diagrams in
   Technical Plans" in `instructions/software-engineering.md`).
5. **Verify traceability**: Every component addresses at least one use case.
   Every use case is addressed by at least one component.
6. **Flag open questions**: Anything ambiguous or requiring a decision is
   listed explicitly rather than assumed.

## Output

- `docs/plans/technical-plan.md` (created or updated)
