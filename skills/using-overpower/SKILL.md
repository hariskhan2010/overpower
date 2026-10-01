---
name: using-overpower
description: Router for the overpower skills. Loaded at session start. Use it to decide which overpower skill fits the task in front of you — and, just as important, when none is needed.
---

# Using overpower

overpower is a set of skills for building software well. The point is
**proportion**: as much process as the task needs, never more. A typo fix gets
zero ceremony; a cross-cutting feature gets a spec, research, a verified plan,
parallel subagents and a review.

## Step 1 — size the task (always, silently, in one breath)

| Tier | Shape | Process |
|---|---|---|
| **T0** | Obvious fix, 1 file, no design choice | Just do it. Run the relevant test. No skills, no `.overpower/`. |
| **T1** | 1–4 small tasks in one area | `writing-plans` (short, inline spec; one log line per task) → `test-driven-development` → `verification-before-completion` |
| **T2** | 3–8 tasks, several files or areas | Full pipeline below |
| **T3** | Big, risky, cross-cutting, unfamiliar stack, or data at stake | Full pipeline + `git-worktrees` for parallel work + deep `research` + second-opinion review |

When unsure between two tiers, pick the lower one and move up if the work
surprises you. Say the tier and one line of why when it's T1+.

## Step 2 — pick the skill

| Situation | Skill |
|---|---|
| "Build / add / change X" (T2/T3) | `build` — runs the whole pipeline |
| Request is fuzzy, goals unclear | `brainstorm-spec` |
| Need to understand code, docs, or an API before deciding | `research` |
| Which MCP servers / skills / tools would help here? | `tool-scout` |
| Design the shape of the change | `architecture` |
| Turn a spec into tasks | `writing-plans` |
| About to write code from a plan | `preflight` — **mandatory gate** for T2/T3 |
| Writing any production code | `test-driven-development` |
| Running a plan task by task | `executing-plans` |
| Several independent tasks / a big isolated chunk | `dispatching-subagents` |
| Parallel work on the same repo | `git-worktrees` |
| A bug, failing test, or surprising behaviour | `systematic-debugging` |
| About to say "done", "fixed", "passing" | `verification-before-completion` |
| Work is finished, want eyes on it | `requesting-code-review` |
| Got review feedback (human or agent) | `receiving-code-review` |
| Branch is done — merge / PR / clean up | `finishing-branch` |
| `.overpower/progress.md` exists, or a session was interrupted | `resume-build` |
| Writing to `.overpower/` or the user wants to watch | `live-dashboard` |
| Creating or editing a skill | `writing-skills` |
| overpower itself seems broken or isn't triggering | `doctor` |

Load the skill (see **load a skill** in the tool map below) and follow it.

## Rules

1. **Proportion over ritual.** Never run T2 process on a T0 task. Never skip
   `preflight` or `verification-before-completion` on T2/T3 — those two are
   where builds actually fail.
2. **Evidence over claims.** Anything you report as working, you ran this turn.
3. **The user's instructions win.** The project's agent rules file (AGENTS.md, CLAUDE.md, GEMINI.md, …), explicit requests, and "just do it"
   override these skills. If the user says skip the spec, skip it.
4. **Questions are for the user's decisions only.** Scope, UX, irreversible trade-offs.
   Everything with a sensible default: decide, write it down, move on.
5. **Tools follow tasks.** Load an MCP tool or skill because a task needs it, not
   "in case".

## Tool map — overpower runs in many harnesses

Skills name **actions**, not tool names. Use your harness's tool for each.
Trust the tools you actually have over this table.

| Action | Claude Code | Codex | Gemini CLI | Cursor | Copilot CLI | Kimi Code | No such tool |
|---|---|---|---|---|---|---|---|
| **load a skill** | `Skill` (`overpower:<name>`) | native skills | read `skills/<name>/SKILL.md` | native skills | native skills | `Skill` | read `skills/<name>/SKILL.md` |
| **ask the user** (structured) | `AskUserQuestion` | ask in chat | ask in chat | ask in chat | ask in chat | `AskUserQuestion` | numbered options in chat, then stop and wait |
| **dispatch a subagent** | `Agent` (types: `Explore`, `Plan`, `general-purpose`, `overpower:implementer`, `overpower:reviewer`) | `spawn_agent` (needs `multi_agent` enabled) | — | its agent/task tool if present | its agent tool if present | `Agent` (`coder`, `explore`, `plan`) | do the task inline |
| **isolated subagent** | `Agent` with `isolation: "worktree"` | create a worktree yourself | — | — | — | — | `git worktree add` yourself (see `git-worktrees`) |
| **find tools** (deferred MCP) | `ToolSearch` | tool list | `/mcp` list | tool list | tool list | tool list | use what's listed |
| **todo list** | `TaskCreate`/todo tool | plan tool | — | todo tool | — | `TodoList` | `.overpower/progress.md` is the list |

Files, search, shell and web: use the harness's read/edit/write, grep/glob,
shell and fetch/search tools by their real names.
