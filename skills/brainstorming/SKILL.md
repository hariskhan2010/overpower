---
name: brainstorming
description: Use at the start of a T2/T3 task when the request is fuzzy — before writing a plan or any code. Turns a vague idea into an agreed spec.
---

# Brainstorming

The goal is a spec the user has explicitly signed off on. Not code, not a plan —
a shared understanding of *what* and *why*, small enough to read in one sitting.

## How to run it

**Ask one question at a time, and make each question earn its place.** One
question at a time is not a ritual — it's so the user can actually think about
each answer instead of triaging a wall of them. If two questions are genuinely
independent and both cheap to answer, asking both is fine; say why.

Good questions surface a **decision the user hasn't made yet**:
- "When two records conflict, does the newer one win, or do we surface both?"
- "Is this for one project at a time, or many in parallel?"

Bad questions ask the user to do your thinking:
- "What should the architecture be?" — that's your job to propose
- "What edge cases matter?" — enumerate the ones you see, ask which are real

**When the user asks you for context instead of answering** — answer them, then
**re-ask the same question**. Don't move on. Their question was them trying to
answer yours.

## Proposing, not just asking

After ~2–5 questions you should know enough to **propose**. Put a concrete option
on the table with its tradeoff, and say what you'd pick:

> "Two ways to store this: a single JSON file (simple, no deps, fine under ~10k
> entries) or SQLite (scales, adds a dep). I'd start with JSON — we can migrate
> if it grows. Object?"

Every recommendation names the **evidence** behind it — a measured number, a
constraint the user gave, a property of the data. "X is popular" or "X is the
standard" is not evidence; if you're guessing, say "I'm guessing, but…".

## The spec

When the shape is clear, write it back in sections short enough to read:

```markdown
# <name> — spec

## Problem
<what's wrong / missing today, in the user's terms>

## What we're building
<the change, concretely>

## Decisions
- <decision>: <what we chose> — because <evidence>
- <decision>: <what we chose> — because <evidence>

## Out of scope
- <thing we are deliberately not doing now>

## How we'll know it works
<the observable outcome>
```

Show it. Ask for a yes. Iterate on the parts they push back on.

## Do NOT

- ❌ start coding "to explore" — that's committing before the user agreed
- ❌ commit the spec or plan to git here — no branch exists yet
  (`using-git-worktrees` creates it after sign-off)
- ❌ write the spec to `.overpower/` before sign-off — keep it in the
  conversation until the user says yes, then `writing-plans` persists it
- ❌ present 8 options — narrow to the 2 that matter and recommend one
