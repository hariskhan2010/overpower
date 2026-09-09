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

## The skills (10)

| Skill | Fires when | Does |
|---|---|---|
| `using-overpower` | session start / after compaction | Bootstraps; classifies the task tier |
| `brainstorming` | fuzzy T2/T3 request, before a plan | Idea → agreed spec, evidence-backed |
| `writing-plans` | a feature needs a plan | Verifiable tasks; opens the durable state file |
| `using-git-worktrees` | T2/T3, spec approved | Isolated workspace; checks repo state first |
| `executing-work` | a plan or a clear task exists | Tier-appropriate flow; verifies real subagent dispatch |
| `test-driven-development` | writing any implementation | RED-for-the-right-reason → GREEN → REFACTOR |
| `reviewing-changes` | between tasks / before a fix | Reviews against the plan **and** traces each fix's blast radius |
| `systematic-debugging` | a test fails / a bug appears | Reproduce → locate → **explain** → fix → record |
| `finishing-work` | tasks done and reviewed | Verify, merge decision, **archive** state (never delete) |
| `writing-skills` | creating/editing a skill | Keeps skills valid and consistent |

## Status

**v0.2 — the full skill set, not yet battle-tested.** The 10 skills, the
skeleton, the state model. The structural pieces (Claude-Code-only, the hook,
append-only state, the lint tests) are done and verified. The behavioral pieces
(the agent actually classifies tiers, runs the change-impact gate, won't
fabricate subagents) are written into the skills but need real sessions to
confirm — that's the open work, a skill-eval harness. Treat it as a working
draft you tune to how you work; that is the point of owning it rather than
installing a product.

## License

MIT. Not affiliated with obra/superpowers or Prime Radiant. The comparison table
cites their public issue tracker; the skill content here is original.
