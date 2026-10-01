# overpower skill-evals

The tests in `tests/` check the skill *files* are valid. These check the skills
*work* — they put a skill in front of a model with a realistic scenario and
assert the response follows the rule.

## Run

```
python evals/run_evals.py                 # all cases, deterministic checks only
python evals/run_evals.py --rubric         # also run the judge-model pass
python evals/run_evals.py tier-typo red-import-error-is-not-red
python evals/run_evals.py --model sonnet   # pin a model
```

Needs the `claude` CLI on PATH (present inside Claude Code). No API key — it uses
your logged-in session. Each case is one `claude -p` call (two with `--rubric`),
run `--restricted` with all tools disabled from a clean temp dir, so the model
can only respond with text and picks up none of this repo's settings.

Results land in `evals/results/<timestamp>.json` (git-ignored) with the full
response for every case.

## What each case pins

| Case | The claim it tests | superpowers issue |
|---|---|---|
| `tier-typo` | a one-word fix gets no plan/spec/subagents | #1120, #1152 |
| `tier-feature-forces-plan` | a multi-file feature routes into planning, not code | — |
| `tier-hidden-design-decision` | an unstated design choice escalates the tier | #1120 |
| `red-import-error-is-not-red` | a `ReferenceError` RED doesn't count; get the assertion to fail | #2146 |
| `fix-blast-radius-gate` | name a fix's consumers before editing | #2266 |
| `subagent-needs-real-agentid` | don't narrate a subagent result with no `tool_result` | #1749 |
| `findings-carried-not-deleted` | finishing carries open findings forward | #2253, #1075 |
| `worktree-greenfield-no-repo` | no repo → no `git worktree add`, work in place | #2242, #1108 |
| `brainstorm-reask-after-context-question` | answer the user's question, then re-ask yours | #1989 |
| `preflight-before-first-task` | an approved plan's assumptions are checked against the code before task 1 | — |
| `scout-maps-tools-to-tasks` | available MCP tools are mapped to the tasks that need them; unused ones named | — |

## Interpreting results

Model output varies run to run. A case that flaps between PASS and FAIL means
the skill's wording isn't strong enough for that scenario — tighten the rule
(that's `writing-skills`' job), re-run, and keep the case as the regression
guard. A case that fails consistently means the skill doesn't do what the
README claims — fix the skill or the claim.

These are a **signal, not a gate.** Don't block a commit on a 1-run eval; do
track the pass rate over time.
