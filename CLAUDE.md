# Working in this repo

## codegraph

The "answer code questions from the graph, not the codebase" rule lives in the
**global** `~/.claude/CLAUDE.md` and applies here — this repo has
`codegraph-out/codegraph.db`. In short: for any structure / wiring / impact
question, run `codegraph query|context|affected|explain` or read
`codegraph-out/GRAPH_REPORT.md` before touching source files.

Repo-specific: the graph drifts on every commit — run `codegraph update .`
first. `report.md` shows up as a few noisy doc communities; ignore them.

## Project notes

- overpower is a methodology **plugin** (mostly Markdown skills + small Python
  hooks). Tests: `python -m pytest -q`. Evals: `python evals/run_evals.py`.
- `codegraph-out/` and `evals/results/` are gitignored — regenerated, never committed.
- Commit trailer: `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`.
