---
name: live-dashboard
description: The .overpower/ file-format contract that op-viewer reads, and how to show the user a live dashboard of a build. Use whenever writing progress.md, findings.md or architecture.md, or when the user wants to watch progress.
---

# live-dashboard

`op-viewer` (zero-dependency Node app) polls `.overpower/` every 2s and renders
the build: tasks with status, findings, the architecture diagram, a progress bar.
Its parser is tolerant but literal — these formats are a contract.

## Watching

```
op-viewer                     # in the repo root (reads ./.overpower)
op-viewer path/to/.overpower --port 4199 --no-open
```
If `op-viewer` isn't installed: `git clone` it and `npm link` in its folder,
or run `node <op-viewer>/bin/op-viewer <dir>`. Tell the user this once per build —
they run it in a separate terminal (or via the harness's shell-escape, e.g. `! op-viewer` in Claude Code).

## progress.md — what the parser reads

| Field | Format | Notes |
|---|---|---|
| Feature | first `# Heading` | |
| Branch | line `Branch: <name>` | |
| Tier | line `Tier: T0`–`T3` | |
| Worktree | log line `- ... worktree <path> on <branch>` | |
| Tasks | `### Task <n> — <title>` | em dash, hyphen or colon |
| Status | log lines under `## Log` naming `Task <n>` | rules below |

Status rules, per task, from log lines that mention `Task <n>`:
- line contains `BLOCKED` → **blocked** (wins over everything)
- line contains the word `done` → **done**
- line `Task <n> →` (or `->`) → **in-progress**
- otherwise → **pending**

So: one task per log line. **Never** write `Task 3 done` inside a line about
another task, and don't mention a task number in prose lines that aren't about
its status ("unlike Task 2..." in a Task 5 line would attach the line to Task 2).

Canonical log lines:
```
- 2026-10-02 Task 3 → subagent implementer
- 2026-10-02 Task 3 (export endpoint) done — verify: npm test -- export → 6 passed
- 2026-10-02 Task 4 BLOCKED — needs Neon auth
- 2026-10-02 worktree ../app-export on feat/export
- 2026-10-02 preflight passed — baseline 412/415; 9 assumptions checked; tools ok: Neon, gh
```

## findings.md

```
# Deferred findings — <feature>

- [ ] Task 3: export ignores timezone on dates — src/reports/export.ts:61
- [x] flaky test in auth.test.js — fixed in a8c2e1f
```
`- [ ]` open, `- [x]` resolved. A `Task <n>` mention links it to that task.
Append only; check off, never delete.

## architecture.md

Only the **first** ```mermaid block is rendered. Put the component map first.

## Writing safely

The viewer reads while you write. Append to the log with small edits; never
rewrite progress.md wholesale mid-build.
