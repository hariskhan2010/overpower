---
name: systematic-debugging
description: Use for any bug, failing test, crash, flaky behaviour, or "it works on my machine" — reproduce, localise, find the root cause with evidence, fix with a regression test. Stops guess-and-patch loops.
---

# systematic-debugging

**No fix without a root cause you can state and prove.** Patching symptoms
creates the next bug.

## 1. Reproduce

- Get a **reliable, fast** reproduction: the failing test, a command, a request.
  Write the exact steps down.
- Can't reproduce → gather more evidence (logs, versions, env, input data)
  before touching code. Flaky → run it N times, note the rate, look for
  shared state, ordering, time, concurrency.
- Turn the repro into a failing automated test now if you can. It becomes the
  regression test.

## 2. Read the evidence fully

The whole error, the whole stack trace, the actual vs expected values. Read
the first error, not the last. Check what changed recently:
`git log -p --since=... -- <area>`, dependency bumps, config, data.

## 3. Localise

Narrow the space, don't guess inside it:
- **Trace the data**: follow the bad value back from where it shows up to where
  it's born. Use codegraph `path`/`context` or call-site Greps to walk callers.
- **Bisect**: `git bisect` across commits, or halve the input / the code path.
- **Instrument**: targeted logging/asserts at boundaries, one run, read the output.
- **Compare** with a working case: same function with good input, the previous
  version, a sibling feature that works.

## 4. Hypothesis → test → conclude

Write one hypothesis: "X is null because Y returns early when Z". Design a check
that would **disprove** it. Run it. Confirmed → root cause. Disproved → next
hypothesis. Never stack two changes to test one idea.

After **3 failed hypotheses**: stop, list what you've ruled out, and question
the assumptions (is the test right? is it the code you think is running?
stale build/cache? wrong env?). Tell the user what you've learned if it's a
long hunt.

## 5. Fix at the root

- Failing test first (from step 1), then the smallest fix at the cause, not the symptom.
- Ask: where else does this pattern occur? Grep for siblings; fix or log to findings.
- Run the full suite — the fix mustn't break neighbours.

## 6. Record

In progress.md log (if in a build) or your report: symptom → root cause
(`file:line`) → fix → regression test name. One line each.

## Red flags

"Let me try...", adding retries/sleeps to make it pass, catching and swallowing
the error, changing the test's expectation, a fix you can't explain.
