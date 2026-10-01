---
name: doctor
description: Use when overpower doesn't seem to be working — skills not triggering, the session-start router missing, op-viewer showing wrong status, or a build stuck — diagnoses the install and the .overpower/ record and says exactly what to fix.
---

# doctor

Check in order; stop at the first failure and report the fix.

## 1. Is the plugin installed and enabled?

Use your harness's plugin list (Claude Code: `claude plugin list`; Codex,
Cursor, Gemini, Copilot, Kimi: their `/plugins` or `extensions list`).
`overpower` should be listed and enabled. If not, reinstall per the README's
**Install** section for your harness, then start a new session (plugins load
at session start). Harness with no plugin system → see `docs/any-agent.md`.

## 2. Did the router load?

In a fresh session, the context should contain an `<overpower>` block (from the
SessionStart hook). Missing →
- `node --version` works? The hook is a Node script.
- Run it by hand: `CLAUDE_PLUGIN_ROOT=<plugin dir> node <plugin dir>/hooks/session-start.js`
  — it must print one JSON object with `additionalContext`.
- Run the harness with its debug flag (Claude Code: `claude --debug`) and look
  for hook errors at startup. No hook support → the router loads from the
  rules file instead (GEMINI.md, AGENTS.md snippet).

## 3. Do the skills show up?

The available-skills list should include `overpower:build`, `overpower:preflight`,
etc. Missing one → its folder lacks `SKILL.md` or the frontmatter is malformed
(`---`, `name:`, `description:`, `---`).

## 4. Conflicts

- Another workflow plugin (e.g. a different planning/TDD suite) triggering on the
  same requests → disable one in your harness's plugin manager.
- A rules-file entry (CLAUDE.md / AGENTS.md / GEMINI.md) duplicating overpower's router → remove one copy.
- A loose `~/.claude/skills/overpower/` folder from before the plugin → remove it.

## 5. The `.overpower/` record

- op-viewer shows a task wrong → check the log line wording against
  `live-dashboard` (one task per line; `done` / `BLOCKED` / `→`).
- Run the parser directly: `node -e "import('<op-viewer>/src/parse.js').then(m=>console.log(m.parse({progress:require('fs').readFileSync('.overpower/progress.md','utf8')})))"`.
- Build stuck → `resume-build`.

## Report

What you checked, what failed, the exact fix (command or edit), and whether you
applied it.
