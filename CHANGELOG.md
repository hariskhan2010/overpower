# Changelog

## [0.6.1] — 2026-09-10

Release hygiene — no behaviour change.

### Fixed

- **Manifest version.** `plugin.json` / `marketplace.json` had been stuck at
  `0.1.0` since the first release; bumped to match. `tests/test_plugin_manifest.py`
  now asserts the manifest version equals the newest `CHANGELOG.md` heading, so
  it can't drift again.
- **README accuracy.** Status block said `v0.5` and "not yet used on a real
  build"; corrected to `v0.6` / "used on 4 real builds so far", and the stale
  test/eval counts (`22`/`12`) updated to `38`/`14`.

### Changed

- `.gitignore` now excludes `codegraph-out/` (local graph artifacts).

## [0.6.0] — 2026-09-09

Multi-harness: overpower's method now runs on any agent that reads skill files,
not just Claude Code.

### Added

- **`AGENTS.md`** — the universal entry. Any agent that reads `AGENTS.md`
  (Codex, Cursor, Gemini CLI, Aider, Jules, Zed…) gets routed to the skills.
- **`SUPPORT.md`** — the per-harness feature matrix and the honest trade-off:
  the *method* is one set of files; guarantees that can't be automatic on a
  harness become rules `reviewing-changes` checks — never silently dropped.
- **`.cursor/rules/overpower.mdc`** (always-applies Cursor rule) and
  **`.github/copilot-instructions.md`**.
- `tests/test_harness_neutral.py` — skills don't lean on a Claude-only concept
  without the neutral framing; adapters exist and route to the skills;
  `AGENTS.md`/`SUPPORT.md` stay in sync with `skills/`.

### Changed

- **Skill vocabulary is now harness-neutral.** `using-overpower` defines three
  terms once — **skills mechanism**, **delegate**, **guard hook** — with the
  "if your harness lacks it" fallback. `executing-work`, `autonomous-execution`,
  `reviewing-changes`, `using-git-worktrees` rewritten to use them: a delegate's
  result counts only with a **concrete run artifact** (result block / run id /
  new diff), and every skill says what to do with no delegates (inline, in
  sequence) and no hooks (the rule is checked, not enforced).
- **`hooks/session_start.py`** detects the harness from its environment and
  emits the context shape it consumes (Claude Code nested / Cursor snake_case /
  top-level SDK standard).
- README leads with "runs on any agent"; the what's-different table is
  re-scoped from "Claude Code only" to "one set of files, thin adapters".

### Kept

- Claude Code is still Tier A — full automation via the plugin. Nothing there
  regressed.

## [0.5.0] — 2026-09-09

A diagrammed architecture step in planning.

### Added

- **`designing-architecture` skill** — runs after the spec, before the plan,
  for anything with UI or more than one moving part. Produces
  `.overpower/architecture.md`:
  - a **mermaid component map** (new/changed nodes marked distinctly)
  - an **ASCII layout wireframe** (where the new element sits)
  - an **element spec table**: Where · Look · Does · Data, one row per
    added/changed element
  - **states** (idle/pending/error/empty) for interactive elements
  - a **mermaid sequence diagram** for request round-trips
  - decisions with evidence

  Colour and tokens come from the project's design system (Tailwind config, CSS
  vars, `theme.ts`, a component library) — the skill looks for it; if there's
  none it marks choices `(proposed — no design system found)` so the user knows
  to confirm. Optional: a self-contained `architecture-mockup.html` to *see* it.

### Changed

- `using-overpower` T2/T3 flow gains step 2 (architecture) between spec and plan.
- `writing-plans` requires `architecture.md` for UI/multi-component features and
  adds a `Design:` line to the task template pointing at the element's row —
  the plan no longer re-decides placement or colour.
- `op-implementer` reads `architecture.md` for a task's `Design` row and builds
  exactly that; it does not invent a different colour, position, or interaction.

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
