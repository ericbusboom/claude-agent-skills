"""Claude Code hook event handlers.

Each handler reads stdin JSON (the hook payload from Claude Code),
performs the appropriate action, and exits with the correct code:
  - exit 0: allow (hook passes)
  - exit 2: block (hook rejects, stderr message fed back to model)

These are thin dispatchers — actual logic lives in dedicated modules.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def handle_hook(event: str) -> None:
    """Dispatch a hook event to the appropriate handler."""
    payload = _read_payload()

    handlers = {
        "role-guard": _handle_role_guard,
        "subagent-start": _handle_subagent_start,
        "subagent-stop": _handle_subagent_stop,
        "task-created": _handle_task_created,
        "task-completed": _handle_task_completed,
    }

    handler = handlers.get(event)
    if handler is None:
        print(f"Unknown hook event: {event}", file=sys.stderr)
        sys.exit(1)

    handler(payload)


def _read_payload() -> dict:
    """Read JSON payload from stdin."""
    try:
        data = sys.stdin.read()
        if not data.strip():
            return {}
        return json.loads(data)
    except (json.JSONDecodeError, OSError):
        return {}


# ---------------------------------------------------------------------------
# Role Guard — PreToolUse hook for Edit/Write/MultiEdit
# ---------------------------------------------------------------------------


def _handle_role_guard(payload: dict) -> None:
    """Enforce directory write scopes based on agent tier.

    Tier 0 (team-lead / interactive session): can write to docs/clasi/,
    .claude/, CLAUDE.md, AGENTS.md.
    Tier 1 (sprint-planner): can write to docs/clasi/sprints/<sprint>/.
    Tier 2 (programmer): can write anywhere within scope_directory.
    """
    tool_input = payload if payload else {}
    file_path = (
        tool_input.get("file_path")
        or tool_input.get("path")
        or tool_input.get("new_path")
        or ""
    )

    if not file_path:
        sys.exit(0)  # Can't determine path, allow

    agent_tier = os.environ.get("CLASI_AGENT_TIER", "")

    # Programmer (tier 2) can write — that's their job
    if agent_tier == "2":
        sys.exit(0)

    # OOP bypass
    if Path(".clasi-oop").exists():
        sys.exit(0)

    # Recovery state bypass
    db_path = Path("docs/clasi/.clasi.db")
    if db_path.exists():
        try:
            from clasi.state_db import get_recovery_state

            recovery = get_recovery_state(str(db_path))
            if recovery and file_path in recovery["allowed_paths"]:
                sys.exit(0)
        except Exception:
            pass

    # Safe prefixes for any tier
    safe_prefixes = [".claude/", "CLAUDE.md", "AGENTS.md"]
    for prefix in safe_prefixes:
        if file_path == prefix or file_path.startswith(prefix):
            sys.exit(0)

    # Team-lead (tier 0 or unset) can write to docs/clasi/
    if agent_tier in ("", "0") and file_path.startswith("docs/clasi/"):
        sys.exit(0)

    # Sprint-planner (tier 1) can write to sprint directories
    if agent_tier == "1" and file_path.startswith("docs/clasi/sprints/"):
        sys.exit(0)

    # Block — determine who's violating
    agent_name = os.environ.get("CLASI_AGENT_NAME", "team-lead")
    print(
        f"CLASI ROLE VIOLATION: {agent_name} (tier {agent_tier or '0'}) "
        f"attempted direct file write to: {file_path}",
        file=sys.stderr,
    )
    print(
        "Dispatch to the appropriate agent for this write:",
        file=sys.stderr,
    )
    if agent_tier == "1":
        print("- programmer agent for source code and tests", file=sys.stderr)
    else:
        print(
            "- sprint-planner agent for sprint/architecture/ticket artifacts",
            file=sys.stderr,
        )
        print("- programmer agent for source code and tests", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# Subagent lifecycle logging — SubagentStart / SubagentStop
# ---------------------------------------------------------------------------


def _handle_subagent_start(payload: dict) -> None:
    """Log when a subagent starts.

    Creates a log entry in docs/clasi/log/ with timestamp, agent info.
    """
    log_dir = Path("docs/clasi/log")
    if not log_dir.exists():
        # No log directory — skip silently (project may not be initialized)
        sys.exit(0)

    agent_type = payload.get("agent_type", "unknown")
    agent_id = payload.get("agent_id", "")
    session_id = payload.get("session_id", "")
    timestamp = datetime.now(timezone.utc).isoformat()

    # Write a start marker file that subagent-stop can find
    marker_dir = log_dir / ".active"
    marker_dir.mkdir(parents=True, exist_ok=True)

    marker_id = agent_id or session_id or "unknown"
    marker = marker_dir / f"{marker_id}.json"
    marker.write_text(
        json.dumps(
            {
                "agent_type": agent_type,
                "agent_id": agent_id,
                "session_id": session_id,
                "started_at": timestamp,
            },
            indent=2,
        )
    )

    sys.exit(0)


def _handle_subagent_stop(payload: dict) -> None:
    """Log when a subagent finishes.

    Reads the start marker, computes duration, writes a log entry.
    """
    log_dir = Path("docs/clasi/log")
    if not log_dir.exists():
        sys.exit(0)

    agent_type = payload.get("agent_type", "unknown")
    agent_id = payload.get("agent_id", "")
    session_id = payload.get("session_id", "")
    stop_time = datetime.now(timezone.utc)

    # Find and read start marker
    marker_dir = log_dir / ".active"
    marker_id = agent_id or session_id or "unknown"
    marker = marker_dir / f"{marker_id}.json"

    start_info = {}
    duration_s = None
    if marker.exists():
        try:
            start_info = json.loads(marker.read_text())
            started_at = datetime.fromisoformat(start_info["started_at"])
            duration_s = (stop_time - started_at).total_seconds()
        except (json.JSONDecodeError, KeyError, ValueError):
            pass
        marker.unlink(missing_ok=True)

    # Write log entry
    _next = _next_log_number(log_dir)
    log_file = log_dir / f"{_next:03d}-{agent_type}.md"

    lines = [
        "---",
        f"agent_type: {agent_type}",
        f"agent_id: {agent_id}",
        f"started_at: {start_info.get('started_at', 'unknown')}",
        f"stopped_at: {stop_time.isoformat()}",
    ]
    if duration_s is not None:
        lines.append(f"duration_seconds: {duration_s:.1f}")
    lines.extend(["---", "", f"# Subagent: {agent_type}", ""])

    log_file.write_text("\n".join(lines))
    sys.exit(0)


# ---------------------------------------------------------------------------
# Task lifecycle — TaskCreated / TaskCompleted
# ---------------------------------------------------------------------------


def _handle_task_created(payload: dict) -> None:
    """Validate a task creation.

    Checks that the referenced ticket exists and is in the right state.
    For now, this is permissive — log and allow.
    """
    # TODO: validate ticket exists, sprint is in executing phase
    sys.exit(0)


def _handle_task_completed(payload: dict) -> None:
    """Validate task completion.

    Checks tests pass, acceptance criteria met, updates ticket frontmatter.
    For now, this is permissive — log and allow.

    Future: run tests, check criteria, merge worktree, block on failure.
    """
    # TODO: run tests, validate criteria, merge worktree
    sys.exit(0)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _next_log_number(log_dir: Path) -> int:
    """Find the next sequential log number in a directory."""
    existing = sorted(log_dir.glob("[0-9][0-9][0-9]-*.md"))
    if not existing:
        return 1
    try:
        last = int(existing[-1].name[:3])
        return last + 1
    except (ValueError, IndexError):
        return 1
