---
id: "003"
title: Gate recording
status: todo
use-cases:
  - SUC-002
depends-on:
  - "001"
---

# Gate recording

## Description

Add the `record_gate(db_path, sprint_id, gate_name, result, notes=None)`
function to `state_db.py`. This function records the result of a review gate
(architecture review or stakeholder approval) for a sprint.

Gate results are stored in the `sprint_gates` table with a UNIQUE constraint on
`(sprint_id, gate_name)`. This means recording a new result for the same gate
overwrites the previous one (using `INSERT OR REPLACE` or equivalent). This
allows a failed review to be re-attempted after addressing feedback -- the new
result simply replaces the old one.

### Behavior

- Validates that `gate_name` is one of the recognized gates:
  `architecture_review` or `stakeholder_approval`.
- Validates that `result` is either `passed` or `failed`.
- Validates that the sprint exists in the database.
- Records the gate with an ISO 8601 timestamp and optional notes text.
- Returns a dict representing the recorded gate (sprint_id, gate_name, result,
  recorded_at, notes).

The gate results are consumed by `advance_phase` (ticket 002) to determine
whether phase transitions are allowed. For example, the
`architecture-review` -> `stakeholder-review` transition requires the
`architecture_review` gate to have result = `passed`.

## Acceptance Criteria

- [ ] `record_gate(db_path, sprint_id, gate_name, result, notes=None)` is added to `state_db.py`
- [ ] Accepted gate names are `architecture_review` and `stakeholder_approval`; others raise an error
- [ ] Accepted results are `passed` and `failed`; others raise an error
- [ ] Recording a gate for a non-existent sprint raises an error
- [ ] Gate result is stored with an ISO 8601 timestamp
- [ ] Optional `notes` text is stored alongside the result
- [ ] Re-recording the same gate for the same sprint overwrites the previous result (UNIQUE constraint with upsert)
- [ ] Function returns a dict with `sprint_id`, `gate_name`, `result`, `recorded_at`, and `notes`
- [ ] Unit tests cover recording, overwriting, and validation errors
