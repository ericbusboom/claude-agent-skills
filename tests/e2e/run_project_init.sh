#!/usr/bin/env bash
# run_project_init.sh — Bootstrap a test project and run CLASI project initiation via Claude Code.
#
# Usage:
#   ./tests/e2e/run_project_init.sh [target-dir]
#
# If no target directory is given, uses tests/e2e/project/.
#
# Steps:
#   1. Runs setup_project.py to create the project directory, init CLASI + git, copy spec.
#   2. Invokes Claude Code in print mode to run /se init, using the guessing-game spec
#      as the stakeholder specification.
#
# Prerequisites:
#   - Python 3.10+ with `clasi` installed (for setup_project.py)
#   - `claude` CLI available on PATH
#   - ANTHROPIC_API_KEY set (or Claude Code otherwise authenticated)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET="${1:-$SCRIPT_DIR/project}"

echo "=== E2E: Project Initialization ==="
echo "Target: $TARGET"
echo ""

# Step 1: Bootstrap the project directory
echo "[1/2] Running setup_project.py ..."
python "$SCRIPT_DIR/setup_project.py" "$TARGET"
echo ""

# Step 2: Invoke Claude Code to run project initiation
echo "[2/2] Running Claude Code project initiation ..."
SPEC_CONTENT="$(cat "$SCRIPT_DIR/guessing-game-spec.md")"

cd "$TARGET"
claude -p \
  --dangerously-skip-permissions \
  --output-format text \
  --max-budget-usd 5.00 \
  "Run /se init to initialize this project. Use the following specification as the stakeholder input. Do not ask clarifying questions — accept the spec as-is and produce the overview, specification, and use-case artifacts.

Specification:
$SPEC_CONTENT"

echo ""
echo "=== E2E: Project initialization complete ==="
echo "Check $TARGET/docs/clasi/ for generated artifacts."
