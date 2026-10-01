# overpower

A build methodology for coding agents. It is a response to
[`obra/superpowers`](https://github.com/obra/superpowers) — same idea (skills
that make the agent work like a disciplined engineer), built to sidestep the
failure classes that fill superpowers' issue tracker.

**Runs on any agent that reads skill files.** Full automation on **Claude Code**
(a plugin, with hooks and delegates); on Cursor, Codex, Gemini CLI, Copilot,
Aider and anything that reads `AGENTS.md`, the *method* is identical and the
guarantees that can't be automatic become rules a review step checks — see
[`SUPPORT.md`](SUPPORT.md).

## What's different

| superpowers pain (issue) | overpower's answer |
|---|---|
| Breaks across 14 harnesses; hooks misfire per-platform (#2105, #2252, #1108, #2197, #2083) | **One set of skill files, thin per-harness adapters.** Every guarantee that can't be automatic on a harness is written as a rule `reviewing-changes` checks — not silently dropped. |
| Still instructs removed `TodoWrite` / `Task*` tools (#2177) | No reliance on any removed or harness-specific tool. State lives in `.overpower/` files the agent reads directly. |
| Full ceremony on trivial tasks; token-budget blowouts (#1120 +16, #1152) | **Adaptive process weight.** The agent sizes the task first: a typo is not a project. |
| Orchestrator fabricates fake subagent runs (#1749) | **Verified runs.** A delegate's result counts only with a concrete artifact — a result block, a run id, a new diff on disk. No artifact → run it, or do it inline. |
| "Finish" deletes deferred findings; interrupts lose state (#1075 +11, #2253, #2267) | **`.overpower/` state is durable.** Append-only, survives compaction and interruption; finishing archives, never deletes. |
| Review-fixes create new bugs, nothing traces blast radius (#2266) | **Change-impact gate.** Before applying a fix you name the callers and dependencies of what you changed. |
| RED passes for the wrong reason (#2146) | RED must fail **for the stated behavioral reason**, not an import/typo/missing-export error. |
| Telemetry on by default | **None.** |

## Install

- **Claude Code:** `/plugin marketplace add <this-repo>` then
  `/plugin install overpower` — full automation (session hook, delegates,
  per-edit scope guard).
- **Cursor:** the repo's `.cursor/rules/overpower.mdc` applies automatically.
- **Codex:** add this repo as a plugin marketplace (`/plugins`) — reads
  `.codex-plugin/`. Or nothing at all: `AGENTS.md` routes it too.
- **Gemini CLI:** `gemini extensions install https://github.com/hariskhan2010/overpower`
  (reads `gemini-extension.json` → `GEMINI.md`).
- **Kimi Code:** `/plugins install https://github.com/hariskhan2010/overpower`
  (reads `.kimi-plugin/`, with overpower's vocabulary mapped to Kimi's tools).
- **Devin CLI:** `devin plugins install hariskhan2010/overpower`.
- **Aider / Jules / Zed / anything that reads `AGENTS.md`:** nothing to
  install — `AGENTS.md` routes the agent to the skills.
- **GitHub Copilot:** `.github/copilot-instructions.md` applies automatically.

Feature matrix per harness: [`SUPPORT.md`](SUPPORT.md).

## Autonomous mode

`/op-build <what to build>` (or just "build this end-to-end with overpower")
runs the whole flow — spec, plan, then an **autonomous loop** that runs
`op-implementer` and `op-reviewer` (delegated where the harness has delegates,
inline otherwise), task by task without stopping to ask at every step. It stops
only at a **hard stop**:

- an edit landed outside the worktree (a hook blocks it on Claude Code; a
  checked rule everywhere else)
- a task failed review twice
- a task needs a design decision the spec didn't make
- green tests went red and one debug pass didn't fix them
- a task needs a new dependency
- anything **irreversible or outward-facing** — `git push`, merge to main,
  delete, a network call with side effects, spending money — *always* needs
  explicit approval

`/op-resume` continues an interrupted build from `.overpower/`. `/op-status`
reports without changing anything.

## The skills (15)

| Skill | Fires when | Does |
|---|---|---|
| `using-overpower` | session start / after compaction | Bootstraps; classifies the task tier |
| `brainstorming` | fuzzy T2/T3 request, before a plan | Idea → agreed spec, evidence-backed |
| `designing-architecture` | spec agreed, before the plan | **Diagrams** where each part sits, its colour, what it does, what it talks to → `architecture.md` |
| `writing-plans` | architecture agreed | Verifiable tasks that reference `architecture.md`; opens the durable state file |
| `scouting-tools` | while writing the plan | Maps the MCP servers / skills / CLIs this session **actually has** to the tasks that need them |
| `using-git-worktrees` | T2/T3, spec approved | Isolated workspace; checks repo state first |
| `running-preflight` | plan approved, before any code | Checks every assumption in the plan against the real code, docs and tools — **no code until it passes** |
| `executing-work` | a plan or a clear task exists | Tier-appropriate flow; verifies real subagent dispatch |
| `autonomous-execution` | "build it all" / `/op-build` | The driver loop + hard-stop guardrails |
| `test-driven-development` | writing any implementation | RED-for-the-right-reason → GREEN → REFACTOR |
| `reviewing-changes` | between tasks / before a fix | Reviews against the plan **and** traces each fix's blast radius |
| `systematic-debugging` | a test fails / a bug appears | Reproduce → locate → **explain** → fix → record |
| `finishing-work` | tasks done and reviewed | Verify, merge decision, **archive** state (never delete) |
| `watching-the-build` | writing `.overpower/` | The line formats the [op-viewer](https://github.com/hariskhan2010/op-viewer) live dashboard reads |
| `writing-skills` | creating/editing a skill | Keeps skills valid and consistent |

## Status

**v0.7 — 15 skills, tool scouting, preflight before code, autonomous mode, runs on any agent that reads skill files
(not just Claude Code).** Structural pieces verified by `tests/`; behavioral
pieces by `evals/` — a harness that runs each skill against a real model on its
target scenario. Still a working draft you tune to how you work — that is the
point of owning it rather than installing a product — but the claims above are
demonstrated, not asserted. Used on 4 real builds so far; not yet published.

### Verify

```
python -m unittest discover -s tests   # 40 file-validity tests — instant
python evals/run_evals.py              # 16 behavioral cases — ~3 min
python evals/run_evals.py --rubric     # + a judge-model pass
```

## License

MIT. Not affiliated with obra/superpowers or Prime Radiant. The comparison table
cites their public issue tracker; the skill content here is original.
