---
name: verification-before-completion
description: Use before saying anything is done, fixed, passing, or working — run the checks that prove it this turn, compare against the baseline, exercise the real thing once, and report actual numbers. Claims without fresh evidence are not allowed.
---

# verification-before-completion

"Done" is a claim about the world. Back it with output you saw **this turn**.

## Checklist

1. **The specific check** — the task's Verify, or the repro from debugging.
   Run it; read the output; it passes.
2. **The full suite** — tests, type-check, lint, build as CI runs them. Compare to
   the preflight baseline: same pre-existing failures are fine and are named;
   any new failure is yours.
3. **The real thing, once** — run the program the way a user would: start the
   server and hit the endpoint, run the CLI, open the page. Unit tests passing
   while the app fails to start is common. Dogfooding finds the bugs tests don't.
4. **Spec coverage** — walk the Must-do list; each item has evidence (a test
   name or a command result). Missing → not done.
5. **Diff sanity** — `git diff --stat` and a skim: no debug prints, no stray
   files, no commented-out code, no secrets, nothing outside the plan.

## Reporting

- Real numbers: `431/434 pass (3 pre-existing failures in auth.test.js, unchanged)`.
- Name what you **didn't** verify and why: "didn't test on Windows", "no prod DB".
- Failed or skipped → say so plainly. Never round "mostly works" up to "works".

## Banned without evidence

"should work", "this fixes it", "tests pass" (which? how many?), "done" with
an unrun Verify, a subagent's report repeated as fact.
