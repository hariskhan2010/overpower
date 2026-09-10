# Working in this repo

## Use codegraph before reading source files

This repo has a persistent code graph at `codegraph-out/` (SQLite + reports),
built by the `codegraph` tool. **For any question about how the code is
structured, wired, or what a change affects, query the graph first — do not
start by reading source files.**

### First, make sure the graph is current

```
codegraph check-update .        # reports drift
codegraph update .              # fast, no LLM — run if it drifted
```

### Then answer from the graph

| Need | Command |
|---|---|
| Overview / map / "what is this repo" | read `codegraph-out/GRAPH_REPORT.md` |
| How one symbol works + its callers/callees | `codegraph context "<symbol>" .` |
| One node and its connections | `codegraph explain "<symbol>" .` |
| What breaks if I change X | `codegraph affected "<symbol>" .` |
| How A connects to B | `codegraph path "<A>" "<B>" .` |
| A general question | `codegraph query "<question>" .` |

`codegraph context` returns a symbol's body **plus every caller/callee signature
with `file:line`** — that is usually enough to make an edit with zero extra
file reads.

### When you may read a file directly

- To get the **exact current text** you are about to `Edit` (codegraph gives
  structure and signatures, not a live diff-ready copy).
- When `codegraph query` returns `No matching nodes found.` after one retry with
  key nouns only.
- For non-code files the graph does not cover well (raw JSON fixtures, binaries).

Reach for `Read` / `Grep` / `Glob` as the fallback, not the first move.

## Project notes

- overpower is a methodology **plugin** (mostly Markdown skills + small Python
  hooks). Tests: `python -m pytest -q`. Evals: `python evals/run_evals.py`.
- `codegraph-out/` and `evals/results/` are gitignored — regenerated, never committed.
- Commit trailer: `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
