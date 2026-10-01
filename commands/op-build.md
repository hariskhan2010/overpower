---
description: Build a feature end-to-end with overpower — spec, plan, autonomous execution, review, finish.
argument-hint: <what to build>
---

The user wants to build: **$ARGUMENTS**

Run the overpower flow:

1. Load the `using-overpower` skill and classify this. If it's T0/T1, just do it
   well — don't spin up the full flow for a small task.
2. For T2/T3:
   a. `brainstorming` if the request is fuzzy — get an agreed spec. **This step
      is not autonomous; work it with the user.**
   b. `writing-plans` — a plan the user signs off on. Opens `.overpower/`.
   c. `using-git-worktrees` — isolated workspace, green baseline.
   c2. `running-preflight` — check the plan's assumptions against the real
      code, docs and tools. No code until it passes.
   d. `autonomous-execution` — run the loop. Dispatch `op-implementer` and
      `op-reviewer` subagents. Respect every hard-stop condition.
   e. `finishing-work` — surface the merge decision to the user.

Announce the tier and the plan before starting the loop. Once the loop is
running, only stop to talk to the user at a hard stop or when the feature is
done — that's the point of this command.
