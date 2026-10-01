# overpower in any AI coding agent

Harnesses with no plugin system (Aider, Windsurf, Cline, Roo, Continue, Zed,
JetBrains AI, …) can still run overpower: the skills are plain Markdown, and
every agent can read files. You give the agent one rule that points at them.

## 1. Get the skills

```
git clone https://github.com/<you>/overpower ~/overpower
```

## 2. Add the rule to your agent's rules file

Paste this into whichever file your agent reads every session:

| Agent | Rules file |
|---|---|
| Codex, Copilot, Cursor, Zed, many others | `AGENTS.md` in the repo (open standard) |
| Windsurf | `.windsurfrules` / global rules |
| Cline / Roo | `.clinerules` |
| Aider | `CONVENTIONS.md` (load with `--read CONVENTIONS.md`) |
| Continue | `.continue/rules/` |
| Anything else | its system prompt / custom instructions |

```markdown
## overpower
Before acting on any coding task, read ~/overpower/skills/using-overpower/SKILL.md
and follow it: size the task (T0–T3), then read and follow the skill it points
to from ~/overpower/skills/<name>/SKILL.md. T0 (obvious one-file fix): just do it.
Use the tool map's "No such tool" column for any action your agent lacks a tool for.
```

Use an absolute path if your agent doesn't expand `~`.

## What you lose without a plugin system

- No session-start hook — the rules file does the same job, as long as the
  agent reads it every session.
- No subagents in most of these agents — overpower runs every task inline,
  one at a time, with the same TDD/verify rules. Slower, same result.
- No structured questions — the agent asks numbered options in chat and waits.
