---
description: Resume an interrupted overpower build from its .overpower/ state.
---

Resume the overpower build in this repo.

1. Read `.overpower/progress.md` from the top. Find the last task marked `done`
   and its verify result. If the file doesn't exist, tell the user there's
   nothing to resume.
2. Read `.overpower/findings.md` — note every unchecked item; these are still
   owed.
3. Read `.overpower/roadmap.md` if it exists (T3).
4. Check the worktree named in `progress.md` still exists and is on the right
   branch (`git worktree list`, `git branch --show-current`). If it's gone or
   dirty in a way the log doesn't explain, stop and ask the user.
5. Summarize for the user: where the build is (task N of M done), what's open,
   what's next.
6. Re-enter `autonomous-execution` at its loop, starting from the next
   undone task. **Do not restart any task the log says is done.**
