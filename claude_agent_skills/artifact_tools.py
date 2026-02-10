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
    register_sprint as _register_sprint,
)
from claude_agent_skills.templates import (
    slugify,
    SPRINT_TEMPLATE,
    SPRINT_USECASES_TEMPLATE,
    SPRINT_TECHNICAL_PLAN_TEMPLATE,
    TICKET_TEMPLATE,
    BRIEF_TEMPLATE,
    TECHNICAL_PLAN_TEMPLATE,
    USE_CASES_TEMPLATE,
    OVERVIEW_TEMPLATE,
)


def _plans_dir() -> Path:
    """Return the docs/plans/ directory relative to cwd."""
    return Path.cwd() / "docs" / "plans"


def _sprints_dir() -> Path:
    """Return the docs/plans/sprints/ directory."""
    return _plans_dir() / "sprints"


def resolve_artifact_path(path: str) -> Path:
    """Find a file whether it's in its original location or a done/ subdirectory.

    Resolution order:
    1. Given path as-is
    2. Insert done/ before the filename (e.g., tickets/001.md -> tickets/done/001.md)
    3. Remove done/ from the path (e.g., tickets/done/001.md -> tickets/001.md)

    Returns the resolved Path.
    Raises FileNotFoundError if none of the candidates exist.
    """
    p = Path(path)
    if p.exists():
        return p

    # Try inserting done/ before the filename
    with_done = p.parent / "done" / p.name
    if with_done.exists():
        return with_done

    # Try removing done/ from the path
    parts = p.parts
    if "done" in parts:
        without_done = Path(*[part for part in parts if part != "done"])
        if without_done.exists():
            return without_done

    raise FileNotFoundError(
        f"Artifact not found: {path} (also checked done/ variants)"
    )


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
    structure: sprint.md, usecases.md, technical-plan.md,
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
        ("usecases.md", SPRINT_USECASES_TEMPLATE),
        ("technical-plan.md", SPRINT_TECHNICAL_PLAN_TEMPLATE),
    ]:
        path = sprint_dir / name
        path.write_text(template.format(**fmt), encoding="utf-8")
        files[name] = str(path)

    # Register sprint in state database (lazy init)
    try:
        _register_sprint(
            str(_db_path()), sprint_id, slug, f"sprint/{sprint_id}-{slug}"
        )
    except Exception:
        pass  # Graceful degradation if DB fails

    return json.dumps({
        "id": sprint_id,
        "path": str(sprint_dir),
        "branch": f"sprint/{sprint_id}-{slug}",
        "files": files,
        "phase": "planning-docs",
    }, indent=2)


def _check_sprint_phase_for_ticketing(sprint_id: str) -> None:
    """Check that a sprint is in ticketing phase or later.

    Degrades gracefully: if the DB doesn't exist or the sprint isn't
    registered, the check is skipped (backward compatibility).
    """
    db = _db_path()
    if not db.exists():
        return
    try:
        from claude_agent_skills.state_db import PHASES
        state = _get_sprint_state(str(db), sprint_id)
        phase_idx = PHASES.index(state["phase"])
        ticketing_idx = PHASES.index("ticketing")
        if phase_idx < ticketing_idx:
            raise ValueError(
                f"Cannot create tickets: sprint '{sprint_id}' is in "
                f"'{state['phase']}' phase. Tickets can only be created "
                f"in 'ticketing' phase or later. Complete the review gates first."
            )
    except ValueError as e:
        if "not registered" in str(e):
            return  # Sprint not in DB — allow (backward compat)
        raise


