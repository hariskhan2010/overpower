---
name: research
description: Use before designing or planning a change — maps where the change lands in the codebase, the patterns to copy, how tests run, and checks external docs/APIs you're not certain about. Produces cited findings, not opinions.
---

# research

Answer three questions with evidence: **Where does it land? What do we copy?
What could bite us?**

## Run these in parallel (one message)

**A. The codebase**
- If `codegraph-out/codegraph.db` exists: graph first — `codegraph query`,
  `codegraph context <symbol>`, `codegraph affected <symbol>`. Source files only
  to read exact text.
- Otherwise: Glob/Grep/Read. For a wide sweep in a big repo, one read-only
  explore subagent with "medium" breadth, asked for conclusions with `file:line`.
- Find: the entry points the change touches, the closest existing feature to
  copy (its file layout, naming, error handling, tests), how tests/build/lint run
  (package.json, Makefile, CI config), and what depends on code you'll change.

**B. External knowledge** — only for things you're not sure of
- Library/framework APIs the plan will call: check the **installed version**
  (lockfile) and read docs for that version (WebFetch the docs page, or the
  package's README/CHANGELOG). Training memory goes stale; versions drift.
- Third-party services: auth model, rate limits, error shapes.

**C. Prior art in the repo**
- `git log --oneline -- <area>` for recent changes and why; open issues/TODOs
  in the area; `.overpower/findings.md` from earlier builds.

## Write it down

Append to `.overpower/progress.md`:

```markdown
## Research
- Lands in: src/reports/export.ts:40 (`buildReport`) — called by routes/reports.ts:88
- Copy: src/reports/pdf.ts — same shape (stream + content-disposition), test in test/reports/pdf.test.ts
- Tests: `npm test` (vitest), ~40s; lint `npm run lint`
- Risk: `buildReport` is also used by the cron job (jobs/weekly.ts:12) — keep its signature
- Docs: csv-stringify v6 streaming API — https://csv.js.org/stringify/api/stream/ (installed 6.4.0)
```

Every bullet has a `file:line` or a URL. No bullet says "probably". If something
can't be determined, say so explicitly — that's a preflight item.
