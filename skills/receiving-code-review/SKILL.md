---
name: receiving-code-review
description: Use when you get code review feedback (from a subagent, a tool, or a human) — verify each finding against the code before acting, fix what's real with a test, push back with evidence on what isn't, and report each outcome. No blind agreement, no defensiveness.
---

# receiving-code-review

A finding is a **claim**. Check it like any other claim.

## For each finding

1. **Understand it.** Restate the failure scenario in one line. Unclear → ask
   the reviewer (or the user, for a human's comment) before changing anything.
2. **Verify it.** Read the cited code. Try to trigger the scenario — ideally a
   failing test. Classify:
   - **Real** — reproducible or clearly correct reasoning.
   - **Not real** — the scenario can't happen (show why: the guard at `file:line`,
     the type, the caller contract).
   - **Taste** — valid opinion, no defect.
3. **Act.**
   - Real → failing test → fix → test passes → full suite still green.
   - Not real → don't change code. Write the evidence.
   - Taste → follow the repo's existing convention; if none, the user's call
     for anything non-trivial; nits are fine to just take.
   - Real but out of scope → `.overpower/findings.md`, tell the user.

## Report back

| Finding | Outcome | Evidence |
|---|---|---|
| Null deref in export.ts:52 | fixed | test "export with no rows" added |
| SQL injection in filter | not real | param binding at db.ts:30 |
| Rename `buildRpt` | taken | — |

## Tone

No "You're absolutely right!" — just verify and act. No defending code because
you wrote it. If a human reviewer and the evidence disagree, show the evidence
politely and let them decide. Don't silently skip any finding.
