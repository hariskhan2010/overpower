# Changelog

## [0.1.0] — 2026-09-09

First cut. The skeleton, the state model, and the five core skills.

### Added

- **Plugin skeleton** — `.claude-plugin/plugin.json`, `hooks/` (SessionStart
  injection via a Python hook that self-locates and never breaks a session).
- **`using-overpower`** — the router. Classifies every request into a tier
  (T0 trivial → T3 program) and sends it through the right amount of process.
- **`writing-plans`** — spec → verifiable tasks; opens the durable
  `.overpower/progress.md` + `findings.md`.
- **`executing-work`** — the tiered build loop. Verifies every subagent
  dispatch against a real `agentId`; treats an unchanged working tree as a
  no-op and re-dispatches.
- **`test-driven-development`** — RED must fail on a **behavioral assertion**,
  not an import/typo/missing-export error; refactors have no RED.
- **`reviewing-changes`** — two-stage review + the **change-impact gate**:
  before any fix, name the changed symbol's callers and dependencies and read
  the ones you haven't.
- `docs/design.md` — the issue-by-issue rationale vs `obra/superpowers`.

### Not yet

- `brainstorming`, `systematic-debugging`, `using-git-worktrees`,
  `finishing-work`, `writing-skills` — planned; `using-overpower` references
  them and will fall back to plain judgement until they exist.
- A skill-eval harness.
- Marketplace publishing.
