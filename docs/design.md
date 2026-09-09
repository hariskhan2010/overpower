# overpower — design

## Goal

Make Claude Code build software the way a careful senior engineer does — spec
before code, plan before build, test before implementation, review before merge —
**without** the two things that make `obra/superpowers` fragile in practice:

1. **Cross-harness surface.** superpowers targets 14+ agents. Most of its
   platform bugs are "works on X, silently breaks on Y". overpower targets
   Claude Code and nothing else.
2. **Undifferentiated ceremony.** superpowers runs the full brainstorm → plan →
   subagent-review flow on every task. That is the top-voted complaint (#1120)
   and the cause of the token-budget blowouts (#1152). overpower sizes the task
   first.

## The tier model

`using-overpower` classifies every incoming request before doing anything:

| Tier | Looks like | Flow |
|---|---|---|
| **T0 trivial** | typo, rename, comment, one obvious line, a question | Just do it. Verify it. Done. No plan, no subagents, no state file. |
| **T1 small** | one function / one file, behavior is clear, no design decision | TDD (RED→GREEN→REFACTOR) + a self-review pass. No subagents. No plan file unless it spans >~3 steps. |
| **T2 feature** | multiple files, a design choice exists, "add X to the app" | Full flow: brainstorm (if the spec is fuzzy) → `writing-plans` → `executing-work` with subagents → `reviewing-changes` → finish. |
| **T3 program** | a roadmap, weeks of work, many features | T2 per feature, plus a persistent roadmap file the agent re-reads each session. |

Misclassifying **down** (treating a feature as small) is the expensive mistake,
so the rule is: **any design decision, any "it depends", any change touching
>2 files → at least T2.** When unsure between two tiers, pick the heavier and
say so in one line.

The user can always force a tier: "just do it" → T0/T1; "plan this properly" → T2.

## Durable state — `.overpower/`

Lives at the repo root, git-ignored by default (the user opts in to committing it).

```
.overpower/
  progress.md        append-only log: phase changes, task status, decisions
  findings.md        deferred / parked review findings — NEVER deleted mid-project
  roadmap.md         (T3 only) cross-session priorities
  archive/           finished progress/findings files, moved here by finishing-work
```

**Rules that fix superpowers #1075 / #2253 / #2267:**

- Every phase transition and every task status change is **appended** to
  `progress.md` with a timestamp. Nothing is rewritten in place.
- A review finding that is real but out of scope goes to `findings.md`
  immediately, with the task that found it. `findings.md` is only ever
  appended to or checked off — never truncated, never deleted.
- `finishing-work` moves the files to `archive/<date>-<branch>/`. It does not
  delete them. A project resumed after an interruption reads `progress.md` to
  learn where it was and `findings.md` to learn what it still owes.
- The files are plain Markdown a human can read and edit. No JSON, no tool
  dependency, survives compaction because the agent re-reads them.

## Verified subagent dispatch — fixes #1749

The failure: the orchestrator narrates a subagent's implementer/reviewer/user
exchange as prose without ever calling the Agent tool, and it self-reinforces.

overpower's `executing-work` makes fabrication structurally visible:

- Every subagent turn in `progress.md` records the returned **`agentId`** and the
  reported token usage. No `agentId` → the dispatch did not happen.
- The orchestrator is instructed: *"You may not summarize, quote, or act on a
  subagent result you cannot attribute to a real `agentId` from this session.
  If you're about to write what a subagent 'said' and there is no tool_result
  block above it, stop — you are hallucinating the run. Dispatch it for real."*
- A subagent that returns with an **unchanged working tree** is treated as a
  no-op (fixes the related #1701): the orchestrator re-dispatches with an
  explicit "the tree is unchanged, make the edit or report why you can't."

## RED for the right reason — fixes #2146

superpowers' TDD says RED must "fail because feature missing (not typos)". That
lets a missing-export error pass as RED while proving nothing.

overpower's rule: **the RED failure must be an assertion failure about the
behavior under test.**

- If RED fails with `X is not defined` / `cannot import` / a syntax error / a
  missing file — the test harness isn't wired yet. Fix that first, re-run, and
  only count RED once the failure is *"expected 3, got undefined"* shaped.
- Before GREEN, write one line in `progress.md`: *"RED: `<test>` fails with
  `<actual assertion failure>` — this is the behavior the code will provide."*
  If you can't write that line, you don't have RED.
- On a refactor there is **no RED** — the test must stay green. A refactor that
  turns a test red changed behavior; stop and decide if that was intended.

## Change-impact gate — fixes #2266

Before applying any fix to a review finding, `reviewing-changes` requires:

> Name the symbol the fix changes. List (a) every caller of it and what they do
> with its result, and (b) every thing it now depends on. If (a) or (b) has an
> entry you have not read this session, read it before editing. A green test
> suite is not evidence here — tests only cover what some consumer already
> checks.

The fix and a one-line impact note go to `progress.md` together.

## What overpower deliberately does NOT do

- No multi-harness support. No `.cursor-plugin`, no `.codex-plugin`.
- No telemetry.
- No mandated worktree for T0/T1 (superpowers #1108 / #2242: worktree setup
  crashes on greenfield and non-Poetry repos). T2+ uses one; the skill checks
  the repo state before touching it.
- No hard dependency on `TodoWrite` / `TaskCreate` (removed on current models,
  #2177). State lives in `.overpower/` files the agent reads directly.
