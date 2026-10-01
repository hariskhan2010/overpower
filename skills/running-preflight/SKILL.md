---
name: running-preflight
description: Use for a T2/T3 task after the plan is approved and the branch is set up, before any implementation code. Proves the plan's assumptions against the real code, docs and tools; no code is written until it passes.
---

# Running preflight

A plan is a list of assumptions: *this function exists with this signature, this
library call behaves like that, this table has that column, this tool works.*
One wrong assumption wastes every task built on it — and the agent usually finds
out at task 5. Preflight checks them all **before** task 1, when fixing the plan
is cheap.

**No implementation code is written until preflight passes.**

## 0. Baseline

`using-git-worktrees` already ran the test suite and logged the baseline. No
worktree (T1 grown into a plan, or a greenfield repo)? Run the suite now and log
`baseline: <N passed / M pre-existing failures>`. Pre-existing failures aren't
yours — recording them is how you'll tell them apart from regressions.

## 1. Every assumption is real

Walk the plan task by task. List each concrete thing it relies on and check it:

| Assumption | How to check |
|---|---|
| a file / function / class exists with signature X | read the line (or query the code graph if the repo has one) |
| a file the plan calls new doesn't exist yet | list the directory |
| a library API behaves like X | the **installed** version (lockfile) + that version's docs |
| a DB table / column / index exists | the schema, via a DB tool or the migration files |
| a config key / env var / route exists | search config and routing |
| the callers of what you'll change won't break | name them — the same move as the change-impact gate in `reviewing-changes` |

A wrong assumption → fix the task (and `architecture.md` if placement changed),
re-check it. Never start coding around it.

## 2. Every planned tool works

For each `Uses:` entry from `scouting-tools`: load it, make **one harmless read
call** (list / describe / get), complete any login now. A tool that fails here
gets replaced or its task re-planned — not discovered mid-build.

## 3. The plan itself holds

- [ ] every spec requirement maps to at least one task; no task is outside the spec
- [ ] every `Verify` is a runnable command with what "pass" looks like
- [ ] `Depends on` has no cycles and no fake dependencies
- [ ] tasks in one parallel group share no files
- [ ] the riskiest task comes first; schema/interface tasks go first and alone

## 4. Second opinion (T3 only)

Hand a read-only delegate the spec, `architecture.md` and the plan: "Find wrong
assumptions, missing tasks, hidden dependencies and bad ordering. Cite
file:line. Don't rewrite the plan." No delegate → do one deliberate pass yourself
looking only for those four things. Fix what holds up; log what you rejected and why.

## Outcome

Append exactly one of:

```
- <date-time> preflight passed — <n> assumptions checked; tools ok: <list>; plan changes: <none | what changed>
- <date-time> preflight BLOCKED — <what failed, what's needed from the user>
```

If preflight **changed the plan**, show the user what changed and get a fresh
yes before `executing-work`. If it changed nothing, carry on — the user already
approved this plan.

## Anti-patterns

- ❌ "the function is probably called X" — read it
- ❌ checking the library docs from memory instead of the installed version
- ❌ a preflight line with no numbers — say how many assumptions you checked
- ❌ skipping preflight because the plan "looks right" — that's what it was
  supposed to prove
