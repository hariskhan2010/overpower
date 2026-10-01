# AGENTS.md — overpower

This project uses the **overpower** build methodology. Any coding agent that
reads `AGENTS.md` (Codex, Cursor, Jules, Gemini CLI, Aider, Zed, and others)
picks it up from here.

## Do this first, every task

1. Read [`skills/using-overpower/SKILL.md`](skills/using-overpower/SKILL.md) and
   follow it. It classifies the task into a tier (T0 trivial → T3 program) and
   routes it to the right amount of process.
2. Load other skills by opening `skills/<name>/SKILL.md` when `using-overpower`
   or another skill names one.
3. If a session resumed or compacted: read `.overpower/progress.md` then
   `.overpower/findings.md` (if they exist) before continuing.

## The skills

`skills/`: `using-overpower`, `brainstorming`, `designing-architecture`,
`writing-plans`, `scouting-tools`, `using-git-worktrees`, `running-preflight`,
`executing-work`, `autonomous-execution`, `test-driven-development`,
`reviewing-changes`, `systematic-debugging`, `finishing-work`,
`watching-the-build`, `writing-skills`.

## What overpower assumes about your harness

overpower is harness-neutral. It uses three capabilities that differ between
agents — where a skill names one, read it per `using-overpower` → **Vocabulary**:

- **skills mechanism** — how you load a skill. No dedicated tool? Just open the
  `.md` file.
- **delegate** — a sub-worker for one task. No delegates? Do tasks inline, in
  sequence. You lose parallelism, not the discipline.
- **guard hook** — a script that blocks an out-of-scope edit. No hooks? The
  scope rule is one you follow, and `reviewing-changes` checks it.

Per-harness detail and the feature matrix: [`SUPPORT.md`](SUPPORT.md).

## Commands

Where your harness has slash commands: `/op-build <what>`, `/op-resume`,
`/op-status` (see `commands/`). Where it doesn't, just tell the agent "build
this end-to-end with overpower" / "resume the overpower build" / "overpower
status".

## The non-negotiables (every harness)

- Classify the tier before doing anything. A typo is not a project.
- Never claim done without verifying — run it, show the output.
- Never act on a delegate result with no concrete run artifact.
- A green test suite is not proof a fix is safe.
- `.overpower/progress.md` is append-only; `.overpower/findings.md` is never
  truncated.
- Merge / push / delete / spend / any outward-facing action needs explicit
  user approval — always.
