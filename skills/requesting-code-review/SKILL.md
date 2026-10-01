---
name: requesting-code-review
description: Use when a build or significant change is complete and verified — gets an independent review of the diff against the spec (reviewer subagent, the harness's review command, or a human), with severity-ranked findings tied to file:line.
---

# requesting-code-review

You can't review your own blind spots. Get fresh eyes, then judge what they find.

## When

- End of every T2/T3 build (after `verification-before-completion` passes).
- T1: a self-review pass is enough unless the change touches auth, money,
  data deletion, concurrency or a public API — then get a real review.
- Before any PR the user will merge.

## Pick the reviewer

| Situation | Reviewer |
|---|---|
| Default | this plugin's `reviewer` subagent |
| Want breadth / the user's standard flow | the harness's built-in review (Claude Code: `/code-review high`) |
| Security-sensitive | the harness's security review if it has one (Claude Code: `/security-review`) plus the reviewer |
| Team repo with a PR | a human, via the PR |

## Brief the reviewer

Give it what it needs, not your opinion of the code:
- The diff range: `git diff <base>...HEAD`
- SPEC.md (what it's meant to do) and architecture.md (intended shape)
- The test command and current result
- Specific worries, if any: "concurrency in the export stream", "error path when the DB times out"

Ask for: findings ranked by severity (**must-fix** = bug/security/data loss/
spec violation; **should-fix** = maintainability, missing tests; **nit**), each
with `file:line`, a concrete failure scenario, and a suggested fix. Ask it to
say plainly if it found nothing serious.

## Self-review pass (always, even with a reviewer)

Read your own diff top to bottom once as a stranger: does each hunk serve a
Must-do? Error paths handled? Names clear? Tests test behaviour? Anything
you'd be embarrassed to explain?

Then → `receiving-code-review` to process the findings.
