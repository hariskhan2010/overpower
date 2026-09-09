# Changelog

## [0.2.0] — 2026-09-09

Completes the skill set — 10 skills, the full methodology.

### Added

- **`brainstorming`** — fuzzy request → agreed spec. One question at a time
  (with the reason why), propose don't just ask, every recommendation names its
  evidence, keep the question open when the user asks for context, no premature
  git commit.
- **`systematic-debugging`** — reproduce → locate (trace the bad value
  backwards) → **explain before fixing** → fix + blast-radius check *on the
  first fix, not the third* → record.
- **`using-git-worktrees`** — checks repo state first (greenfield → no worktree,
  work in place; dirty → stop), detects the real setup command instead of
  assuming a package manager, verifies a green baseline, keeps all file ops
  inside the worktree path.
- **`finishing-work`** — full verification, settle findings, present the merge
  decision, **archive (never delete)** `.overpower/`, carry open findings
  forward into the next feature.
- **`writing-skills`** — the meta-skill. Exactly two frontmatter keys (valid
  YAML), rule in the first two lines, prose-vs-script guidance, reference skills
  by name not path.

### Changed

- `using-overpower` now lists all 10 skills and routes bugs to
  `systematic-debugging` at any tier.

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

### Not yet (as of 0.1.0 — see 0.2.0 above)

- The remaining five skills. *(Done in 0.2.0.)*
- A skill-eval harness (behavioral tests — does the model actually follow the
  skill). Still open.
- Marketplace publishing. Still open.