@server.tool()
def create_ticket(sprint_id: str, title: str) -> str:
    """Create a new ticket in a sprint's tickets/ directory.

    Auto-assigns the next ticket number within the sprint.
    Checks sprint phase if the state database exists.

    Args:
        sprint_id: The sprint ID (e.g., '001')
        title: The ticket title
    """
    _check_sprint_phase_for_ticketing(sprint_id)
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
def create_overview() -> str:
    """Create the top-level project overview (docs/plans/overview.md).

    This is the recommended way to start a new project. The overview
    replaces the separate brief, use cases, and technical plan files
    with a single lightweight document. Detailed planning lives in sprints.

    Returns an error if the file already exists.
    """
    path = _plans_dir() / "overview.md"
    if path.exists():
        raise ValueError(f"Overview already exists: {path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(OVERVIEW_TEMPLATE, encoding="utf-8")

    return json.dumps({"path": str(path)}, indent=2)


@server.tool()
def create_brief() -> str:
    """Create the top-level project brief (docs/plans/brief.md).

    Deprecated: prefer create_overview() for new projects.

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

    Deprecated: prefer create_overview() for new projects.

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

    Deprecated: prefer create_overview() for new projects.

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

    try:
        ticket_path = resolve_artifact_path(path)
    except FileNotFoundError:
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
    try:
        ticket_path = resolve_artifact_path(path)
    except FileNotFoundError:
        raise ValueError(f"Ticket not found: {path}")

    # If resolved to done/, the parent is already the done dir — go up one more
    tickets_dir = ticket_path.parent
    if tickets_dir.name == "done":
        tickets_dir = tickets_dir.parent
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

    # Update state database: advance to done and release lock
    db = _db_path()
    if db.exists():
        try:
            state = _get_sprint_state(str(db), sprint_id)
            # Advance through closing → done if needed
            from claude_agent_skills.state_db import PHASES
            phase_idx = PHASES.index(state["phase"])
            done_idx = PHASES.index("done")
            while phase_idx < done_idx:
                _advance_phase(str(db), sprint_id)
                phase_idx += 1
            # Release execution lock if held
            if state["lock"]:
                _release_lock(str(db), sprint_id)
        except (ValueError, Exception):
            pass  # Graceful degradation

    # Auto-version after archiving
    version = None
    try:
        from claude_agent_skills.versioning import (
            compute_next_version,
            update_pyproject_version,
            create_version_tag,
        )
        version = compute_next_version()
        pyproject = Path.cwd() / "pyproject.toml"
        if pyproject.exists():
            update_pyproject_version(version, pyproject)
        create_version_tag(version)
    except Exception:
        pass  # Versioning is best-effort

    result = {
        "old_path": str(sprint_dir),
        "new_path": str(new_path),
    }
    if version:
        result["version"] = version
        result["tag"] = f"v{version}"

    return json.dumps(result, indent=2)


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


# --- TODO management tools ---


def _todo_dir() -> Path:
    """Return the docs/plans/todo/ directory."""
    return _plans_dir() / "todo"


@server.tool()
def list_todos() -> str:
    """List all active TODO files.

    Scans docs/plans/todo/*.md (excludes done/ subdirectory).

    Returns JSON array of {filename, title}.
    """
    todo = _todo_dir()
    results = []
    if todo.exists():
        for f in sorted(todo.glob("*.md")):
            title = f.stem
            # Extract title from first # heading
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
            results.append({"filename": f.name, "title": title})
    return json.dumps(results, indent=2)


@server.tool()
def move_todo_to_done(filename: str) -> str:
    """Move a TODO file to the done/ subdirectory.

    Args:
        filename: The TODO filename (e.g., 'my-idea.md')

    Returns JSON with {old_path, new_path}.
    """
    todo = _todo_dir()
    src = todo / filename
    if not src.exists():
        raise ValueError(f"TODO not found: {filename}")

    done = todo / "done"
    done.mkdir(parents=True, exist_ok=True)
    dst = done / filename
    src.rename(dst)

    return json.dumps({
        "old_path": str(src),
        "new_path": str(dst),
    }, indent=2)


# --- Frontmatter tools ---


@server.tool()
def read_artifact_frontmatter(path: str) -> str:
    """Read YAML frontmatter from a file.

    Uses resolve_artifact_path to find files in original or done/ locations.

    Args:
        path: Path to the file

    Returns JSON dict of frontmatter fields.
    """
    try:
        resolved = resolve_artifact_path(path)
    except FileNotFoundError:
        raise ValueError(f"File not found: {path}")

    fm = read_frontmatter(resolved)
    return json.dumps(fm, indent=2)


@server.tool()
def write_artifact_frontmatter(path: str, updates: str) -> str:
    """Update YAML frontmatter on a file, merging with existing fields.

    Uses resolve_artifact_path to find files in original or done/ locations.
    Creates frontmatter on a plain file that has none.

    Args:
        path: Path to the file
        updates: JSON string of fields to merge (e.g., '{"status": "done"}')

    Returns JSON with {path, updated_fields}.
    """
    try:
        resolved = resolve_artifact_path(path)
    except FileNotFoundError:
        raise ValueError(f"File not found: {path}")

    try:
        update_dict = json.loads(updates)
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Invalid JSON for updates: {e}")

    fm = read_frontmatter(resolved)
    fm.update(update_dict)
    write_frontmatter(resolved, fm)

    return json.dumps({
        "path": str(resolved),
        "updated_fields": list(update_dict.keys()),
    }, indent=2)


# --- Versioning tools ---


@server.tool()
def tag_version(major: int = 0) -> str:
    """Compute the next version, update pyproject.toml, and create a git tag.

    Version format: <major>.<YYYYMMDD>.<build>
    Build auto-increments within the same date, resets to 1 on new date.

    Args:
        major: Major version number (default 0)

    Returns JSON with {version, tag}.
    """
    from claude_agent_skills.versioning import (
        compute_next_version,
        update_pyproject_version,
        create_version_tag,
    )

    version = compute_next_version(major)
    pyproject = Path.cwd() / "pyproject.toml"
    if pyproject.exists():
        update_pyproject_version(version, pyproject)
    create_version_tag(version)

    return json.dumps({
        "version": version,
        "tag": f"v{version}",
    }, indent=2)
