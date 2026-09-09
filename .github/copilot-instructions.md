# Copilot instructions — overpower

This project uses the **overpower** build methodology.

Before acting on a build or coding request:

1. Open `skills/using-overpower/SKILL.md` and follow it. It classifies the task
   into a tier (T0 trivial → T3 program) and routes it to the right amount of
   process — a typo gets no ceremony; a feature gets spec → architecture → plan
   → test-first → review → finish.
2. Open other skills at `skills/<name>/SKILL.md` when `using-overpower` names one.
3. If work is in progress, read `.overpower/progress.md` (append-only log) and
   `.overpower/findings.md` (never-truncated open items) first.

Copilot has no delegates or hooks (see `SUPPORT.md`, Tier C): run tasks inline
in sequence, and the scope / dispatch guarantees are rules you follow —
`reviewing-changes` is the check.

Always: classify the tier first · never claim done without verifying · a green
test suite is not proof a fix is safe · RED must fail on a behavioral assertion,
not an import error · name a fix's callers and dependencies before editing ·
merge / push / delete / spend need explicit user approval.
