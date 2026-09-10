# Working in this repo

## Answer code questions FROM THE GRAPH, not the codebase

This repo has a persistent code graph at `codegraph-out/`, built by the
`codegraph` tool. It is the source of truth for how the code is put together.

**Hard rule:** when the user asks how something *works*, where something *is*,
how the *architecture* is laid out, or what a change *affects* — your FIRST
action is a `codegraph` command or reading a file inside `codegraph-out/`.
Do **not** open, `Grep`, or `Glob` the source tree to answer these. `codegraph
query` reads `codegraph-out/codegraph.db` — that already *is* "reading the
codegraph folder".

### Worked example

User: *"How does the authentication system work?"*

Do this:
1. `codegraph query "how does the authentication system work" .`
2. If thin, `codegraph context "<the main auth symbol it named>" .` and read
   `codegraph-out/GRAPH_REPORT.md` for where it sits.
3. Answer from that subgraph, citing `source_file:line` from the output.

Do **NOT** do this: `Grep "auth"`, open `src/auth/*.py`, then summarize.

### Keep the graph current first

```
codegraph check-update .        # reports drift
codegraph update .              # fast, no LLM — run if it drifted
```

### Commands

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

### The ONLY times you open a source file first

1. You have already located the symbol via codegraph and now need its **exact
   current text** to `Edit` it.
2. `codegraph query` returned `No matching nodes found.` even after retrying with
   just the key nouns.
3. The target is a file the graph does not model (raw JSON fixtures, binaries,
   generated output).

In every other case: graph first, source second.

## Project notes

- overpower is a methodology **plugin** (mostly Markdown skills + small Python
  hooks). Tests: `python -m pytest -q`. Evals: `python evals/run_evals.py`.
- `codegraph-out/` and `evals/results/` are gitignored — regenerated, never committed.
- Commit trailer: `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
