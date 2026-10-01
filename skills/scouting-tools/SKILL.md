---
name: scouting-tools
description: Use for a T2/T3 task while writing the plan. Finds the MCP servers, skills and CLIs actually available in this session and maps each useful one to the task that needs it, so no task is built by hand when a tool already does it.
---

# Scouting tools

The agent's tool list changes per user, per machine, per session. A plan written
from memory misses the database tool that could have checked the schema, or
loads a browser tool nobody needs. This step makes the tool choice deliberate
and visible: **task → tool**, every entry earning its place.

## 1. Inventory what exists — look, don't guess

- **Skills** — the ones your harness lists as available (and this repo's
  `skills/`).
- **MCP tools** — your tool list. If your harness keeps MCP tools deferred
  behind a search, search it with 3–5 keyword queries taken from the spec
  ("postgres schema", "figma frame", "browser screenshot", "issue tracker").
  Read each returned description; a tool's name is not its behavior.
- **CLIs on the machine** — `gh`, `docker`, `psql`, cloud CLIs, the project's
  own scripts. Check with `command -v <name>` (or `Get-Command` on Windows)
  only when a task would use one.
- **Delegates** — what sub-worker types your harness offers. None → every task
  is inline (see `using-overpower` → Vocabulary).

## 2. Map tools to tasks

For each task in the plan ask: is there a tool that makes this **more correct**
or **much faster** than writing code or doing it by hand?

| The task needs to… | Look for |
|---|---|
| read or change a database schema | a DB MCP server (describe tables, run SQL on a branch) |
| build from a design | a design-tool MCP server or design skill |
| check UI in a real browser | a browser-automation MCP server |
| call a third-party API correctly | its docs via fetch, or a docs MCP server |
| open PRs, read CI | `gh` |

## 3. Record it

In each task's block in `progress.md`, add a `Uses:` line (`—` if none). Then
append one summary to the log:

```
- <date-time> tools scouted — Neon MCP → Task 2 (schema check); gh → Task 6 (PR); considered, not used: browser MCP (no UI change)
```

"Considered, not used" matters: it shows the choice was made, not skipped.

## 4. Flag friction now, not mid-build

- A tool that needs **auth** → tell the user now, in one message, naming the task
  that needs it. `running-preflight` checks it actually works.
- A **destructive** tool (deletes, writes to production, spends money) → mark it.
  Using it needs explicit user approval at the moment of use, every time.
- A missing capability that would clearly help → say so, and what it would unlock.

## Anti-patterns

- ❌ loading every MCP tool "in case" — each one costs context and attention
- ❌ choosing a tool by its name without reading its description
- ❌ discovering mid-build that the tool needs a login the user isn't there to give
