#!/usr/bin/env python3
"""overpower session-start hook.

Injects the `using-overpower` skill in full at session start / clear / compact,
so the tier routing is in context from the first message and again after every
compaction.

Emits the context in whichever shape the running harness consumes, detected
from its environment:
  - Claude Code (CLAUDE_PLUGIN_ROOT, no COPILOT_CLI): hookSpecificOutput.additionalContext
  - Cursor (CURSOR_* set): additional_context (snake_case)
  - anything else / SDK standard: additionalContext (top-level)

Builds JSON with json.dumps (no hand escaping), self-locates via __file__
(works even if the plugin-root variable wasn't substituted), and prints nothing
on any error so a broken hook can never break a session.
"""
import json
import os
import sys
from pathlib import Path


def build_context() -> str | None:
    try:
        plugin_root = Path(__file__).resolve().parent.parent
        body = (plugin_root / "skills" / "using-overpower" / "SKILL.md").read_text(encoding="utf-8")
    except Exception:
        return None
    return (
        "<EXTREMELY_IMPORTANT>\n"
        "This project uses the **overpower** build methodology. Before acting on "
        "any build/coding request, follow the `using-overpower` skill below to "
        "classify the task tier and route to the right amount of process. Load "
        "other skills by opening `skills/<name>/SKILL.md`.\n\n"
        "If this session was just compacted or resumed, also read "
        "`.overpower/progress.md` and `.overpower/findings.md` (if they exist) "
        "before continuing.\n\n"
        f"{body}\n"
        "</EXTREMELY_IMPORTANT>"
    )


def main() -> int:
    context = build_context()
    if context is None:
        return 0

    if os.environ.get("CURSOR_PLUGIN_ROOT") or any(k.startswith("CURSOR_") for k in os.environ):
        payload = {"additional_context": context}
    elif os.environ.get("CLAUDE_PLUGIN_ROOT") and not os.environ.get("COPILOT_CLI"):
        payload = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}
    else:
        payload = {"additionalContext": context}

    sys.stdout.write(json.dumps(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
