# Harness support

overpower's **method** — tiers, spec → architecture → plan → TDD → review →
finish, the `.overpower/` state model, the change-impact gate — works on **any**
coding agent that can read skill files. What varies is how much is *automatic*
vs. a rule you follow.

## The three capabilities

| | what it buys | without it |
|---|---|---|
| **skills mechanism** | the agent loads a skill on its own when the situation matches | you (or a rule) tell it to open `skills/<name>/SKILL.md` |
| **delegate** (sub-worker) | parallel tasks; a clean context per task; harder to fabricate a run | tasks run inline in sequence — slower, same discipline |
| **guard hook** (per-edit script) | an out-of-scope edit is *blocked*, so the scope-breach hard stop can't be skipped | the scope rule is followed by hand; `reviewing-changes` is the backstop |
| **session hook** | `using-overpower` is injected at session start + after compaction | a rules file or `AGENTS.md` carries the same pointer |

## Matrix

| Harness | Entry | skills | delegate | guard hook | session hook | Tier |
|---|---|---|---|---|---|---|
| **Claude Code** | `.claude-plugin/` (install as a plugin) | Skill tool | Task/Agent tool | PostToolUse (`hooks/enforce_scope.py`) | SessionStart | **A — full** |
| **Codex** (CLI / IDE) | `.codex-plugin/` or `AGENTS.md` | native skills | `spawn_agent` (multi-agent) | — | — | B |
| **Cursor** | `.cursor/rules/overpower.mdc` + `AGENTS.md` | read file | background agents | — | rule is always-on | B |
| **Gemini CLI** | `gemini-extension.json` → `GEMINI.md`, or `AGENTS.md` | read file | — | — | context file always-on | B |
| **Kimi Code** | `.kimi-plugin/` | Skill tool | Agent (`coder` / `explore` / `plan`) | — | `sessionStart` skill | B |
| **Devin CLI** | `.devin-plugin/` | native skills | background agents | — | — | B |
| **GitHub Copilot** | `.github/copilot-instructions.md` | read file | — | — | instructions always-on | C |
| **Aider** | `AGENTS.md` (or `--read`) | read file | — | — | — | C |
| **Jules / Zed / others that read AGENTS.md** | `AGENTS.md` | read file | varies | — | — | B/C |

- **Tier A** — every guarantee is automatic.
- **Tier B** — full method, delegates where the harness has them, scope + dispatch
  guarantees become disciplined rules that `reviewing-changes` checks.
- **Tier C** — the method as always-on rules; no delegates, no hooks. Still gets
  you tiers, TDD, the architecture step, the change-impact gate, durable state.

## The honest trade-off

Targeting many harnesses is why `obra/superpowers`' tracker is full of "works on
X, breaks on Y". overpower's answer: the **method is one set of files**, the
per-harness adapters are thin, and every guarantee that can't be automatic on a
harness is written as a rule a review step checks — not silently dropped. You
lose enforcement on Tier B/C; you don't lose the methodology.

If you only use Claude Code, install the plugin and ignore the rest.
