# Changelog

## [0.4.0] — 2026-09-09

Autonomy: run a whole feature end-to-end, with guardrails.

### Added

- **`autonomous-execution` skill** — the driver loop. Picks the next ready
  task, dispatches subagents, verifies each dispatch is real, reviews, acts on
  findings, records, commits, repeats — until the plan is done or a **hard
  stop** fires. Hard stops: a scope breach, a task that fails review twice, an
  unplanned design decision, red tests one debug pass can't fix, a needed new
  dependency, or anything irreversible/outward-facing (push, merge, delete,
  spend) — those always need explicit approval.
- **Commands** — `/op-build <what>` (full flow), `/op-resume` (continue from
  `.overpower/`), `/op-status` (read-only report).
- **Agents** — `op-implementer` (one task, test-first, inside the worktree) and
  `op-reviewer` (two-stage + change-impact, edits nothing). Defined subagents
  make dispatch more reliable than ad-hoc prompts (further hardening of #1749).
- **`enforce_scope.py` PostToolUse hook** — during a live autonomous build, an
  Edit/Write outside the worktree is blocked with a reason, so the scope-breach
  hard stop fires automatically instead of by instruction (#1040, #2166).
  Strict no-op with no active `.overpower/progress.md`.

### Changed

- `using-overpower` documents autonomous mode and lists the new skill.

## [0.3.0] — 2026-09-09

The behavioral claims are now tested, not just asserted.

### Added

- **`evals/`** — a skill-eval harness. Each case puts a skill in front of a
  model (`claude -p --restricted --tools ""`, clean temp cwd, no repo settings)
  with a realistic scenario and asserts the response follows the rule.
  Deterministic checks (`present_any` / `absent_all` / `regex`) plus an optional
  `--rubric` judge-model pass. Results to `evals/results/` (git-ignored).
- **9 eval cases**, one per behavioral claim in the README:
  `tier-typo`, `tier-feature-forces-plan`, `tier-hidden-design-decision`,
  `red-import-error-is-not-red`, `fix-blast-radius-gate`,
  `subagent-needs-real-agentid`, `findings-carried-not-deleted`,
  `worktree-greenfield-no-repo`, `brainstorm-reask-after-context-question`.
- `tests/test_eval_cases_lint.py` — case files are valid JSON, reference real
  skills, and only use check shapes the runner handles.

### Result

**First run: 9/9 passed** (deterministic checks; the two spot-checked with
`--rubric` also passed the judge). The change-impact gate, the tier router, the
RED-reason rule, the subagent-fabrication guard, and the findings-carry rule
all demonstrably change model behavior on their target scenario. This is a
signal to track over time, not a hard gate — model output varies run to run.

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
