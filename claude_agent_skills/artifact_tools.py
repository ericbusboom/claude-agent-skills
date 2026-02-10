"""Artifact Management tools for the CLASI MCP server.

Read-write tools for creating, querying, and updating SE artifacts
(sprints, tickets, briefs, technical plans, use cases).
"""

import json
import shutil
from pathlib import Path
from typing import Optional

from claude_agent_skills.frontmatter import read_frontmatter, write_frontmatter
from claude_agent_skills.mcp_server import server
from claude_agent_skills.state_db import (
    advance_phase as _advance_phase,
    record_gate as _record_gate,
    acquire_lock as _acquire_lock,
    release_lock as _release_lock,
    get_sprint_state as _get_sprint_state,
)
from claude_agent_skills.templates import (
    slugify,
    SPRINT_TEMPLATE,
    SPRINT_BRIEF_TEMPLATE,
    SPRINT_USECASES_TEMPLATE,
    SPRINT_TECHNICAL_PLAN_TEMPLATE,
    TICKET_TEMPLATE,
    BRIEF_TEMPLATE,
    TECHNICAL_PLAN_TEMPLATE,
    USE_CASES_TEMPLATE,
)


def _plans_dir() -> Path:
    """Return the docs/plans/ directory relative to cwd."""
    return Path.cwd() / "docs" / "plans"


def _sprints_dir() -> Path:
    """Return the docs/plans/sprints/ directory."""
    return _plans_dir() / "sprints"


def _find_sprint_dir(sprint_id: str) -> Path:
    """Find a sprint directory by its ID (checks active and done)."""
    sprints = _sprints_dir()
    # Check active sprints
    for d in sorted(sprints.iterdir()) if sprints.exists() else []:
        if d.is_dir() and d.name.startswith(sprint_id):
            fm = read_frontmatter(d / "sprint.md") if (d / "sprint.md").exists() else {}
            if fm.get("id") == sprint_id:
                return d
    # Check done sprints
    done_dir = sprints / "done"
    for d in sorted(done_dir.iterdir()) if done_dir.exists() else []:
        if d.is_dir() and d.name.startswith(sprint_id):
            fm = read_frontmatter(d / "sprint.md") if (d / "sprint.md").exists() else {}
            if fm.get("id") == sprint_id:
                return d
    raise ValueError(f"Sprint '{sprint_id}' not found")


def _next_sprint_id() -> str:
    """Determine the next sprint number (NNN format)."""
    sprints = _sprints_dir()
    max_id = 0
    for location in [sprints, sprints / "done"]:
        if not location.exists():
            continue
        for d in location.iterdir():
            if d.is_dir() and (d / "sprint.md").exists():
                fm = read_frontmatter(d / "sprint.md")
                try:
                    num = int(fm.get("id", "0"))
                    max_id = max(max_id, num)
                except (ValueError, TypeError):
                    pass
    return f"{max_id + 1:03d}"


def _next_ticket_id(sprint_dir: Path) -> str:
    """Determine the next ticket number within a sprint."""
    tickets_dir = sprint_dir / "tickets"
    max_id = 0
    for location in [tickets_dir, tickets_dir / "done"]:
        if not location.exists():
            continue
        for f in location.glob("*.md"):
            fm = read_frontmatter(f)
            try:
                num = int(fm.get("id", "0"))
                max_id = max(max_id, num)
            except (ValueError, TypeError):
                pass
    return f"{max_id + 1:03d}"


# --- Create tools (ticket 008) ---


