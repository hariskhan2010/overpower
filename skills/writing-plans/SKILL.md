---
name: writing-plans
description: Use when turning a spec (and architecture) into an executable task plan — small tasks, real dependencies, a runnable Verify per task, and a Run decision (inline vs subagent) for each. Written so a cold subagent could execute any single task from its block alone.
---

# writing-plans

A plan is good when **any task block, handed alone to a fresh subagent, is enough
to do the task correctly**.

## Shape (exact — op-viewer parses it)

```markdown
# <feature name>

Spec: .overpower/SPEC.md — <one line>
Branch: <branch>
Tier: T2
Started: <YYYY-MM-DD>

## Plan — <N> tasks

### Task 1 — <short title>
Files: <paths; mark (new)>
Depends on: nothing | 1, 3
Uses: <entries from ## Tools, or —>
Run: inline | subagent | parallel group A
Change: <what changes, concretely — names, signatures, behaviour>
Test: <test names, written first — "export returns header row", "empty filter → only header">
Verify: <exact command> → <expected result>

## Log
- <YYYY-MM-DD> spec agreed, plan written — N tasks
```

(`## Research` and `## Tools` sit between the header and `## Plan`.)

## Logging while you build (every tier)

Each task gets its **own** log lines — the dashboard reads status per line:
```
- <date> Task 2 → inline
- <date> Task 2 (list shows due date) done — verify: npm test → 9/9 pass
- <date> Task 3 BLOCKED — <why, what's needed>
```
Log each task as it finishes, not one summary line at the end — the user may be
watching live. Full format: `live-dashboard`.

## Cutting tasks

- **Size:** one coherent change, verifiable on its own, roughly ≤ 1 hour of work.
  Split anything with "and" in the title.
- **Order:** risky / unknown first (fail early), then the core path, then the edges,
  then wiring and docs.
- **Dependencies are real:** "2 needs 1's function" — yes. "2 comes after 1 in my
  head" — no. False deps kill parallelism.
- **Disjoint files** within a parallel group. If two tasks must touch one file,
  they're not parallel — chain them.
- **Every Must-do** in the spec maps to ≥1 task. Note the mapping if not obvious.
- **Verify** is a command with an expected result: `npm test -- export → 6 passed`,
  not "check it works". For UI: the command that renders it plus what to look for.

## Run decision per task

- `inline` — small, shares context with you, or needs the user.
- `subagent` — big isolated chunk that would flood your context.
- `parallel group X` — independent of the others in group X (disjoint files, no
  deps between them). See `dispatching-subagents`.

Default `inline`. A subagent starts cold; it must earn its spawn.

## Don't

- Don't write code in the plan beyond signatures and tricky snippets.
- Don't plan beyond the spec. Extras go to findings.md.
- Don't ask for approval yet — `preflight` checks the plan first, then you ask.
