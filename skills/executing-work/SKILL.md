---
name: executing-work
description: Use once a plan exists (T2/T3) or a clear T1 task is in hand. Runs the tier-appropriate build loop and verifies every subagent dispatch is real.
---

# Executing work

## T1 — a single clear task

No subagents. No plan file unless it grows past ~3 steps.

1. `test-driven-development`: RED (for the right reason) → GREEN → REFACTOR.
2. Self-review: re-read your diff against the original request. Does it do
   exactly what was asked, nothing more? Run the verification.
3. If you found something real but out of scope, append it to
   `.overpower/findings.md` (create it if needed) — do not fix it now.

## T2/T3 — executing a plan

Work the plan's tasks in dependency order. For each task or parallel group:

### Dispatch

- **Sequential task:** do it yourself, or dispatch one implementer subagent with
  the task's full text (Files / Change / Test / Verify).
- **Parallel group** (tasks that depend only on completed work): dispatch one
  subagent per task, concurrently.

### Verify the dispatch is real — MANDATORY

This is the guard against fabricating subagent runs.

- After a subagent returns, there **must** be a `tool_result` block in this
  conversation with an `agentId` and token usage. Record it in `progress.md`:
  ```
  - <date-time> Task 4 → implementer agentId=<id> (~<n> tok) — <one-line result>
  ```
- **If you are about to write what a subagent "did" or "found" and there is no
  `tool_result` block for it above — stop.** You are narrating a run that did
  not happen. Dispatch it for real.
- **Unchanged working tree** after an implementer subagent = a no-op. Re-dispatch
  with: "the working tree is unchanged — make the edit described, or reply with
  the specific reason you cannot."

### Review each task

After a task's implementer returns, dispatch a **reviewer** subagent (or review
yourself for T1-sized tasks) using `reviewing-changes`:

- Stage 1: does the diff match the task's `Change` and pass its `Verify`?
- Stage 2: code quality, and the **change-impact gate** on anything the fix
  touched.

A Critical finding blocks the next task. An out-of-scope finding goes to
`findings.md`. Record the verdict + reviewer `agentId` in `progress.md`.

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
