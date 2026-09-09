---
name: reviewing-changes
description: Use to review a task's diff before moving on, and before finishing a branch. Also defines the change-impact gate that every fix must pass.
---

# Reviewing changes

Two stages. Both required. Run them yourself, or hand them to an `op-reviewer`
delegate if the harness has delegates.

## Stage 1 — does it match the plan?

- Diff does exactly what the task's `Change` line says — nothing more.
- The task's `Verify` command runs and passes (paste the output).
- No unrelated edits rode along. No commented-out code. No debug prints.
- Public interfaces / formats / schemas changed only if the task said so.

Fail Stage 1 → back to the implementer with the specific gap. Do not proceed.

## Stage 2 — code quality

- Names say what the thing is. Control flow is followable. No needless option
  parameters or abstraction the task didn't call for (YAGNI).
- Error paths handled the way the surrounding code handles them.
- The test is a real test (see `test-driven-development` — asserts behavior, not
  a mock).
- Matches the file's existing style and comment density.

## Severity

| Level | Meaning | Effect |
|---|---|---|
| **Critical** | wrong behavior, a crash, a security hole, data loss | Blocks the next task. Fix now. |
| **Important** | will bite later; a real gap | Fix now if cheap, else `.overpower/findings.md` with a note. |
| **Minor** | style, naming, a nicer way | Note it; batch or skip. |

An out-of-scope finding of any severity goes to `findings.md` — appended, with
the task that found it. `findings.md` is never truncated.

## The change-impact gate — run this before applying ANY fix

Fixes to review findings are the #1 source of new bugs, because each fix looks
only at its named line. Before you edit:

> **Name the symbol the fix changes.** Then:
> 1. **Callers** — every place that uses its result. What does each do with it?
> 2. **Dependencies** — every thing it now reads or calls.
>
> If (1) or (2) has an entry you have not read this session, **read it before
> editing.** A green test suite is not evidence here — the suite only covers
> what some existing consumer already checks, and a call site that throws away
> the return value will stay green while the next real caller crashes.

Worked example of what this catches:

> A build step's return value went two places: into a generic `refresh()` that
> writes it, and out to `refresh()`'s callers that use it. Fix 1 made the step
> write for itself but left the return value → `refresh()` wrote it twice.
> Fix 2 returned `nil` to stop the double write → every caller of `refresh()`
> called `.size` on `nil` and crashed. Two fixes, each checked one consumer.

Record in `progress.md` together:

```
- <date-time> fix for <finding>: changed <symbol>. Callers: <list> (read). Depends on: <list> (read). Verify: <cmd> → passed.
```

## After review

Append the verdict to `progress.md`:

```
- <date-time> Task N review (reviewer run=<id-or-"inline">): Stage 1 pass, Stage 2 — <n> Important → 1 fixed, 1 to findings.md. Cleared.
```