@server.tool()
def create_sprint(title: str) -> str:
    """Create a new sprint directory with template planning documents.

    Auto-assigns the next sprint number and creates the full directory
    structure: sprint.md, brief.md, usecases.md, technical-plan.md,
    and tickets/ + tickets/done/ directories.

    Args:
        title: The sprint title (e.g., 'MCP Server Implementation')
    """
    sprint_id = _next_sprint_id()
    slug = slugify(title)
    sprint_dir = _sprints_dir() / f"{sprint_id}-{slug}"

    if sprint_dir.exists():
        raise ValueError(f"Sprint directory already exists: {sprint_dir}")

    sprint_dir.mkdir(parents=True, exist_ok=True)
    (sprint_dir / "tickets").mkdir()
    (sprint_dir / "tickets" / "done").mkdir()

    fmt = {"id": sprint_id, "title": title, "slug": slug}

    files = {}
    for name, template in [
        ("sprint.md", SPRINT_TEMPLATE),
        ("brief.md", SPRINT_BRIEF_TEMPLATE),
        ("usecases.md", SPRINT_USECASES_TEMPLATE),
        ("technical-plan.md", SPRINT_TECHNICAL_PLAN_TEMPLATE),
    ]:
        path = sprint_dir / name
        path.write_text(template.format(**fmt), encoding="utf-8")
        files[name] = str(path)

    return json.dumps({
        "id": sprint_id,
        "path": str(sprint_dir),
        "branch": f"sprint/{sprint_id}-{slug}",
        "files": files,
    }, indent=2)


@server.tool()
def create_ticket(sprint_id: str, title: str) -> str:
    """Create a new ticket in a sprint's tickets/ directory.

    Auto-assigns the next ticket number within the sprint.

    Args:
        sprint_id: The sprint ID (e.g., '001')
        title: The ticket title
    """
    sprint_dir = _find_sprint_dir(sprint_id)
    ticket_id = _next_ticket_id(sprint_dir)
    slug = slugify(title)
    tickets_dir = sprint_dir / "tickets"
    tickets_dir.mkdir(parents=True, exist_ok=True)

    path = tickets_dir / f"{ticket_id}-{slug}.md"
    if path.exists():
        raise ValueError(f"Ticket file already exists: {path}")

    content = TICKET_TEMPLATE.format(id=ticket_id, title=title)
    path.write_text(content, encoding="utf-8")

    return json.dumps({
        "id": ticket_id,
        "path": str(path),
        "template_content": content,
    }, indent=2)


