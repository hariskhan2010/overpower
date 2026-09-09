---
description: Report where the current overpower build stands, without changing anything.
---

Report the state of the overpower build in this repo. **Read-only — change
nothing, dispatch nothing.**

1. `.overpower/progress.md`: how many tasks total, how many `done`, what's in
   flight, the last few log lines.
2. `.overpower/findings.md`: the open (unchecked) items, by name.
3. `git worktree list`, `git branch --show-current`, `git log --oneline -5` on
   the feature branch, `git status --short`.
4. Any archived builds under `.overpower/archive/`.

Present it as a short status block. If there's no `.overpower/`, say so and stop.
