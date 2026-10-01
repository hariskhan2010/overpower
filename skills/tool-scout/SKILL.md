---
name: tool-scout
description: Use when planning work that might benefit from MCP servers, skills, plugins or CLIs — finds what's actually available in this session, maps each useful one to the task that needs it, and flags auth needs early. Prevents both "forgot we had a tool for that" and loading tools nobody uses.
---

# tool-scout

Goal: a short, honest map from **task → tool**. Every entry earns its place.

## 1. Inventory what exists (don't guess)

- **Skills:** the skills your harness lists as available.
- **MCP tools:** your tool list. If your harness defers MCP tools behind a
  search (see **find tools** in the tool map), search it with keywords from the spec — try 3–5 queries
  (`"postgres sql"`, `"figma design"`, `"browser screenshot"`, `"slack message"`,
  `"issue tracker"`). Read returned descriptions; don't assume from names.
- **CLIs on the machine:** `gh`, `docker`, `psql`, cloud CLIs, the project's own
  scripts — check with `command -v` / `Get-Command` when a task would use one.
- **Subagent types:** whatever agent types your harness offers (none → all work is inline).

## 2. Map to tasks

For each Must-do / likely task, ask: is there a tool that makes this **more
correct or much faster** than writing code or doing it by hand?

| Need | Typical fit |
|---|---|
| Inspect/migrate a database | DB MCP (schema describe, run SQL on a branch) |
| Implement from a design | design MCP / design skill |
| Verify UI in a real browser | browser-automation MCP |
| Charts / dashboards | dataviz skill |
| Office docs, PDFs | the matching document skill |
| Library docs | WebFetch, a docs MCP |
| Repo/PR/CI | `gh` CLI |

## 3. Write the map

Append to `.overpower/progress.md`:

```markdown
## Tools
- MCP `Neon` (describe_table_schema, run_sql) → Task 2 schema check — needs project_id; auth ok
- skill `dataviz` → Task 4 chart
- CLI `gh` → Task 6 open PR
- considered, not used: `claude-in-chrome` — no UI in this change
```

The "considered, not used" line matters: it shows you looked.

## 4. Flag friction now

- Tools needing auth (`*__authenticate`): tell the user now, in one message, which
  task needs it. `preflight` will verify it works.
- Destructive tools (deletes, prod writes): mark them; they need explicit user
  approval at the moment of use, never autonomously.
- Missing capability that would clearly help: say so, with what it would unlock.
