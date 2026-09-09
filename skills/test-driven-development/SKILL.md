---
name: test-driven-development
description: Use before writing any implementation code for a T1+ task — a feature, a bugfix, or a behavior change.
---

# Test-driven development

Write the test first. Watch it fail **for the right reason**. Write the minimal
code to pass. Refactor with the test green.

**If you didn't watch the test fail with a real assertion failure, you don't
know it tests anything.**

## The iron law

```
NO IMPLEMENTATION CODE WITHOUT A TEST THAT FAILS ON AN ASSERTION FIRST
```

Wrote code before the test? Delete it. Don't keep it "for reference", don't
adapt it — implement fresh from the test.

Exceptions (say which one, out loud): throwaway spike, pure config, generated
code. "Just this once" is not an exception.

## RED — and what actually counts as RED

Write one small test for one behavior. Clear name. Real code paths, not a mock
of the thing under test.

Run it. Now classify the failure:

| The test… | That's… | Do |
|---|---|---|
| fails with an **assertion** message about behavior (`expected 3, got undefined`) | **RED. Good.** | Proceed to GREEN. |
| **passes** | you're testing existing behavior | Rewrite the test to target what's missing. |
| **errors**: `X is not defined`, `cannot import`, syntax error, missing file, wrong path | harness not wired | Fix the wiring. Re-run. Only count RED once the failure is assertion-shaped. |

**Before GREEN, write this line in `.overpower/progress.md`** (or say it, for a
no-state T1):

> RED: `<test name>` fails with `<the actual assertion failure>` — this is the
> behavior the code will provide.

If you can't fill in `<the actual assertion failure>` with a real behavioral
message, you do not have RED yet.

### Why "feature missing (not typos)" isn't enough

Extracting buggy inline logic into a new function and testing it: if you write
the function correctly from the start, RED is `X is not exported`. That proves
the test file resolves an import. It does **not** prove the assertions can catch
the bug — and a test written during a bugfix is exactly the one that must have
detection power. So: stub the function to return a wrong-but-defined value,
confirm the test goes red **on the assertion**, then implement.

## GREEN

Simplest code that makes the test pass. No options objects, no config knobs, no
"while I'm here". Just the behavior the test asserts.

Run the test. Green? Run the **whole** suite — you didn't break a neighbor.

## REFACTOR

Clean up with the suite green. **A refactor has no RED.** If a test goes red
during refactor, you changed behavior — stop, decide if that was intended, and
if so it's a new RED→GREEN cycle with its own progress line.

## Commit

One RED→GREEN→REFACTOR cycle = one commit. Message names the behavior added.

## Good vs bad tests

<Good>
```
test('retries a failing operation 3 times then succeeds', async () => {
  let attempts = 0;
  const op = () => { attempts++; if (attempts < 3) throw new Error('fail'); return 'ok'; };
  expect(await retry(op)).toBe('ok');
  expect(attempts).toBe(3);
});
```
Names the behavior. Exercises real control flow. One assertion cluster.
</Good>

<Bad>
```
test('retry works', async () => {
  const m = jest.fn().mockRejectedValueOnce(e).mockResolvedValueOnce('ok');
  await retry(m);
  expect(m).toHaveBeenCalledTimes(2);
});
```
Vague name. Tests the mock, not the code. Tells you nothing when it breaks.
</Bad>
