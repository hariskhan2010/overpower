---
name: git-worktrees
description: Use when parallel subagents will edit the same repo, or when a T3 build should be isolated from the user's working tree — creates, tracks, merges and cleans up git worktrees safely.
---

# git-worktrees

Worktrees let parallel work happen in separate checkouts of one repo without
stepping on each other or on the user's uncommitted changes.

## When

- Parallel subagents editing the same repo → give each its own worktree (your harness may
  do this for you — see **isolated subagent** in the tool map).
- A T3 build → do the whole build in one worktree off the base branch, so the
  user's checkout stays untouched.
- Not for T0/T1, and not when the user wants to watch edits land in their tree.

## Creating one yourself

```bash
git worktree add ../<repo>-<feature> -b <feature-branch> <base>
```
- Put it **outside** the repo directory (or in a gitignored folder) so tools
  don't index it twice.
- Install deps and run the baseline tests in the new worktree before building —
  a worktree has no `node_modules` / venv of its own.
- Log it: `- <date> worktree <path> on <branch>` (op-viewer shows this).

## Merging subagent worktrees

One at a time, in plan order:
1. Review the branch diff against the task's Files list.
2. Merge (or cherry-pick) into the build branch.
3. Run the full test suite. Conflict or red → fix now, before the next merge.

## Cleanup

`git worktree list` to see them; `git worktree remove <path>` for each finished
one; `git branch -d <branch>` once merged. Agent-created worktrees with no
changes are cleaned up automatically. Never `--force` remove a worktree with
unmerged work without asking.
