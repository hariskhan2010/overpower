---
name: writing-plans
description: Use for a T2/T3 task once the spec is agreed. Turns the spec into verifiable tasks and opens the durable state file.
---

# Writing plans

A plan is for an implementer with no context and no judgement. Every task must be
executable and checkable without re-reading the whole spec.

## Before you start

If this is a UI feature or has more than one moving part, `.overpower/architecture.md`
must exist and be signed off (`designing-architecture`). The plan does not
re-decide placement, colour, or which component talks to what — it points at
`architecture.md`. If the architecture doc is missing for a feature that needs
one, stop and run `designing-architecture` first.

## 1. Open the state file

Create `.overpower/progress.md` at the repo root if it doesn't exist:

```markdown
# <feature name>

Spec: <1-line summary or link to the spec doc>
Branch: <branch name, or "not yet">
Started: <ISO date-time>

## Log
- <date-time> plan opened
```

`progress.md` is **append-only** from here. You add lines; you never rewrite
earlier ones. If a task's status changes, append a new line saying so.

Also create `.overpower/findings.md`:

```markdown
# Deferred findings — <feature name>

Real problems found during this work that are out of scope for it.
Append only. Check items off; never delete them.
```

## 2. Write the tasks

Each task:

- **is one behavior change**, 5–20 minutes of work
- names **exact file paths**
- states its **verification**: the command to run, or the observable result,
  and what "pass" looks like
- lists what it **depends on** (earlier task numbers) — so `executing-work`
  knows what can run in parallel

Template:

```markdown
### Task N — <imperative title>
Files: <path>, <path>
Depends on: <task numbers, or "nothing">
Design: <the row(s) in architecture.md this builds — "architecture.md: Export button"> (omit for non-UI/infra tasks)
Change: <what to make true. Concrete. Include the shape of the code if it's not obvious.>
Test: <the failing test to write first (T1+ tasks) — its name and the assertion>
Verify: <command> → <what pass looks like>
```

## 3. Order and parallelism

- A task that only depends on "nothing" or on completed tasks can run in
  parallel with its siblings — mark these; `executing-work` may dispatch them
  concurrently.
- Schema / interface / migration tasks go first and alone — everything downstream
  depends on them.
- The last task is always **"wire it together and run the whole feature
  end-to-end"** with a concrete manual or automated check.

## 4. Show it, get a yes

Present the plan to the user in sections short enough to read. Ask for a yes
before `executing-work` starts. Append to `progress.md`:

```
- <date-time> plan approved by user — N tasks
```

## Anti-patterns

- ❌ "Task 3: implement the feature" — not a task, it's the whole job
- ❌ a task with no `Verify` line — you won't know it worked
- ❌ 40 tasks — the plan is too granular or the feature is really a T3 program;
  group into 5–10 tasks, or split into features with their own plans
- ❌ rewriting an earlier `progress.md` line to "fix" the record — append a
  correction instead
