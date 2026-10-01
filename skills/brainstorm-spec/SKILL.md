---
name: brainstorm-spec
description: Use when a build request needs a spec, or when what the user wants is fuzzy — turns a request into an agreed SPEC.md (goal, must-do, out of scope, how we'll know) by asking only the questions that are genuinely the user's call.
---

# brainstorm-spec

Goal: a spec the user recognises as what they meant, in as few round-trips as possible.

## 1. Understand before asking

Before any question, look: read the repo's README and agent rules file (AGENTS.md, CLAUDE.md, GEMINI.md, …), skim the area the
request touches (codegraph if present), and check `.overpower/` for prior work.
Half of "questions" are answered by the code. Never ask what you can look up.

## 2. Sort the unknowns

For each unknown, put it in one bucket:

- **Look it up** — answerable from code/docs. Do it.
- **Default it** — has a conventional answer (naming, file layout, error style,
  library already in the repo). Decide; record it under *Decisions* in the spec.
- **Ask** — only the user can decide: scope boundaries, UX choices, behaviour on
  edge cases that change outcomes, cost/risk trade-offs, anything irreversible.

## 3. Ask once, well

Put all **Ask** items into one structured question to the user (max 4 —
see **ask the user** in the tool map). Each
option: concrete, with the trade-off in its description, recommended one first.
If an answer opens a genuinely new question, one follow-up round is fine. Three
rounds means you should have looked harder in step 1.

If the request is wide open ("make me an app for X"), first offer 2–3 distinct
directions with one line each and let the user pick — then spec the pick.

## 4. Write the spec

`.overpower/SPEC.md` — kept with the rest of the build record, out of the project's own files (T1: a `## Spec` section in progress.md is enough):

```markdown
# <Feature> — spec

## Goal
<one paragraph, in the user's words where possible>

## Must do
1. <testable behaviour — "GET /export?fmt=csv returns the filtered rows as CSV">
2. ...

## Out of scope
- <what we are explicitly not building>

## Decisions
- <default you picked> — <one-line reason>

## How we'll know it works
- <checks: tests, a command, a thing the user can see>
```

Every Must-do is observable and testable. "Fast", "clean", "user-friendly" are
not Must-dos until they have a number or a check.

## 5. Get agreement

Show the spec in short form (Must-do + Out of scope + Decisions) — not the whole
file. Ask "anything wrong or missing?" Incorporate changes; don't re-ask settled points.
