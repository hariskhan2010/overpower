---
name: resume-build
description: Use when .overpower/progress.md already exists, after /clear or a context compaction, or when the user says "continue" — rebuilds the state of an interrupted build from the record and picks up at the right phase without redoing finished work.
---

# resume-build

The `.overpower/` record is the memory. Trust it, then verify it.

## 1. Read the record

`.overpower/progress.md` (header, Research, Tools, Plan, Log), `.overpower/SPEC.md` (or a root `SPEC.md` from older builds),
`.overpower/architecture.md`, `.overpower/findings.md`.

## 2. Work out where you are

| Last thing in the log | Resume at |
|---|---|
| No `## Plan` yet | the phase after the last completed one (spec → research → …) |
| Plan, no `preflight passed` | `preflight` |
| `preflight passed`, no approval noted | show plan + preflight result, ask approval |
| Tasks in progress | `executing-plans` from the first task not `done` |
| All tasks done, no review | `verification-before-completion` → review |
| `FINISHED` | nothing to resume — tell the user, offer the next step |

## 3. Verify the record against reality

The record can be stale (someone edited code, a session died mid-task):
- `git status` / `git log` since the last log entry — unexpected changes?
- Run the full suite: does it match the last logged result?
- A task logged `→` (started) but not `done`: inspect its files; the work may be
  half-applied. Finish it or reset its files — log which.
- Tools in `## Tools`: re-check any MCP auth.

Log `- <date> resumed at <phase/task> — <what you found>`.

## 4. Continue

Tell the user in two lines: where the build is, what you're doing next. Then
continue with the matching skill. Don't re-ask questions the spec already answers.
