# overpower

A build methodology for **Claude Code**, packaged as a plugin. It is a response
to [`obra/superpowers`](https://github.com/obra/superpowers) — same idea (skills
that make the agent work like a disciplined engineer), narrower target, and
built to sidestep the failure classes that fill superpowers' issue tracker.

## What's different

| superpowers pain (issue) | overpower's answer |
|---|---|
| Breaks across 14 harnesses; hooks misfire per-platform (#2105, #2252, #1108, #2197, #2083) | **Claude Code only.** One target, current primitives, no compatibility layer. |
| Still instructs removed `TodoWrite` / `Task*` tools (#2177) | Built against what Claude Code ships **now**; no reliance on removed tools. |
| Full ceremony on trivial tasks; token-budget blowouts (#1120 +16, #1152) | **Adaptive process weight.** The agent sizes the task first: a typo is not a project. |
| Orchestrator fabricates fake subagent runs (#1749) | **Verified dispatch.** Every subagent result must cite a real `agentId`; unverifiable = not dispatched. |
| "Finish" deletes deferred findings; interrupts lose state (#1075 +11, #2253, #2267) | **`.overpower/` state is durable.** Append-only, survives compaction and interruption; finishing archives, never deletes. |
| Review-fixes create new bugs, nothing traces blast radius (#2266) | **Change-impact gate.** Before applying a fix you name the callers and dependencies of what you changed. |
| RED passes for the wrong reason (#2146) | RED must fail **for the stated behavioral reason**, not an import/typo/missing-export error. |
| Telemetry on by default | **None.** |

## Install

```
/plugin marketplace add <this-repo>
/plugin install overpower
```

Or point Claude Code at a local checkout for development.

## The skills

| Skill | Fires when | Does |
|---|---|---|
| `using-overpower` | session start | Bootstraps the system; classifies the task tier |
| `writing-plans` | a feature needs a plan | Breaks work into verifiable tasks; opens the durable state file |
| `executing-work` | a plan or a task exists | Runs the tier-appropriate flow; verifies real subagent dispatch |
| `test-driven-development` | writing any implementation | RED-for-the-right-reason → GREEN → REFACTOR |
| `reviewing-changes` | between tasks / before finishing | Reviews against the plan **and** traces each fix's blast radius |

More skills (`brainstorming`, `systematic-debugging`, `using-git-worktrees`,
`finishing-work`, `writing-skills`) land as they're written and tested — see
[`CHANGELOG.md`](CHANGELOG.md).

## Status

**v0.1 — early.** The skeleton, the state model, and the five core skills.
Not yet exercised across a large range of real sessions. Treat it as a working
draft you tune to how you work — that is the point of owning it rather than
installing a product.

## License

MIT. Not affiliated with obra/superpowers or Prime Radiant. The comparison table
cites their public issue tracker; the skill content here is original.
