#!/usr/bin/env python3
"""overpower PostToolUse hook (Edit / Write).

During an autonomous build, an implementer that edits a file *outside the
worktree* has done work that won't be on the feature branch — a silent,
expensive mistake (obra/superpowers #1040, #2166). This hook catches it the
moment it happens and tells Claude, so `autonomous-execution`'s scope-breach
hard stop can fire.

It is a strict no-op unless ALL of these hold:
  - `.overpower/progress.md` exists in the project (an autonomous build is live)
  - that file names a worktree path
  - the edited file is outside both the worktree and the project's own
    `.overpower/` tree

Reads the standard PostToolUse JSON on stdin; prints nothing (allow) or a
`{"decision":"block","reason":...}` object. Any error → allow (never break a
session over the hook).
"""
import json
import re
import sys
from pathlib import Path


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    tool = event.get("tool_name", "")
    if tool not in ("Edit", "Write", "MultiEdit"):
        return 0

    ti = event.get("tool_input", {}) or {}
    target = ti.get("file_path") or ti.get("path")
    if not target:
        return 0

    try:
        project = Path(event.get("cwd") or ".").resolve()
        progress = project / ".overpower" / "progress.md"
        if not progress.exists():
            return 0
        text = progress.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"worktree\s+(\S+)", text)
        if not m:
            return 0
        worktree = (project / m.group(1)).resolve()
        edited = Path(target).resolve()

        def inside(child: Path, parent: Path) -> bool:
            try:
                child.relative_to(parent)
                return True
            except ValueError:
                return False

        if inside(edited, worktree):
            return 0
        if inside(edited, project / ".overpower"):
            return 0  # the orchestrator writing progress/findings is fine
        if inside(edited, worktree.parent) and edited.name in ("progress.md", "findings.md"):
            return 0

        reason = (
            f"overpower scope breach: an edit landed at {edited} — OUTSIDE the "
            f"active worktree {worktree}. Work outside the worktree will not be "
            f"on the feature branch. Per `autonomous-execution`, this is a hard "
            f"stop: revert this edit, and surface to the user which task's "
            f"implementer went out of scope."
        )
        sys.stdout.write(json.dumps({"decision": "block", "reason": reason}))
        return 0
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
