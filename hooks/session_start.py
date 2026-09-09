#!/usr/bin/env python3
"""overpower SessionStart hook (Claude Code).

Injects the `using-overpower` skill in full at session start / clear / compact,
so the task-tier routing is in context from the first message and again after
every compaction — the point where obra/superpowers loses its bootstrap on some
setups (#2105, #2083).

Builds its JSON with json.dumps (no hand-rolled escaping), self-locates via
__file__ (works even if ${CLAUDE_PLUGIN_ROOT} was not substituted), and prints
nothing on any error so a broken hook can never break a session.
"""
import json
import sys
from pathlib import Path


def main() -> int:
    try:
        plugin_root = Path(__file__).resolve().parent.parent
        skill = plugin_root / "skills" / "using-overpower" / "SKILL.md"
        body = skill.read_text(encoding="utf-8")
    except Exception:
        return 0  # never break a session over the hook

    context = (
        "<EXTREMELY_IMPORTANT>\n"
        "This project uses the **overpower** build methodology. Before acting on "
        "any build/coding request, follow the `using-overpower` skill below to "
        "classify the task tier and route to the right amount of process. For "
        "every other overpower skill, use the Skill tool.\n\n"
        "If this session was just compacted or resumed, also read "
        "`.overpower/progress.md` and `.overpower/findings.md` (if they exist) "
        "before continuing.\n\n"
        f"{body}\n"
        "</EXTREMELY_IMPORTANT>"
    )

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }
    sys.stdout.write(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
