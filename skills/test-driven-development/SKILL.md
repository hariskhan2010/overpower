---
name: test-driven-development
description: Use when writing or changing production code — write the failing test first, watch it fail for the right reason, make it pass with the least code, then tidy. Includes what to do when TDD genuinely doesn't fit.
---

# test-driven-development

## The loop

1. **RED** — write one test for the next small behaviour. Run it. It must fail,
   and fail **for the reason you expect** (assertion on the missing behaviour —
   not an import error, typo, or wrong path). A test that fails for the wrong
   reason proves nothing; fix the test until it fails right.
2. **GREEN** — write the least code that makes it pass. Run it. Run the
   neighbouring tests too.
3. **REFACTOR** — tidy names, remove duplication, keep behaviour. Tests stay green.
4. Repeat for the next behaviour.

Log RED honestly in the task's log line when it was informative:
`RED: 4/5 fail on AssertionError (expected header row, got '') — valid`.

## What makes a good test

- Tests **behaviour through the public interface**, not internals. Refactors
  shouldn't break it.
- One reason to fail. The name says the behaviour: `"empty filter returns header only"`.
- Real collaborators where cheap (in-memory DB, temp dir, local server); mocks
  only at slow/external boundaries (network, clock, payment API).
- Covers the edge cases the spec cares about: empty, one, many, invalid, failure
  of a dependency.
- Deterministic. No sleeps, no real time, no order dependence.

## When code already exists without tests

Write a **characterisation test** pinning current behaviour first, then change it.

## When TDD doesn't fit — say so, don't fake it

Pure config, generated code, visual styling, spikes to learn an API. Then:
state why in the log, verify another way (render it, run it, screenshot it), and
add a test afterwards wherever behaviour emerged. A spike's code is thrown away
or rewritten test-first.

## Red flags

- Writing the implementation, then a test that passes first time → you skipped RED.
  Break the implementation, see the test fail, restore.
- Changing a test to match buggy output.
- Asserting on mocks being called instead of on outcomes.
