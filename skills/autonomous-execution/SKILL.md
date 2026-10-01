---
name: autonomous-execution
description: Use when the user wants overpower to run a whole feature end-to-end with minimal check-ins — "build this", "just do it all", "/op-build". The driver loop.
---

# Autonomous execution

This is the loop that lets overpower work a feature for an hour without stopping
to ask permission at every step — while staying inside guardrails so it can't go
off the rails or do something irreversible unasked.

Works on any harness. Where the harness has **delegates** (sub-workers) the loop
runs tasks in parallel through them; where it doesn't, the loop runs tasks
inline in sequence — slower, same discipline. Where the harness has a **guard
hook**, an out-of-scope edit is blocked automatically; where it doesn't, the
scope rule is one you follow and `reviewing-changes` checks. See `SUPPORT.md`.

## Entry

You arrive here from `/op-build`, from `/op-resume`, or when the user says "build
the whole thing". Preconditions:

- an **approved spec** (run `brainstorming` first if the request is fuzzy — that
  step is *not* autonomous, it needs the user)
- an **approved plan** (`writing-plans`) with tasks in `.overpower/progress.md`
- a **worktree** (`using-git-worktrees`) with a green baseline
- a **`preflight passed`** line in `progress.md` (`running-preflight`) — the
  plan's assumptions checked against the real code before the loop builds on them

If any is missing, do that step *with* the user, then start the loop.

## The loop

Repeat until the plan is complete or a **hard stop** fires:

1. **Pick the next work.** From `progress.md`, the lowest-numbered task whose
   dependencies are all `done`. If several are independent, take the whole group.
2. **Do it.** `op-implementer` per task (the group in parallel) if the harness
   has delegates; otherwise implement each inline, in order. Give each the
   task's full text and the **absolute worktree path**.
3. **Verify it actually ran** (from `executing-work`): a concrete run artifact —
   a result block, a run id, or a new diff on disk. None → it didn't run, redo.
   Unchanged tree → no-op, redo with "make the edit or say why not".
4. **Review.** `op-reviewer` per completed task (or review inline). Stage 1 +
   Stage 2 from `reviewing-changes`.
5. **Act on findings.**
   - Critical → fix now (run the change-impact gate first), re-verify, re-review.
   - Important, in scope → same.
   - Anything out of scope → append to `.overpower/findings.md`, keep going.
6. **Record.** Append task done + verify result + reviewer run id (or "inline")
   to `progress.md`.
7. **Commit** the task (one RED→GREEN→REFACTOR = one commit).
8. Back to 1.

When the plan's last "wire it together end-to-end" task passes: stop the loop,
run `finishing-work`, and **surface to the user** for the merge decision.

## Hard stops — end the loop and surface to the user immediately

Stop and report (do **not** push through) if:

- a task's implementer touched a file **outside the worktree** — the guard hook
  flags this where the harness has one; everywhere else you check it yourself
  before recording the task done. Either way it's a scope breach — stop.
- the same task has failed review **twice** — the plan or the approach is wrong
- an **unplanned design decision** surfaced (a task can't be done as written
  without choosing something the spec didn't) — that's the user's call
- tests that were green go red and one debugging pass (`systematic-debugging`)
  doesn't restore them
- a task would need a **new dependency** not in the plan
- you're about to do something **irreversible or outward-facing**: `git push`,
  merge to main, `rm -rf`, a network call with side effects, editing anything
  outside the repo, spending real money. These **always** need explicit approval,
  autonomous mode or not.
- the user's token budget is visibly near exhaustion — checkpoint and report
  rather than dying mid-task

## Surfacing

When you stop — done or hard-stopped — give the user:

- one line: done / stopped-because-X
- what got built (tasks completed, commits)
- open findings by name
- if hard-stopped: the specific decision or breach, and 2 options for proceeding

Then wait. Autonomous means fewer check-ins, not zero — the loop earns its
autonomy by stopping at the right moments, not by never stopping.

## Resuming

`/op-resume` or a fresh session: read `progress.md` top-to-bottom for the last
`done` task, `findings.md` for open items, confirm the worktree still exists and
is on the right branch, then re-enter the loop at step 1. Never restart a task
the log says is done.
