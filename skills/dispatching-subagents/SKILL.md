---
name: dispatching-subagents
description: Use when a plan has independent tasks that can run in parallel, or one big isolated chunk that would flood your context — decides whether a subagent pays off, writes a self-contained brief, launches parallel groups in one message, and checks every result before accepting it.
---

# dispatching-subagents

A subagent starts **cold** — it re-reads the codebase you already know. It pays
off only when the work is independent and big enough to beat that cost.

## Spawn or not?

Spawn when **all** hold:
- the task needs no back-and-forth with the user, and
- it shares no files with other running work, and
- either ≥2 such tasks can run at once, or it's a large isolated chunk
  (a module, a wide research sweep) that would bloat your context.

Stay inline when: it's small, it touches files another task touches, you already
hold all the context, or it needs judgement calls the user should see.

## Pick the type

| Work | Agent type |
|---|---|
| Read-only search / "where is X" across many files | an explore / read-only agent |
| Design a sub-problem, critique a plan | a plan / read-only agent |
| Implement a task, write tests | this plugin's `implementer`, else a general coding agent |
| Review a diff | this plugin's `reviewer`, else a read-only agent with `agents/reviewer.md` as its brief |

Exact names differ per harness — see **dispatch a subagent** in the tool map.
No subagent support → run the tasks inline, one at a time, same rules.

## The brief (self-contained — the subagent sees nothing else)

```
You are implementing one task from a plan. Work only on this task.

TASK (verbatim from the plan):
<the whole ### Task N block>

CONTEXT:
- Spec lines this serves: <Must-do items>
- Interfaces you must match: <from architecture.md>
- Pattern to copy: <file:line from research>
- Test runner: <command>
- Tools to use: <from Uses:, with how>

RULES:
- Write the failing test first, see it fail for the right reason, then implement.
- Touch only: <Files list>. If you must touch anything else, stop and report why.
- Do not edit .overpower/ or commit.
- If an assumption in the task is wrong, stop and report it — don't improvise a redesign.

REPORT BACK:
- Files changed (paths)
- The Verify command's exact output
- RED evidence (what failed first and why)
- Anything surprising, or out of scope you noticed
```

## Launch

- All tasks of a parallel group in **one message** (multiple subagent calls in parallel).
- Same repo + parallel edits → one worktree each (see `git-worktrees`).
- Never fabricate or predict a result while it's running.

## Accept or reject

For each report: read the diff, run Verify yourself, check it stayed inside its
Files list. Good → log done. Wrong → fix inline if small, or re-brief with the
specific failure (never "try again"). Then merge worktrees one at a time,
running tests after each merge.