@server.tool()
def create_brief() -> str:
    """Create the top-level project brief (docs/plans/brief.md).

    Returns an error if the file already exists.
    """
    path = _plans_dir() / "brief.md"
    if path.exists():
        raise ValueError(f"Brief already exists: {path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(BRIEF_TEMPLATE, encoding="utf-8")

    return json.dumps({"path": str(path)}, indent=2)


@server.tool()
def create_technical_plan() -> str:
    """Create the top-level technical plan (docs/plans/technical-plan.md).

    Returns an error if the file already exists.
    """
    path = _plans_dir() / "technical-plan.md"
    if path.exists():
        raise ValueError(f"Technical plan already exists: {path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TECHNICAL_PLAN_TEMPLATE, encoding="utf-8")

    return json.dumps({"path": str(path)}, indent=2)


@server.tool()
def create_use_cases() -> str:
    """Create the top-level use cases file (docs/plans/usecases.md).

    Returns an error if the file already exists.
    """
    path = _plans_dir() / "usecases.md"
    if path.exists():
        raise ValueError(f"Use cases file already exists: {path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(USE_CASES_TEMPLATE, encoding="utf-8")

    return json.dumps({"path": str(path)}, indent=2)


# --- Query tools (ticket 009) ---


@server.tool()
def list_sprints(status: Optional[str] = None) -> str:
    """List all sprints with their metadata.

    Args:
        status: Optional filter by status (planning, active, done)

    Returns JSON array of {id, title, status, path, branch}.
    """
    results = []
    sprints = _sprints_dir()

    for location in [sprints, sprints / "done"]:
        if not location.exists():
            continue
        for d in sorted(location.iterdir()):
            sprint_file = d / "sprint.md"
            if not d.is_dir() or not sprint_file.exists():
                continue
            fm = read_frontmatter(sprint_file)
            sprint_status = fm.get("status", "unknown")
            if status and sprint_status != status:
                continue
            results.append({
                "id": fm.get("id", ""),
                "title": fm.get("title", ""),
                "status": sprint_status,
                "path": str(d),
                "branch": fm.get("branch", ""),
            })

    return json.dumps(results, indent=2)


@server.tool()
def list_tickets(sprint_id: Optional[str] = None, status: Optional[str] = None) -> str:
    """List tickets, optionally filtered by sprint and/or status.

    Args:
        sprint_id: Optional sprint ID to filter by
        status: Optional status filter (todo, in-progress, done)

    Returns JSON array of {id, title, status, sprint_id, path}.
    """
    results = []
    sprints = _sprints_dir()

    # Collect sprint directories to scan
    sprint_dirs = []
    if sprint_id:
        try:
            sprint_dirs.append(_find_sprint_dir(sprint_id))
        except ValueError:
            return json.dumps([], indent=2)
    else:
        for location in [sprints, sprints / "done"]:
            if not location.exists():
                continue
            for d in sorted(location.iterdir()):
                if d.is_dir() and (d / "sprint.md").exists():
                    sprint_dirs.append(d)

    for sprint_dir in sprint_dirs:
        sprint_fm = read_frontmatter(sprint_dir / "sprint.md")
        sid = sprint_fm.get("id", "")

        for ticket_location in [sprint_dir / "tickets", sprint_dir / "tickets" / "done"]:
            if not ticket_location.exists():
                continue
            for f in sorted(ticket_location.glob("*.md")):
                fm = read_frontmatter(f)
                if not fm.get("id"):
                    continue
                ticket_status = fm.get("status", "unknown")
                if status and ticket_status != status:
                    continue
                results.append({
                    "id": fm.get("id", ""),
                    "title": fm.get("title", ""),
                    "status": ticket_status,
                    "sprint_id": sid,
                    "path": str(f),
                })

    return json.dumps(results, indent=2)


@server.tool()
def get_sprint_status(sprint_id: str) -> str:
    """Get a summary of a sprint's status including ticket counts.

    Args:
        sprint_id: The sprint ID (e.g., '001')

    Returns JSON with {id, title, status, branch, tickets: {todo, in_progress, done}}.
    """
    sprint_dir = _find_sprint_dir(sprint_id)
    fm = read_frontmatter(sprint_dir / "sprint.md")

    counts = {"todo": 0, "in_progress": 0, "done": 0}
    for ticket_location in [sprint_dir / "tickets", sprint_dir / "tickets" / "done"]:
        if not ticket_location.exists():
            continue
        for f in sorted(ticket_location.glob("*.md")):
            ticket_fm = read_frontmatter(f)
            if not ticket_fm.get("id"):
                continue
            s = ticket_fm.get("status", "todo")
            if s == "in-progress":
                s = "in_progress"
            if s in counts:
                counts[s] += 1

    return json.dumps({
        "id": fm.get("id", ""),
        "title": fm.get("title", ""),
        "status": fm.get("status", ""),
        "branch": fm.get("branch", ""),
        "tickets": counts,
    }, indent=2)


# --- Update tools (ticket 010) ---


@server.tool()
def update_ticket_status(path: str, status: str) -> str:
    """Update a ticket's status in its YAML frontmatter.

    Args:
        path: Path to the ticket file
        status: New status (todo, in-progress, done)

    Returns JSON with {path, old_status, new_status}.
    """
    valid_statuses = {"todo", "in-progress", "done"}
    if status not in valid_statuses:
        raise ValueError(f"Invalid status '{status}'. Must be one of: {', '.join(sorted(valid_statuses))}")

    ticket_path = Path(path)
    if not ticket_path.exists():
        raise ValueError(f"Ticket not found: {path}")

    fm = read_frontmatter(ticket_path)
    old_status = fm.get("status", "unknown")
    fm["status"] = status
    write_frontmatter(ticket_path, fm)

    return json.dumps({
        "path": str(ticket_path),
        "old_status": old_status,
        "new_status": status,
    }, indent=2)


@server.tool()
def move_ticket_to_done(path: str) -> str:
    """Move a ticket (and its plan file if exists) to the sprint's tickets/done/ directory.

    Args:
        path: Path to the ticket file

    Returns JSON with {old_path, new_path}.
    """
    ticket_path = Path(path)
    if not ticket_path.exists():
        raise ValueError(f"Ticket not found: {path}")

    tickets_dir = ticket_path.parent
    done_dir = tickets_dir / "done"
    done_dir.mkdir(parents=True, exist_ok=True)

    new_path = done_dir / ticket_path.name
    ticket_path.rename(new_path)

    result = {"old_path": str(ticket_path), "new_path": str(new_path)}

    # Also move the plan file if it exists
    plan_name = ticket_path.stem + "-plan.md"
    plan_path = tickets_dir / plan_name
    if plan_path.exists():
        new_plan_path = done_dir / plan_name
        plan_path.rename(new_plan_path)
        result["plan_old_path"] = str(plan_path)
        result["plan_new_path"] = str(new_plan_path)

    return json.dumps(result, indent=2)


@server.tool()
def close_sprint(sprint_id: str) -> str:
    """Close a sprint by updating its status and moving it to sprints/done/.

    Args:
        sprint_id: The sprint ID (e.g., '001')

    Returns JSON with {old_path, new_path}.
    """
    sprint_dir = _find_sprint_dir(sprint_id)

    # Update sprint status to done
    sprint_file = sprint_dir / "sprint.md"
    fm = read_frontmatter(sprint_file)
    fm["status"] = "done"
    write_frontmatter(sprint_file, fm)

    # Move to done directory
    done_dir = _sprints_dir() / "done"
    done_dir.mkdir(parents=True, exist_ok=True)
    new_path = done_dir / sprint_dir.name

    if new_path.exists():
        raise ValueError(f"Destination already exists: {new_path}")

    shutil.move(str(sprint_dir), str(new_path))

    return json.dumps({
        "old_path": str(sprint_dir),
        "new_path": str(new_path),
    }, indent=2)


# --- State management tools (ticket 005) ---


def _db_path() -> Path:
    """Return the default state database path."""
    return _plans_dir() / ".clasi.db"


@server.tool()
def get_sprint_phase(sprint_id: str) -> str:
    """Get a sprint's current lifecycle phase and gate status.

    Args:
        sprint_id: The sprint ID (e.g., '002')

    Returns JSON with {id, phase, gates, lock}.
    """
    try:
        state = _get_sprint_state(str(_db_path()), sprint_id)
        return json.dumps(state, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)


@server.tool()
def advance_sprint_phase(sprint_id: str) -> str:
    """Advance a sprint to the next lifecycle phase.

    Validates that exit conditions are met (review gates passed,
    execution lock held, etc.) before allowing the transition.

    Args:
        sprint_id: The sprint ID (e.g., '002')

    Returns JSON with {sprint_id, old_phase, new_phase}.
    """
    try:
        result = _advance_phase(str(_db_path()), sprint_id)
        return json.dumps(result, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)


@server.tool()
def record_gate_result(
    sprint_id: str,
    gate: str,
    result: str,
    notes: Optional[str] = None,
) -> str:
    """Record a review gate result for a sprint.

    Args:
        sprint_id: The sprint ID
        gate: Gate name ('architecture_review' or 'stakeholder_approval')
        result: 'passed' or 'failed'
        notes: Optional notes about the review

    Returns JSON with {sprint_id, gate_name, result, recorded_at}.
    """
    try:
        gate_result = _record_gate(str(_db_path()), sprint_id, gate, result, notes)
        return json.dumps(gate_result, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)


@server.tool()
def acquire_execution_lock(sprint_id: str) -> str:
    """Acquire the execution lock for a sprint.

    Only one sprint can hold the lock at a time. Prevents concurrent
    sprint execution in the same repository.

    Args:
        sprint_id: The sprint ID

    Returns JSON with {sprint_id, acquired_at, reentrant}.
    """
    try:
        lock = _acquire_lock(str(_db_path()), sprint_id)
        return json.dumps(lock, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)


@server.tool()
def release_execution_lock(sprint_id: str) -> str:
    """Release the execution lock held by a sprint.

    Args:
        sprint_id: The sprint ID

    Returns JSON with {sprint_id, released}.
    """
    try:
        result = _release_lock(str(_db_path()), sprint_id)
        return json.dumps(result, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)}, indent=2)
