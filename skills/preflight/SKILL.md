---
name: preflight
description: Mandatory gate before writing code from a T2/T3 plan — runs the baseline tests, proves every assumption in the plan against the real code/docs, checks every planned tool actually works, and audits the plan's coverage and dependencies. No code until it passes.
---

# preflight — verify before coding

A plan built on one wrong assumption wastes every task after it. Checking is
cheap now and expensive later. **No production code is written until this passes.**

Run checks 1–3 in parallel where possible.

## 1. Baseline

Run the existing test suite / build / lint exactly as CI would. Record:
`baseline: 412/415 pass — 3 failing in test/auth.test.js (pre-existing)`.

- Pre-existing failures are not yours; recording them lets you tell them apart
  from regressions later.
- If nothing runs (missing deps, broken build), fix setup or ask — don't plan
  on top of a broken floor.

## 2. Assumptions are real

List every concrete thing the plan relies on and check each:

| Assumption kind | Check |
|---|---|
| File / function / class exists with signature X | codegraph `context`/`explain`, or Read the line |
| "New" file doesn't exist yet | Glob |
| Library API behaves like X | installed version from lockfile + docs for that version |
| DB table / column / index exists | schema via DB tool or migration files |
| Config key / env var / route exists | Grep the config and routing |
| Callers won't break | codegraph `affected`, or Grep call sites |

Wrong assumption → fix the plan (and the architecture if needed), re-check.

## 3. Tools work

For every entry in `## Tools`: load it (MCP tools may need loading first — see **find tools** in the tool map), make **one harmless
read call** (list / describe / get), run any `*__authenticate` now. Confirm
each skill is in the available-skills list. A tool that fails here gets replaced
or its task gets re-planned — not discovered mid-build.

## 4. Plan audit

- [ ] Every Must-do maps to ≥1 task; no task falls outside the spec.
- [ ] Every Verify is an exact runnable command with an expected result.
- [ ] `Depends on` has no cycles and no fake deps.
- [ ] Tasks in one parallel group share no files.
- [ ] Risky tasks come first.
- [ ] Branch is right; working tree state is known (clean, or the dirt is understood).

## 5. Second opinion (T3 only)

One read-only planning subagent gets SPEC.md, architecture.md and the plan, with: "Find
wrong assumptions, missing tasks, hidden dependencies and bad ordering. Cite
file:line. Don't rewrite the plan." Fix what holds up; note what you rejected and why.

## Outcome

- **Pass** → log `- <date> preflight passed — baseline <result>; <n> assumptions checked; tools ok: <list>`
- **Needs the user** → log `- <date> preflight BLOCKED — <what>`, ask, stop.

Then present to the user: the plan (task titles + Run column), the preflight
result, anything you changed because of it. Get approval (T2/T3). Then build.
