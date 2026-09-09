---
name: using-overpower
description: Read at the start of any coding or building task, and after context compaction. Classifies the task and routes to the right amount of process.
---

# Using overpower

overpower is a build methodology. Its job is to make you work like a careful
senior engineer **and** to not waste the user's tokens on ceremony a task
doesn't need.

## Step 1 — classify the task (do this before anything else)

Pick the tier. When torn between two, pick the heavier and say so in one line.

| Tier | The request is… | Then |
|---|---|---|
| **T0 trivial** | a question, a typo, a rename, a comment, one obvious line | Answer / make the change. Verify it (run it, read it back). Done. **No plan, no state file, no subagents.** |
| **T1 small** | one function or one file, behavior is clear, **no design decision** | Use `test-driven-development`. Then a self-review pass against the request. No subagents. Open a state file only if it grows past ~3 steps. |
| **T2 feature** | multiple files, or a design choice exists, or "add X to the app/system" | Full flow — see Step 2. |
| **T3 program** | a roadmap, many features, multi-session | T2 per feature + a `roadmap.md` you re-read each session. |

**The expensive mistake is classifying a feature as small.** Any of these forces
**T2 or higher**, regardless of size:

- there is a design decision, or your answer would start with "it depends"
- the change touches more than 2 files
- it changes a public interface, a data format, or a schema
- it needs new dependencies
- the user said "properly", "design", "plan this", or "think about"

The user overrides: "just do it" / "quick" → T0–T1. "plan this properly" → T2.

Announce the tier in one line: `Tier: T2 (touches routing + the store + a migration).`

## Step 2 — the T2/T3 flow

1. **Spec.** If the request is fuzzy, use `brainstorming` first. If it's already
   crisp, write a 3–6 line spec back to the user and get a yes.
2. **Plan.** Use `writing-plans`. This opens `.overpower/progress.md`.
3. **Branch.** Use `using-git-worktrees` (T2+) — it checks the repo is in a
   state that can take one.
4. **Build.** Use `executing-work`. Subagents for parallelizable tasks;
   every subagent result is verified against a real `agentId`.
5. **Review.** Use `reviewing-changes` between task groups and before finishing —
   it runs the change-impact gate on every fix.
6. **Finish.** Use `finishing-work` — archives `.overpower/`, never deletes it.

**Any time a test fails unexpectedly or a bug appears** — at any tier, in any
phase — use `systematic-debugging` before attempting a fix.

## Autonomous mode

When the user wants the whole feature built with minimal check-ins — "build
this", "do it all", or the `/op-build` command — run the spec + plan + worktree
steps *with* the user, then hand execution to `autonomous-execution`: it loops
through the tasks, dispatches `op-implementer` and `op-reviewer` subagents, and
only stops at a **hard stop** (scope breach, repeated review failure, an
unplanned design decision, red tests it can't fix, a new dependency, or anything
irreversible/outward-facing — push, merge, delete, spend). `/op-resume` picks a
build back up from `.overpower/`; `/op-status` reports without changing anything.

## The skills

| Skill | Use it |
|---|---|
| `using-overpower` | session start / after compaction (this file) |
| `brainstorming` | T2/T3, request is fuzzy, before a plan |
| `writing-plans` | T2/T3, spec agreed |
| `using-git-worktrees` | T2/T3, spec approved; before parallel subagents |
| `executing-work` | a plan exists, or a clear T1 task |
| `autonomous-execution` | run a whole feature end-to-end with minimal check-ins |
| `test-driven-development` | writing any T1+ implementation code |
| `reviewing-changes` | between tasks; before finishing; before any fix |
| `systematic-debugging` | a test fails unexpectedly or a bug is reported |
| `finishing-work` | all tasks done and reviewed |
| `writing-skills` | creating or editing an overpower skill |

## The `.overpower/` directory

At the repo root. `progress.md` is an **append-only** log — phase changes, task
status, decisions, RED lines, subagent `agentId`s. `findings.md` holds real
review findings that are out of scope — **it is never truncated or deleted**
mid-project. Full model: `docs/design.md`.

If you were compacted or the session was interrupted: read `.overpower/progress.md`
top to bottom to learn where you are, then `.overpower/findings.md` for what's
still owed, then continue.

## Rules that always apply (every tier)

- **Never claim done without verifying.** Run it, read the output, or show the
  test passing. "Should work" is not done.
- **Never act on a subagent result you can't attribute to a real `agentId`.**
  If there is no `tool_result` block above your summary of what a subagent
  "found", you are hallucinating it — dispatch it for real.
- **A green test suite is not proof a fix is safe.** Tests only cover what some
  consumer already checks.
- Match the surrounding code's style, naming, and comment density.
