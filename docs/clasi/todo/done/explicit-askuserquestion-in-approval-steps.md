---
status: done
consumed-by: sprint-009
---

# Explicit AskUserQuestion in Approval Steps

## Problem

Several skill steps that require stakeholder approval say "present and wait
for approval" without specifying `AskUserQuestion` as the mechanism. This
leads to the agent presenting text and waiting for a free-form reply instead
of showing a structured UI with clear options.

Other steps in the same skills DO explicitly say `AskUserQuestion`, so the
inconsistency creates ambiguity about which mechanism to use.

## Affected Steps

1. **plan-sprint.md step 10** — "Present the sprint plan and architecture
   review to the stakeholder. Wait for approval." Steps 8 and 9 in the same
   skill explicitly say `AskUserQuestion`, but step 10 doesn't.

2. **project-initiation.md step 5** — "Present the completed overview to
   the stakeholder. If they request changes, revise and re-present. Only
   proceed when approved." Step 2 in the same skill says `AskUserQuestion`,
   but step 5 doesn't.

## Fix

Add explicit `AskUserQuestion` instructions with concrete options to both
steps, matching the pattern used elsewhere in the same skills.
