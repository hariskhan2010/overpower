---
name: executing-plans
description: Use to run an approved, preflighted plan — executes tasks in dependency waves, inline or via subagents as each task's Run line says, verifies every task before marking it done, and keeps the .overpower log current.
---

# executing-plans

Precondition: `.overpower/progress.md` has a plan and a `preflight passed` log
line. If not → `preflight` first.

## 1. Build the waves

From `Depends on`: wave 1 = tasks with no deps; wave N = tasks whose deps are all
in earlier waves. Within a wave, tasks marked `parallel group X` go out together.

## 2. Run each wave

For each task in the wave:

1. Log start: `- <date> Task N → inline` (or `→ subagent implementer`).
2. **Inline:** follow `test-driven-development` against the task block.
   **Subagent:** follow `dispatching-subagents` — launch the whole group in one message.
3. **Verify it yourself.** Run the task's Verify command. A subagent's "all
   tests pass" is a claim until you've seen the output.
4. Log done:
   `- <date> Task N (<title>) done — verify: <command> → <actual result>`
5. Anything out of scope you noticed → `.overpower/findings.md`.

After each wave, run the **full** suite once. Compare to the baseline. New
failures are yours; fix before the next wave (`systematic-debugging`).

## 3. When things go wrong

| Situation | Do |
|---|---|
| Verify fails | `systematic-debugging`. Don't mark done. |
| Plan was wrong (assumption broke) | Stop that task. Fix the plan in place (edit the task block, note why in the log), re-check dependents, continue. |
| Needs the user (credential, decision, access) | `- <date> Task N BLOCKED — <why, what's needed>`. Continue all non-dependent tasks. Raise every blocker together. |
| Scope creep tempts you | findings.md. Not now. |
| Same task failing 3 times | Stop and rethink the approach; tell the user what you tried. |

## 4. After the last wave

→ `verification-before-completion`, then `requesting-code-review`.

## Pace

Don't stop to ask "should I continue?" between tasks of an approved plan.
Do stop for: BLOCKED, a plan change that alters scope, or something destructive.
