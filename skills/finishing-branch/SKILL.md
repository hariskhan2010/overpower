---
name: finishing-branch
description: Use when a build is verified and reviewed — presents the user with merge / PR / keep / discard options, executes their choice safely, cleans up worktrees, and closes out .overpower/.
---

# finishing-branch

## 1. Confirm it's really finished

`verification-before-completion` passed this turn, review findings are all
resolved or logged, `git status` is understood. If not → go back.

## 2. Offer the options (one structured question to the user)

1. **Open a PR** (recommended for shared repos) — push the branch, `gh pr create`
   with a body: summary by Must-do, test evidence, findings, how to try it.
2. **Merge locally** into the base branch — for solo repos.
3. **Keep the branch** as is — user will handle it.
4. **Discard** — only with explicit confirmation; show what would be lost first.

Committing, pushing, merging and deleting are the user's call — never assume.
Commit messages and PR bodies follow the repo's style and any attribution rules
in context.

## 3. Execute

- Merge: update base, merge, run the full suite **on the merged result**.
- PR: push, create, report the URL. If CI exists, say it's running; don't claim
  it passed until it has.
- Worktrees: remove the finished ones (`git-worktrees` cleanup).

## 4. Close out `.overpower/`

- Log `- <date> FINISHED. <merged to X | PR #N | kept on branch Y>`.
- Ask whether to keep `.overpower/` in the repo, move it to
  `.overpower/archive/<date>-<feature>/`, or delete it. Default: archive.
- Open findings stay in findings.md — mention the count in the final message.
