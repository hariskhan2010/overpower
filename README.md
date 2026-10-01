# overpower

A plan-and-build workflow plugin for Claude Code. It gives the agent as much
process as a task needs — zero ceremony for a typo, a full spec → verified
plan → parallel build → review pipeline for a real feature.

## What's different

- **Proportional.** Every task is sized T0–T3 first. T0 fixes skip the process entirely.
- **Tool-scout.** Finds the MCP servers, skills and CLIs available in *your*
  session and maps each one to the task that needs it.
- **Preflight gate.** Before any code: baseline test run, every plan
  assumption checked against the real code and docs, every planned tool
  exercised, plan audited for coverage and dependencies.
- **Live dashboard.** Builds are recorded in `.overpower/`; run
  [op-viewer](../op-viewer) to watch tasks, findings and the architecture live.
- **Resumable.** `/clear`, a crash, a new day — `resume-build` picks up from the record.

## Install

One repo, every harness. The skills are plain `SKILL.md` files; each harness
gets a small manifest, and the session-start hook speaks each one's format.

| Harness | Install |
|---|---|
| **Claude Code** | `claude plugin marketplace add <repo>` then `claude plugin install overpower@overpower` |
| **Codex** (CLI / app) | `/plugins` → add marketplace `<repo>` (reads `.agents/plugins/marketplace.json`, `.codex-plugin/`). Enable `multi_agent` in `~/.codex/config.toml` for subagents. |
| **Cursor** | `/add-plugin <repo>` (reads `.cursor-plugin/`, hook `hooks/hooks-cursor.json`) |
| **Gemini CLI** | `gemini extensions install <repo>` (reads `gemini-extension.json` → `GEMINI.md`) |
| **GitHub Copilot CLI** | `copilot plugin marketplace add <repo>` then `copilot plugin install overpower@overpower` |
| **Qwen Code** | `qwen extensions install <repo>` (reads the Claude marketplace) |
| **Factory Droid** | `droid plugin marketplace add <repo>` then `droid plugin install overpower@overpower` |
| **Kimi Code** | `/plugins install <repo>` (reads `.kimi-plugin/`, includes a tool map) |
| **Devin CLI** | `devin plugins install <repo>` |
| **Anything else** (Aider, Windsurf, Cline, Continue, …) | one rule in its rules file — see [docs/any-agent.md](docs/any-agent.md) |

`<repo>` is a local path or `github-user/overpower`. Start a new session
after installing. The hook needs Node.

Status: Claude Code is installed and verified. The other manifests follow each
harness's published plugin format but have not been run in those harnesses yet.

## Use

Just ask: *"add CSV export to the reports page"*. Or call a skill directly:
`/overpower:build`, `/overpower:systematic-debugging`, `/overpower:preflight`, …

## Skills

| Skill | Use |
|---|---|
| `using-overpower` | Router, loaded every session — sizes the task, picks the skill |
| `build` | Whole pipeline for a T2/T3 change |
| `brainstorm-spec` | Fuzzy request → agreed SPEC.md, minimal questions |
| `research` | Where it lands, what to copy, what bites — cited |
| `tool-scout` | Map available MCP servers / skills / CLIs to tasks |
| `architecture` | Component diagram, interfaces, risks |
| `writing-plans` | Tasks with real deps, runnable Verify, inline-vs-subagent |
| `preflight` | Verify the plan against reality before coding |
| `test-driven-development` | RED → GREEN → REFACTOR, honestly |
| `executing-plans` | Run the plan in dependency waves |
| `dispatching-subagents` | When to spawn, the brief, checking results |
| `git-worktrees` | Isolated parallel work |
| `systematic-debugging` | Reproduce → localise → root cause → regression test |
| `verification-before-completion` | Evidence before "done" |
| `requesting-code-review` | Independent review against the spec |
| `receiving-code-review` | Verify each finding, fix or rebut with evidence |
| `finishing-branch` | PR / merge / keep / discard, close out |
| `resume-build` | Continue an interrupted build |
| `live-dashboard` | `.overpower/` format contract + op-viewer |
| `writing-skills` | Write and test skills |
| `doctor` | Diagnose the install and the record |

Agents: `reviewer` (read-only code review), `implementer` (one plan task, test-first).

## License

MIT
