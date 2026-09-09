---
name: executing-work
description: Use once a plan exists (T2/T3) or a clear T1 task is in hand. Runs the tier-appropriate build loop and verifies every delegated task actually ran.
---

# Executing work

("delegate" = your harness's sub-worker: Claude Code's Task tool, background
agents, etc. No delegate mechanism? Do every task inline, in sequence — you lose
parallelism, not the discipline. See `using-overpower` → Vocabulary.)

## T1 — a single clear task

No delegates. No plan file unless it grows past ~3 steps.

1. `test-driven-development`: RED (for the right reason) → GREEN → REFACTOR.
2. Self-review: re-read your diff against the original request. Does it do
   exactly what was asked, nothing more? Run the verification.
3. If you found something real but out of scope, append it to
   `.overpower/findings.md` (create it if needed) — do not fix it now.

## T2/T3 — executing a plan

Work the plan's tasks in dependency order. For each task or parallel group:

### Do the task

- **Inline (always valid):** you implement the task from its full text
  (Files / Design / Change / Test / Verify).
- **Delegated (if the harness has delegates):** hand one `op-implementer` the
  task's full text. For a **parallel group** (tasks depending only on completed
  work), one delegate per task, concurrently.

### Verify a delegated task actually ran — MANDATORY

The guard against inventing a delegate's work (the failure that plagues
methodology plugins: the orchestrator narrates a whole implementer/reviewer
exchange that never happened).

- A delegate's result is real only with a **concrete run artifact**: a returned
  result block, a run id the harness assigned, or a diff that appeared on disk
  that wasn't there before. Record it in `progress.md`:
  ```
  - <date-time> Task 4 → op-implementer run=<id-or-"inline"> — <one-line result>
  ```
- **If you're about to write what a delegate "did" or "found" and there is no
  such artifact — stop.** You're narrating a run that didn't happen. Run it for
  real, or do the task inline and say so.
- **Working tree unchanged** after a delegate that was supposed to edit = a
  no-op. Re-run with: "the tree is unchanged — make the edit, or state the
  specific reason you can't."

### Review each task

After a task is done, review it with `reviewing-changes` — a delegated
`op-reviewer` if the harness has delegates, otherwise you review it yourself:

- Stage 1: does the diff match the task's `Change` and pass its `Verify`?
- Stage 2: code quality, and the **change-impact gate** on anything the fix
  touched.

A Critical finding blocks the next task. An out-of-scope finding goes to
`findings.md`. Record the verdict (and reviewer run id, if delegated) in
`progress.md`.

### Fixing review findings

When applying a fix, run the change-impact gate first (from `reviewing-changes`):
name the changed symbol's callers and dependencies; read any you haven't.
Append the fix + a one-line impact note to `progress.md`. Then re-run the
task's `Verify`.

### After each task

Append to `progress.md`:
```
- <date-time> Task N done — verify: <command> → passed
```

## Interruptions

If you're resumed mid-plan: read `progress.md` for the last completed task and
`findings.md` for open items, then continue from the next task. Do not restart
completed tasks — the log is the source of truth, not your memory.

## The final task

Always end with the plan's "wire it together and run end-to-end" task. Show the
user the feature working (command output, or the observable result). Then hand
off to `finishing-work`.
