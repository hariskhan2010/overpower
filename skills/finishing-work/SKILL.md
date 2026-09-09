---
name: finishing-work
description: Use when a plan's tasks are all done and reviewed. Verifies the whole feature, presents the merge decision, and archives (never deletes) the state.
---

# Finishing work

## 1. Full verification

- Run the **entire** test suite in the worktree. All green.
- Run the plan's final "wire it together end-to-end" task's check. Paste the
  output.
- Re-read `.overpower/progress.md` from the top: every task has a
  `done — verify: … → passed` line. Any task that doesn't is not done — go
  finish it.

## 2. Settle the findings

Open `.overpower/findings.md`. For each open item:

- **Fixed during the work?** Check it off with the commit that fixed it.
- **Still open and belongs in this feature?** It's not finished — go do it.
- **Still open and genuinely separate?** Leave it checked-open. It will be
  carried forward (step 4). Do **not** delete it to make the list look clean.

## 3. Present the decision

Show the user:

- what was built (1–3 lines)
- the test result (numbers)
- the open findings being carried forward, by name
- the options:

| Option | When |
|---|---|
| **Merge to main** | it's done and you have merge rights / the user says so |
| **Open a PR** | it needs review, or that's the team's flow |
| **Keep the branch** | more work coming before merge |
| **Discard** | it was a spike, or the approach didn't pan out |

Wait for the user to choose. Don't merge without an explicit yes.

## 4. Archive the state — do NOT delete it

Once merged or discarded:

```
mkdir -p .overpower/archive/<YYYY-MM-DD>-<branch>
git mv .overpower/progress.md   .overpower/archive/<YYYY-MM-DD>-<branch>/progress.md
git mv .overpower/findings.md   .overpower/archive/<YYYY-MM-DD>-<branch>/findings.md
```

- **Carry forward any open findings**: copy the still-open items from the
  archived `findings.md` into a fresh `.overpower/findings.md` at the root,
  under a `## Carried from <branch>` heading. The next feature inherits the
  debt instead of losing it.
- If a `roadmap.md` exists (T3), append a line: what shipped, what's next.

## 5. Remove the worktree

```
cd <main checkout>
git worktree remove ../<repo>-<feature>
```

Only after merge or an explicit "discard". A worktree with unmerged commits is
not removed silently — warn the user first.

## The rule

`finishing-work` **archives and carries forward**. It never deletes a progress
log or drops an open finding. A project you come back to in a month should be
able to read `.overpower/archive/` and its current `findings.md` and know
exactly what happened and what's still owed.
