# Use Case Traceability

Sprint 002 exposed a traceability gap: the sprint frontmatter references
top-level use cases (UC-004, UC-009, UC-010) but there is no documented
mapping from sprint-level use cases (SUC-xxx) to those top-level IDs. You
cannot tell which sprint use case satisfies which project-level use case.

Fixes needed:

1. Sprint use cases (SUC-xxx) should explicitly reference the top-level
   use case(s) they derive from. Add a `parent: UC-xxx` field to each
   sprint use case.

2. The sprint.md `use-cases` field should reference top-level use cases
   that the sprint as a whole addresses. Each SUC within the sprint should
   then trace to one or more of those.

3. The project-status skill should be able to report traceability coverage:
   which top-level use cases are covered by completed sprints, which are
   not yet addressed.

Note: this interacts with the "rename use cases to scenarios" TODO. Whatever
we call them, the traceability chain needs to be explicit.
