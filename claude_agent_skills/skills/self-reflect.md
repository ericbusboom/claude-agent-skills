---
name: self-reflect
description: Produces a structured reflection document after a stakeholder correction
---

# Self-Reflect Skill

This skill produces a structured reflection document when the agent makes
an error that the stakeholder corrects. The reflection captures what went
wrong and proposes process improvements.

## Agent Used

**project-manager** (self-analysis)

## Inputs

- The stakeholder's correction or feedback
- Context of what the agent did wrong

## Process

1. **Capture the error**: Describe what action the agent took that was wrong
   or suboptimal. Be specific — cite the skill step, instruction, or decision
   point where the error occurred.

2. **Identify the correct action**: Describe what the agent should have done
   instead, based on the stakeholder's feedback.

3. **Analyze root cause**: Determine why the error happened. Common categories:
   - **Missing instruction**: No rule or skill covers this scenario.
   - **Ambiguous instruction**: The instruction exists but is vague or
     could be interpreted multiple ways.
   - **Ignored instruction**: The instruction exists and is clear, but the
     agent didn't follow it.
   - **Emergent gap**: The process works for known scenarios but doesn't
     cover this edge case.

4. **Propose a fix**: Based on the root cause, suggest one of:
   - New instruction or rule (if missing)
   - Clarified wording for existing instruction (if ambiguous)
   - Stronger emphasis or restructuring (if ignored)
   - New TODO for a future sprint (if it requires code/process changes)

5. **Write reflection**: Create a file at
   `docs/plans/reflections/YYYY-MM-DD-slug.md` with:

   ```yaml
   ---
   date: YYYY-MM-DD
   sprint: NNN (if active)
   category: missing-instruction | ambiguous-instruction | ignored-instruction | emergent-gap
   ---
   ```

   Followed by markdown sections:
   - `## What Happened` — the error
   - `## What Should Have Happened` — the correct behavior
   - `## Root Cause` — analysis with category
   - `## Proposed Fix` — specific actionable recommendation

6. **Create TODO if needed**: If the proposed fix requires code or process
   changes beyond the current session, create a TODO file using the
   `/todo` skill.

## Output

- Reflection document in `docs/plans/reflections/`
- Optional TODO file if process changes are needed
- Acknowledgment to the stakeholder of the correction and proposed fix
