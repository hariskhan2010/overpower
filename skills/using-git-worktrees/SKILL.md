---
name: using-git-worktrees
description: Use after a T2/T3 spec is approved, to create an isolated workspace for the feature. Also use before dispatching parallel implementer subagents.
---

# Using git worktrees

A worktree is a second checkout of the same repo on its own branch, in its own
directory. It keeps a feature's changes off your main checkout and lets parallel
subagents work without stepping on each other.

## Check before you touch anything

Run these first. Each has a stop condition:

1. **`git rev-parse --git-dir`** — is this a git repo at all?
   - **Not a repo** (greenfield, first commit): do **not** create a worktree.
     Work in place on a new branch (`git init` if needed, then
     `git checkout -b <branch>`). A worktree needs a repo with at least one
     commit. Revisit worktrees once there's history.
2. **`git status --porcelain`** — is the current checkout clean?
   - **Dirty**: stop, tell the user. Don't stash their work silently.
3. **`git worktree list`** — is there already a worktree for this feature?
   - **Yes**: use it, don't make a second.

## Create it

```bash
git worktree add ../<repo>-<feature> -b <feature-branch>
cd ../<repo>-<feature>
```

- Branch name: short, kebab-case, describes the feature (`add-export-json`).
- Location: a **sibling** of the repo, not inside it (a worktree inside the repo
  confuses tooling and `.gitignore`).

## Set it up

Run the project's setup so the worktree can build and test:

- **Detect, don't assume.** Look for the actual setup command:
  `package.json` scripts, a `Makefile` target, `pyproject.toml` +
  (`poetry`? `uv`? `pip -e .`? — check which), a `flake.nix`, a `README`
  "Development" section. Run what the project actually uses.
- If you can't tell, ask the user for the setup command rather than guessing a
  package manager.

## Verify the baseline

Run the test suite **before writing anything**. It must be green (or its
failures must be pre-existing and known — note them in `.overpower/progress.md`).
You cannot tell your change broke something if it was already broken.

Append to `.overpower/progress.md`:
```
- <date-time> worktree ../<repo>-<feature> on <branch>; setup: <cmd>; baseline: <N passed / M pre-existing failures>
```

## While working in a worktree

- **All file operations stay inside the worktree directory.** A subagent editing
  `../<repo>/src/...` instead of `../<repo>-<feature>/src/...` is editing the
  wrong tree — its work won't be on the feature branch. If you dispatch
  subagents, give them the **absolute worktree path** and tell them to `cd`
  there first and to refuse any path outside it.

## Clean up

`finishing-work` removes the worktree (`git worktree remove`) after the branch
is merged or explicitly abandoned. Don't remove it yourself mid-feature.
