# Ask Open Questions During Sprint Planning

When a sprint's planning documents are finished and the technical plan has
an "Open Questions" section, those questions should be presented to the
stakeholder using Claude Code's `AskUserQuestion` tool (the multi-choice
question UI) rather than left as text in a document.

This should happen at the stakeholder review gate — after the architecture
review passes and before the stakeholder approves. The plan-sprint skill
should:

1. Parse the Open Questions section from the technical plan.
2. For each question, present it via `AskUserQuestion` with the proposed
   options.
3. Record the stakeholder's answers back into the technical plan (replacing
   the open question with the decision).
4. Only then proceed to ask for stakeholder approval.

This ensures open questions are actively resolved rather than silently
carried into implementation.
