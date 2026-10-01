---
name: watching-the-build
description: Use whenever you write to .overpower/ or the user wants to watch a build. The exact line formats the op-viewer dashboard reads, and how the user opens it.
---

# Watching the build

`op-viewer` is a zero-dependency Node dashboard that polls `.overpower/` every
2 seconds and shows the build live: tasks and their status, open findings, the
architecture diagram, a progress bar. It only reads — it never writes.

Its parser is tolerant but literal. These formats are the contract.

## Opening it

```
op-viewer                          # from the repo root; reads ./.overpower
op-viewer path/to/.overpower --port 4199 --no-open
```

Not installed → clone `op-viewer`, run `npm link` in it (or run
`node <op-viewer>/bin/op-viewer <dir>`). Tell the user this **once per build**,
when `progress.md` is first opened: they run it in a second terminal.

## What it reads from `progress.md`

| Shown as | Write it as |
|---|---|
| feature name | the first `# Heading` |
| branch | a line `Branch: <name>` |
| tier badge | a line `Tier: T2` (T0–T3) — put it under `Branch:` |
| worktree | the log line `- … worktree <path> on <branch> …` (from `using-git-worktrees`) |
| a task | a heading `### Task <n> — <title>` |
| task status | log lines that name the task |

Status, per task, from the log lines that name it:

- a line containing `BLOCKED` → **blocked** (beats everything)
- a line containing `done` → **done**
- a line `Task <n> →` → **in progress**
- no line yet → **pending**

So:

- **Log each task on its own line, when it happens.** The user may be watching;
  one summary line at the end leaves the board stale for the whole build.
  (Ranges like `tasks 1–4 done` are read, but they arrive late.)
- Don't name another task in a status line ("unlike Task 2…" inside a Task 5
  line attaches the line to Task 2 as well).

The lines `executing-work` already writes are exactly right:

```
- <date-time> Task 4 → op-implementer run=<id-or-"inline"> — <one-line result>
- <date-time> Task 4 done — verify: <command> → passed
- <date-time> Task 5 BLOCKED — <why, what's needed>
```

## `findings.md`

`- [ ] <text>` open, `- [x] <text>` resolved. A `Task <n>` in the text links the
finding to that task. Append-only, as `writing-plans` set it up.

## `architecture.md`

Only the **first** fenced `mermaid` block is drawn — put the component map first
(`designing-architecture` does).

## Writing safely while it watches

Append with small edits. Never rewrite `progress.md` wholesale mid-build — it's
append-only anyway, and a reader may catch a half-written file.
