---
name: systematic-debugging
description: Use the moment a test fails unexpectedly, a bug is reported, or behavior doesn't match expectation. Before trying a fix.
---

# Systematic debugging

The rule: **you do not write a fix until you can explain the failure.** A fix
without an explanation is a guess, and guesses at bugs usually move the symptom.

## Phase 1 — reproduce it

- Get it failing **on demand**. A bug you can't reproduce, you can't verify you
  fixed.
- Shrink the reproduction: smallest input, fewest steps, one assertion.
- Write it as a failing test now if you can — that test is your GREEN target and
  your regression guard.

## Phase 2 — locate it

- Trace the bad value **backwards** to where it's first wrong. Not where it
  crashes — where it stops being correct. Add prints / breakpoints / logging at
  the midpoint, then bisect.
- State what you expected at each point and what you actually saw. The gap is
  the bug's location.

## Phase 3 — explain it

Write one or two sentences: **"It's wrong because X. X happens because Y."**

If you can't write that, you haven't found it — back to Phase 2. Do not proceed
to a fix on a hunch.

Common real causes (check before blaming the framework):
- an off-by-one / boundary condition
- a value read before it's set, or after it's changed
- two code paths that should agree and don't
- a stale cache / a not-invalidated derived value
- an assumption about an input that isn't always true

## Phase 4 — fix it, and check the blast radius

- Write the **minimal** change that addresses the cause you named — not the
  symptom.
- **Before you save it**, run the change-impact gate from `reviewing-changes`:
  name the callers and dependencies of what you're changing, read the ones you
  haven't. This is here in Phase 4 *deliberately* — the "each fix creates new
  symptoms elsewhere" check must fire on the **first** fix, not after three
  rounds of damage.
- Run the Phase 1 reproduction. It must now pass.
- Run the whole suite. Nothing else moved.

## Phase 5 — record it

Append to `.overpower/progress.md` (or say it, for a no-state task):

```
- <date-time> bug: <symptom>. Cause: <the X-because-Y>. Fix: <symbol> in <file>.
  Impact checked: callers <list>, deps <list>. Repro test: <name>.
```

## When you're stuck after Phase 2

- Re-read the actual error text, slowly, all of it. The answer is often in a
  line you skimmed.
- Question the assumption you're most sure of — that's where blind spots live.
- Rubber-duck it to the user: state what you know and what doesn't fit.
- If three real attempts to locate it have failed, stop and tell the user what
  you've ruled out. Don't keep guessing.
