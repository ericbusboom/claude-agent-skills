---
id: "002"
title: "Extend _markers.py with named marker block support"
status: todo
use-cases:
  - SUC-001
  - SUC-008
depends-on: []
github-issue: ""
todo: ""
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Extend _markers.py with named marker block support

## Description

The root `AGENTS.md` needs to carry two independent CLASI-managed blocks: the existing
entry-point block (`<!-- CLASI:START --> ... <!-- CLASI:END -->`) and a new rules block
(`<!-- CLASI:RULES:START --> ... <!-- CLASI:RULES:END -->`). The current `_markers.py`
module only supports a single block per file.

This ticket adds `write_named_section` and `strip_named_section` to `_markers.py`,
supporting any block name. The existing `write_section`/`strip_section` functions are
left unchanged for backward compatibility.

## Acceptance Criteria

- [ ] `_markers.py` exports `write_named_section(file_path, block_name, content)` that
      writes or replaces the block delimited by `<!-- CLASI:{block_name}:START -->` and
      `<!-- CLASI:{block_name}:END -->`.
- [ ] `_markers.py` exports `strip_named_section(file_path, block_name)` that removes
      only the named block, leaving everything else (including other named blocks and
      user content) intact.
- [ ] Round-trip test: a file with user content + CLASI:START/END block + CLASI:RULES:START/END
      block survives:
      - `write_named_section(..., "RULES", ...)` does not touch the CLASI:START/END block.
      - `strip_named_section(..., "RULES")` leaves the CLASI:START/END block and user content
        intact.
      - `strip_named_section(..., "CLASI")` (if tested) would only strip via the existing
        `strip_section`, not via the new API — or the new API also handles this name.
        (Implementation decision: the named API with name="CLASI" should work identically
        to the existing `strip_section`.)
- [ ] If a named block appears twice in the same file (malformed state), `write_named_section`
      replaces from the first START to the first END of that name. Document the behavior.
- [ ] `write_named_section` is idempotent: calling it twice with the same content leaves
      the file unchanged on the second call.
- [ ] All existing tests pass (existing `write_section`/`strip_section` behavior is
      unchanged).

## Implementation Plan

### Approach

Add two functions to `clasi/platforms/_markers.py`:

```python
def write_named_section(file_path: Path, block_name: str, content: str) -> bool:
    """Write or replace the named CLASI block in file_path.

    The block is delimited by:
        <!-- CLASI:{block_name}:START -->
        <!-- CLASI:{block_name}:END -->

    Behavior:
    - Block already present: replace in place.
    - File exists, block absent: append at end.
    - File does not exist: create with just the block.

    Returns True if the file was written/updated, False if unchanged.
    """
    marker_start = f"<!-- CLASI:{block_name}:START -->"
    marker_end = f"<!-- CLASI:{block_name}:END -->"
    section = f"{marker_start}\n{content}\n{marker_end}\n"
    # ... (same structure as write_section)

def strip_named_section(file_path: Path, block_name: str) -> bool:
    """Remove the named CLASI block from file_path, preserving everything else.

    Deletes the file if it becomes empty (only whitespace).

    Returns True if anything was removed, False otherwise.
    """
    marker_start = f"<!-- CLASI:{block_name}:START -->"
    marker_end = f"<!-- CLASI:{block_name}:END -->"
    # ... (same structure as strip_section)
```

The index arithmetic must use `content.index(marker_start)` and
`content.index(marker_end)` relative to `marker_start` to avoid the wrong marker being
matched when two differently-named blocks coexist.

To ensure the END marker of the RULES block is not confused with the END marker of the
CLASI block (they have different text), a simple `str.index` scan works — the markers
are distinct strings.

### Files to modify

- `clasi/platforms/_markers.py` — add `write_named_section`, `strip_named_section`

### Testing plan

Check if `tests/unit/test_markers.py` exists. If not, create it.

New tests to write in `tests/unit/test_markers.py`:

1. `test_write_named_section_creates_file` — file does not exist; write creates it with
   only the named block.
2. `test_write_named_section_replaces_existing_block` — file has existing named block;
   write replaces only that block.
3. `test_write_named_section_appends_to_existing_file` — file exists with user content
   and no named block; write appends the block.
4. `test_write_named_section_idempotent` — calling twice with same content returns False
   on second call (unchanged).
5. `test_strip_named_section_removes_only_target_block` — file has two named blocks
   (CLASI:START/END and CLASI:RULES:START/END) and user content; strip RULES removes
   only the RULES block, leaving CLASI block and user content intact.
6. `test_strip_named_section_does_not_affect_other_blocks` — strip on a name that is
   absent returns False without modifying the file.
7. `test_two_blocks_coexist_round_trip` — write CLASI:START block, write CLASI:RULES
   block, strip CLASI:RULES, verify CLASI:START block still present.

Run: `uv run pytest tests/unit/test_markers.py -v`

### Documentation updates

Add a module-level docstring update noting the named-block API.
