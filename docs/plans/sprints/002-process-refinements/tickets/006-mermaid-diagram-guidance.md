---
id: "006"
title: Add Mermaid diagram guidance
status: todo
use-cases: [SUC-007]
depends-on: []
---

# Add Mermaid Diagram Guidance

## Description

Add guidance to instructions on when and how to include Mermaid diagrams
in technical plans. The guidance should encourage useful diagrams
(subsystem interaction, module dependencies) while discouraging
unnecessary ones (exhaustive class diagrams, trivial flow charts).

## Changes Required

1. Update `instructions/system-engineering.md` or create a section in
   the technical plan workflow:
   - When to create diagrams (technical plans, architecture notes)
   - What to diagram:
     - Subsystem interactions and communication
     - Module dependencies within subsystems
     - Data flow between components
   - What NOT to diagram:
     - Swim lane diagrams (unless truly multi-system sequencing)
     - Exhaustive class diagrams listing all classes
     - Trivial sequential flows
   - Diagrams should show the system as it will exist at the end of the
     sprint (target state, not current state)
   - Level of detail: subsystems and their interfaces, not individual
     classes (unless the system is small and classes are the subsystems)

2. Update `skills/create-technical-plan.md`:
   - Add a step to include Mermaid diagrams for subsystem interactions
   - Reference the diagram guidance

## Acceptance Criteria

- [ ] Instructions include Mermaid diagram guidance section
- [ ] Guidance specifies what to diagram (subsystem interaction, module
      dependencies)
- [ ] Guidance specifies what NOT to diagram (swim lanes, exhaustive
      class diagrams)
- [ ] Guidance says diagrams show target state at sprint end
- [ ] Guidance addresses appropriate level of detail
- [ ] create-technical-plan skill references diagram guidance
