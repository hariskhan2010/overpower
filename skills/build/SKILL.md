---
name: build
description: Use when asked to build a feature, add a capability, or make a multi-step change (T2/T3). Runs the full overpower pipeline — spec, research, tool-scout, architecture, plan, preflight, build in waves, review, finish — and keeps a live record in .overpower/.
---

# build — the full pipeline

Trigger: `/overpower:build <what to build>`, or any T2/T3 build request.

If `.overpower/progress.md` already exists → use `resume-build` instead.

## The pipeline

| # | Phase | Skill | Output | Gate |
|---|---|---|---|---|
| 1 | Spec | `brainstorm-spec` | `.overpower/SPEC.md` | user agrees with the spec |
| 2 | Research | `research` | `## Research` in progress.md | — |
| 3 | Tools | `tool-scout` | `## Tools` in progress.md | — |
| 4 | Design | `architecture` (T2/T3) | `.overpower/architecture.md` | — |
| 5 | Plan | `writing-plans` | `## Plan` in progress.md | — |
| 6 | Verify | `preflight` | `preflight passed` log line | **all checks pass, then user approves plan** |
| 7 | Build | `executing-plans` + `test-driven-development` + `dispatching-subagents` | code + tests, `Task N done` lines | every task's Verify passes |
| 8 | Check | `verification-before-completion` | full suite + real run | green, real numbers |
| 9 | Review | `requesting-code-review` → `receiving-code-review` | fixes | no open must-fix items |
| 10 | Finish | `finishing-branch` | merge / PR / handoff | user's choice |

Phases 2 and 3 run **together** (one message, parallel tool calls) — they don't
depend on each other.

## Rules for the whole run

- Create `.overpower/` at the repo root at the start of phase 1. Follow
  `live-dashboard` for every file format — op-viewer parses them.
- Two user touchpoints, not ten: agree the spec (phase 1) and approve the
  verified plan (phase 6). Then build autonomously until done or BLOCKED.
- A BLOCKED task stops only its dependents. Continue everything else, then
  bring all blockers to the user at once.
- Out-of-scope problems you spot → `.overpower/findings.md`, never silently fixed,
  never silently dropped.
- Tell the user once, at the start: "watch live with `op-viewer` in the repo root."

## Final report (to the user)

What was built (by Must-do item), test result with real numbers
(`baseline 412/415 → now 431/434, same 3 pre-existing failures`), open findings,
anything skipped and why, and where it is (branch / PR). No "should work".
