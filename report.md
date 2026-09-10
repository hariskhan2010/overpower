# Agent Memory Report

**Snapshot:** 2026-09-10

This report has two parts:

- **Part I — This project's agent memory.** A committed, human-readable dump of
  the Claude Code file-based auto-memory for `overpower` so it is visible on
  GitHub. Every memory reproduced verbatim, plus how the system works.
- **Part II — `agentmemory` (the tool).** A full setup / usage / configuration /
  troubleshooting guide for [`rohitg00/agentmemory`](https://github.com/rohitg00/agentmemory)
  — automatic persistent memory for AI coding agents (Claude Code, Cursor,
  Copilot CLI, …). This is a *different thing* from Part I: Part I is hand-written
  Markdown facts; Part II is a running service that captures memory from hooks.

---

# PART I — This project's agent memory

**Source:** Claude Code file-based auto-memory for this project
**Store location (outside the repo):** `~/.claude/projects/E--colibri-patner/memory/`

---

## 1. What "agent memory" is here

Claude Code keeps a **persistent, file-based memory** per project. It is not a
database and not model weights — it is a folder of plain Markdown files, one
fact per file, each with YAML-ish frontmatter.

| Piece | Role |
|---|---|
| `memory/MEMORY.md` | The **index**. One line per memory. This whole file is loaded into context at session start. |
| `memory/<slug>.md` | One **memory** = one fact. Frontmatter (`name`, `description`, `metadata.type`) + a body. |
| `description:` field | Used at recall time to decide whether the memory is relevant to the current task. |
| `[[other-slug]]` in a body | A link to another memory (may be forward-declared before that memory exists). |

### Memory types

| `metadata.type` | Meaning |
|---|---|
| `user` | Who the user is — role, expertise, preferences. |
| `feedback` | Guidance on how the agent should work (corrections + confirmed approaches), with the *why*. |
| `project` | Ongoing work, goals, constraints not derivable from code or git history. Relative dates converted to absolute. |
| `reference` | Pointers to external resources / environment facts (URLs, dashboards, hardware). |

### Maintenance rules the agent follows

- Before saving, check for an existing file that already covers the fact —
  update it rather than duplicate.
- Delete memories that turn out to be wrong.
- Do **not** store what the repo already records (code structure, past fixes,
  git history, `CLAUDE.md`) or what only matters to one conversation.
- Recalled memories are background context reflecting what was true when
  written — file/flag names are re-verified before being acted on.

### Trust / privacy note

These memories were written by the agent across sessions on this machine. They
contain project status, machine specs, and candid assessments — **no
credentials or secrets**. They are reproduced here because the repo owner asked
for them to be on GitHub.

---

## 2. The index — `MEMORY.md` (verbatim)

```markdown
# Memory index

- [overpower-project](overpower-project.md) — E:\colibri-patner: the user's own Claude Code build-methodology plugin (a better obra/superpowers); v0.6.1 (release hygiene done, clean to install locally), 4 real builds, codegraph built; methodology not yet proven end-to-end
- [codegraph-vs-graphify-test](codegraph-vs-graphify-test.md) — planned 2026-09-10: compare codegraph vs graphify on a heavily-dynamic codebase; how to run it fairly
- [dev-machine](dev-machine.md) — 2-core / 7.6 GB / no-GPU Windows 10 box; text/script work only, no local LLMs, PowerShell/WSL gotchas
```

Three memories are currently stored:

| Slug | Type | One-line |
|---|---|---|
| `overpower-project` | `project` | This repo — what it is, its design, its history, its honest state |
| `codegraph-vs-graphify-test` | `project` | A planned fair comparison of two codebase-graph tools |
| `dev-machine` | `reference` | Hardware ceiling of the machine and how to work within it |

---

## 3. Memory: `overpower-project` (type: `project`)

**Frontmatter**

```yaml
name: overpower-project
description: "overpower" — the user's own Claude Code build-methodology plugin, a better obra/superpowers
metadata:
  type: project
```

**Body (verbatim)**

> `E:\colibri-patner\` is **overpower**: the user's own version of
> `obra/superpowers` (the 283k-star agentic-skills plugin). Goal: "full like
> superpowers but more powerful and error-less." Git repo, branch `main`. (Built
> at `E:\overpower` then moved into the `E:\colibri-patner` working dir on the
> user's request — the folder name is legacy, the project is overpower.)
>
> **This project fits the [[dev-machine]]** (unlike an earlier abandoned colibri
> fork) — it's Markdown skill files + a Python hook + JSON config. No models, no
> compiling. Tests run with `python -m unittest discover -s tests` from `E:\overpower`.
>
> **Design (docs/design.md):** target **Claude Code only** (kills superpowers'
> biggest bug class — 14-harness breakage). Every skill fixes a specific
> superpowers issue:
> - `using-overpower` — task **tier** router (T0 trivial → T3 program). Fixes the
>   undifferentiated ceremony / token blowouts (#1120 +16, #1152).
> - `writing-plans` — opens durable append-only `.overpower/progress.md` +
>   never-truncated `findings.md`. Fixes lost-state (#1075, #2253, #2267).
> - `executing-work` — every subagent result must cite a real `agentId` or it
>   didn't happen. Fixes fabricated subagent runs (#1749).
> - `test-driven-development` — RED must fail on a behavioral **assertion**, not
>   an import/missing-export error. Fixes #2146.
> - `reviewing-changes` — change-impact gate: name a fix's callers + deps before
>   editing. Fixes fix-caused bugs (#2266).
>
> **Status (2026-09-09):** v0.1 `50179e9` → v0.2 `fc7ba06` → v0.3 `c85a267`
> (evals) → v0.4 `fe3e0e5` (autonomous) → **v0.5 `483d0ca` (architecture step)**.
>
> - **12 skills**. Added: `autonomous-execution` (driver loop + hard stops),
>   `designing-architecture` (diagrammed where/look/does/talks-to spec →
>   `.overpower/architecture.md`: mermaid component map + sequence diagram, ASCII
>   wireframe, element table Where|Look|Does|Data, states; colour from the
>   project's design tokens or marked "proposed").
> - **`commands/`** — `/op-build <what>`, `/op-resume`, `/op-status`.
> - **`agents/`** — `op-implementer`, `op-reviewer`.
> - **`hooks/enforce_scope.py`** — PostToolUse; blocks out-of-worktree edits
>   during a live `.overpower/` build; no-op otherwise.
> - **`tests/`** — 28 (`python -m unittest discover -s tests`).
> - **`evals/`** — 14 cases, `python evals/run_evals.py` (~4 min), `--rubric` adds
>   a judge pass. **14/14.** Runner: `shutil.which` for Windows `claude.CMD`,
>   prompt on stdin. Check patterns are deliberately tolerant — tighten when one
>   flaps, the skills are usually right.
>
> **Real builds with overpower (2026-09-09) — 4 so far, all completed cleanly:**
>
> `E:\tocgen\` — a Markdown TOC-generator CLI (no UI — tested the flow adapting
> when architecture has no layout). slug.js (GitHub anchors) + headings.js (fence
> stripping) + toc.js (pure applyToc) + cli.js (--check/--stdout/glob). 36 tests.
> Manual verify on its own README found a `locate()` bug (indexOf matched a prose
> mention of the marker); fixed in-session. Commit `482a66e` branch `master`.
>
> `E:\snip\` — a zero-dep Node snippet manager (search/tag/copy, atomic-write JSON
> store, tiny server + SPA). Full flow, TDD, 45 tests. Dogfooding caught 2 things
> unit tests missed: a spec gap in RED (substring tag match); and `filter.js`
> living in `src/` while the browser imports `/filter.js` served only from
> `public/` — client silently didn't load until opened in a browser. Commit
> `a520e97` branch `master`.
>
> `E:\op-viewer\` — a zero-dep Node dashboard that reads a repo's `.overpower/`
> and shows build status live (tier badge, task list colour-coded, findings,
> mermaid architecture inline, 2s poll). Spec → architecture (diagrammed) → plan
> (6 tasks) → TDD → review → finish. 35 node:test tests green. **Dogfooding found
> 3 real parser bugs** a unit test hadn't (worktree matched in prose; missing
> Tier line; done-detection too strict) — each fixed with a regression test. The
> dashboard was verified working in a browser (6/6 green, diagram rendered).
> op-viewer commits `8186e38`, `02ef682` on branch `master`.
>
> **v0.6 `5d00ee3` — multi-harness.** No longer Claude-Code-only. Harness-neutral
> vocabulary (skills mechanism / delegate / guard hook, each with a fallback);
> `AGENTS.md` (universal entry), `SUPPORT.md` (feature matrix, Tier A/B/C),
> `.cursor/rules/overpower.mdc`, `.github/copilot-instructions.md`;
> `session_start.py` emits per-harness JSON shapes. Claude Code stays Tier A
> (full automation). 37 tests, 14/14 evals.
>
> **v0.6.1 `1f26934` (2026-09-10) — release hygiene, no behaviour change.**
> plugin.json/marketplace.json had been stuck at `0.1.0` since the first release
> (the manifest test only checked the two JSONs against each other) — bumped to
> `0.6.1` and the test now asserts manifest version == newest CHANGELOG heading.
> README corrected: `v0.5`→`v0.6`, "not yet used on a real build"→"used on 4 real
> builds", stale counts `22`/`12`→`38`/`14`. `.gitignore` excludes `codegraph-out/`.
> 39 tests. Merged to `main` (ff). **Now clean to install locally:**
> `/plugin marketplace add E:\colibri-patner` then `/plugin install overpower@overpower`.
>
> **Honest state of the project (2026-09-10 review via codegraph):** it's ~90%
> Markdown; the only executable code is 3 tiny standalone Python scripts
> (`session_start.py`, `enforce_scope.py`, `run_evals.py`) + 7 test modules —
> 0% xref, no shared lib, no core code abstraction (God Nodes are all test
> classes). The evals test per-skill responses to scenarios, NOT end-to-end build
> quality with/without overpower — so "the methodology works" is still an
> unproven hypothesis with good scaffolding. Don't oversell it in the README.
>
> **Still open:** marketplace publishing; `origin` not set for either repo;
> growing the eval set + tracking pass-rate; more real builds; a real
> with/without-overpower comparison on the same task.
>
> Commit trailers: `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` +
> `Claude-Session: https://claude.ai/code/session_01B7bMYosgUC7jmpfhd1pEtX`.
> Use `git commit -F <file>` (PowerShell here-strings break on quotes).

### Notes on this memory

- Some lines are **superseded** and kept as history: the "Status (2026-09-09)"
  block stops at v0.5 and "`tests/` — 28" — the later v0.6 / v0.6.1 blocks carry
  the current numbers (37 → 39 tests). Read newest-block-wins.
- `[[dev-machine]]` links to the reference memory in §5.
- The "Honest state" paragraph is the agent's own candid assessment recorded
  after a 2026-09-10 review, not a claim from the project's docs.

---

## 4. Memory: `codegraph-vs-graphify-test` (type: `project`)

**Frontmatter**

```yaml
name: codegraph-vs-graphify-test
description: Planned comparison of codegraph vs graphify on a heavily-dynamic codebase
metadata:
  node_type: memory
  type: project
  originSessionId: 85599e43-91c9-486d-abe8-b2808b7111c9
  modified: 2026-09-09T19:08:22.983Z
```

**Body (verbatim)**

> The user plans (starting **2026-09-10**) to compare **codegraph** vs
> **graphify** on a **heavily-dynamic codebase** — the one case where AST parsing
> can't see the wiring and graphify's per-file LLM reasoning might catch edges
> codegraph misses.
>
> **Context from the 2026-09-09 session:** built a codegraph for the `overpower`
> project (E:\colibri-patner) — 271 nodes, mostly Markdown; xref_resolution was
> 0% (standalone scripts, no cross-imports) so it didn't exercise dynamic edges.
> Verdict reached: codegraph ~9/10 *with `--lsp` + a proper semantic pass*
> (it already has `--lsp`/`--scip` tiers AND an LLM `ambiguous_edges` field);
> graphify ~7/10 (slow, pricey, model-inferred structure). graphify only wins
> when the codebase is heavily dynamic AND `--lsp`/`--scip` aren't available.
>
> **For a fair test tomorrow:**
> - Pick a genuinely dynamic project: Django (signals, `apps.get_model`), a JS app
>   with an event bus / DI container, Ruby metaprogramming, a Spring/C# DI-heavy
>   app.
> - Run `codegraph extract <path> --lsp --semantic skill` (drive the semantic
>   step, actually fill `ambiguous_edges`) AND graphify.
> - Compare on the metric that matters: `codegraph affected "<dynamic symbol>"`
>   recall vs graphify's — do they find the reflection/signal/event edges?
> - Note cost: codegraph ~40-60k tokens for that repo's semantic pass; graphify
>   ~8-15x on a repo of similar size.

### Status as of this report (2026-09-10)

- The planned dynamic-codebase test has **not** been run. The working notes for
  it live at `codegraph-vs-graphify.md` in this repo (untracked; the file's own
  header says it does not need committing).
- The overpower repo's own codegraph *was* rebuilt on 2026-09-10:
  **288 nodes · 288 edges · 35 communities**, still `xref_resolution: 0%`
  (tier = tree-sitter), 100% `EXTRACTED` provenance.

---

## 5. Memory: `dev-machine` (type: `reference`)

**Frontmatter**

```yaml
name: dev-machine
description: Hardware limits of this dev machine and how to work within them
metadata:
  node_type: memory
  type: reference
  originSessionId: 8676b564-2188-4a30-b7d9-27756a913834
  modified: 2026-09-09T13:16:40.405Z
```

**Body (verbatim)**

> This machine (Windows 10) is a ~2015 ultrabook and constrains the workflow:
>
> - Intel i5-5200U — **2 cores / 4 threads**, AVX2 only
> - **7.6 GB total RAM** (often <1 GB free)
> - Intel HD 5500 — no usable GPU compute
> - Disk free: E: ~38 GB, C: ~13 GB
> - Build toolchain is **WSL2 Ubuntu-24.04** (has gcc 13.3 + OpenMP, python3.12).
>   Default WSL config now (no `.wslconfig`). Heavy multi-subprocess test suites
>   can OOM-crash the WSL VM — keep runs small.
>
> **Can do:** anything text/config/script-based; small compiles; individual unit
> tests; Python stdlib work. Good fit for [[overpower-project]] (Markdown + a
> Python hook).
>
> **Cannot do:** run local LLMs, large model inference, big parallel builds, or
> anything needing a GPU or >4 GB working set. A cloud box is required for that
> class of work.
>
> **PowerShell gotchas here:** here-strings (`@'...'@`) break on quotes/apostrophes
> — use `git commit -F <file>`. WSL-through-PowerShell mangles `$()`, `awk`,
> backticks — put non-trivial shell in a `.sh` file and run
> `wsl -d Ubuntu-24.04 -- bash /mnt/e/.../x.sh`. `>` redirect adds a UTF-8 BOM.

---

## 6. Memory graph

```
overpower-project ──[[dev-machine]]──> dev-machine
dev-machine ──[[overpower-project]]──> overpower-project   (bidirectional link)

codegraph-vs-graphify-test   (standalone — no [[links]], but shares the
                              "E:\colibri-patner" subject with overpower-project)
```

## 7. Cross-references outside the memory store

| Referenced from memory | What / where |
|---|---|
| `docs/design.md` | In this repo — the tier model + the superpowers issues each skill fixes |
| `codegraph-vs-graphify.md` | In this repo (untracked) — working notes for the planned tool comparison |
| `~/.claude/skills/codegraph/` | The codegraph skill (installed globally, v0.7.0) |
| Session `session_01B7bMYosgUC7jmpfhd1pEtX` | The session whose commit trailer convention is recorded |
| `E:\tocgen`, `E:\snip`, `E:\op-viewer` | The 4 real builds done with overpower (all on branch `master`, no `origin`) |

---

## 8. How to regenerate Part I

The memory store is at `~/.claude/projects/E--colibri-patner/memory/`. To refresh
this file, copy `MEMORY.md` and each `<slug>.md` body in verbatim and update the
snapshot date. There is no automated exporter — the store is meant to be read by
the agent, not published, so this report is a manual courtesy copy.

---

# PART II — `agentmemory` (the tool)

**Repo:** <https://github.com/rohitg00/agentmemory> · **28.3k ⭐** ·
**TypeScript/JS** · **Apache-2.0** · **1,674+ tests**
**Package:** `@agentmemory/agentmemory` (CLI) + `@agentmemory/mcp` (MCP shim)
**Tagline:** "#1 Persistent memory for AI coding agents based on real-world benchmarks"

> Everything below is transcribed from the project's README as of 2026-09-10.
> Verify against the repo before relying on version-pinned details (iii engine
> `v0.11.2`, default model names, etc.).

---

## 9. What it is (and how it differs from Part I)

`agentmemory` is a **running local service** that gives coding agents memory
across sessions. Instead of you re-explaining the codebase every session, it:

1. **Captures** the agent's tool use automatically (12 auto-capture hooks in
   Claude Code — zero manual effort).
2. **Compresses** raw observations into searchable memory.
3. **Injects** relevant context when a new session starts.

Works across 20+ agents: Claude Code, GitHub Copilot CLI, Cursor, Gemini CLI,
Codex CLI, Hermes, OpenClaw, pi, OpenCode, Zed, Continue.dev, Warp, and any MCP
client. Cross-agent memory is shared via MCP (opt into per-agent isolation with
`AGENTMEMORY_AGENT_SCOPE=isolated`).

| | Part I (this project's memory) | Part II (`agentmemory` tool) |
|---|---|---|
| Form | Hand-written `.md` files | SQLite + vector index, a daemon |
| Capture | Manual — the agent decides to write | Automatic — from hooks on every tool call |
| Scope | One project | Cross-project, cross-agent |
| Retrieval | Loaded whole at session start | Hybrid search (BM25 + vector + graph), token-budgeted |
| Runs anything? | No | Yes — a background server + real-time viewer |

### The 4-tier consolidation model (human-memory analogy)

| Tier | Content | Analogy |
|---|---|---|
| Working | Raw tool-use observations | Short-term memory |
| Episodic | Compressed session summaries | "What happened" |
| Semantic | Extracted facts and patterns (knowledge graph) | "What I know" |
| Procedural | Workflows and decision patterns | "How to do it" |

Memories **decay on an Ebbinghaus curve** — frequently accessed ones strengthen,
stale ones auto-evict.

---

## 10. Requirements

- **Node.js 20+** with `npm` and `npx`
- **macOS / Linux:** `curl`, POSIX `sh`, and `tar` (for automatic iii-engine install)
- **Native Windows:** must manually install pinned **iii-engine v0.11.2**
  (`iii.exe`), or use WSL2 / Docker Desktop — see §14
- iii-engine is fetched automatically on macOS/Linux; it is pinned to `v0.11.2`

> Note for this machine ([[dev-machine]] in Part I): 2 cores / 7.6 GB RAM, no GPU.
> agentmemory itself is light (SQLite + in-memory index), but **LLM-written
> compression** and **local embeddings** add load — keep `AGENTMEMORY_AUTO_COMPRESS`
> off or point it at a hosted model, and expect the first local-embedding request
> to download `Xenova/all-MiniLM-L6-v2`.

---

## 11. Installation

### Fresh install (interactive)

```bash
npx -y @agentmemory/agentmemory@latest
```

This interactive setup lets you: select which agents to connect, choose an LLM
provider (or stay keyless), seed the config, launch the memory server with its
pinned iii engine, and optionally install globally.

### Verify

```bash
npx -y @agentmemory/agentmemory@latest demo      # seeds sample sessions, tests recall
npx skills add rohitg00/agentmemory -y           # installs the skills (auto-detects agent)
curl http://localhost:3111/agentmemory/health    # should return OK
```

Real-time viewer: <http://localhost:3113>

### From source

```bash
git clone https://github.com/rohitg00/agentmemory.git && cd agentmemory
npm install && npm run build && npm start
```

---

## 12. Connecting agents

### Claude Code (this is the relevant one for overpower)

```bash
agentmemory                              # terminal 1: start the server, leave it running
```

Then inside Claude Code:

```
/plugin marketplace add rohitg00/agentmemory
/plugin install agentmemory
```

Registers **12 auto-capture hooks + 17 skills + 54 MCP tools**. Verify:

```bash
curl http://localhost:3111/agentmemory/health
```

### Native skills (works across 50+ agents, complements MCP)

```bash
npx skills add rohitg00/agentmemory -y            # auto-detect calling agent
npx skills add rohitg00/agentmemory -y -a warp    # explicit agent
npx skills add rohitg00/agentmemory -y -a '*'     # install to ALL agents
```

Skills tell the agent *when* to invoke memory tools; MCP wiring gives it the
tools. You generally want both.

### Cursor / Claude Desktop / Cline / Roo Code / Gemini CLI / OpenClaw

Merge into the existing `mcpServers` block (`~/.cursor/mcp.json` for Cursor):

```json
{
  "mcpServers": {
    "agentmemory": {
      "command": "npx",
      "args": ["-y", "@agentmemory/mcp"],
      "env": {
        "AGENTMEMORY_URL": "http://localhost:3111",
        "AGENTMEMORY_SECRET": "${AGENTMEMORY_SECRET}"
      }
    }
  }
}
```

### GitHub Copilot CLI

```bash
agentmemory connect copilot-cli                       # MCP-only
copilot plugin install rohitg00/agentmemory:plugin    # full plugin
```

### Codex CLI

```bash
codex plugin marketplace add rohitg00/agentmemory
codex plugin add agentmemory@agentmemory
```

Registers MCP + 6 lifecycle hooks (SessionStart, UserPromptSubmit, PreToolUse,
PostToolUse, PreCompact, Stop) + 17 skills. For **Codex Desktop** hook support
(currently silent — upstream issue #16430) also run:

```bash
agentmemory connect codex --with-hooks
```

### Other agents (quick reference)

| Agent | Command / note |
|---|---|
| Devin CLI | `agentmemory connect devin` (+ `--with-hooks` for 6 hooks) |
| OpenCode | top-level `mcp` key; 22 auto-capture hooks |
| Hermes | copy `integrations/hermes/` to `~/.hermes/plugins/agentmemory` |
| pi | `agentmemory connect pi` |
| Warp | `agentmemory connect warp` (skills auto-discovered from `.claude/skills/`) |
| Continue.dev | `agentmemory connect continue` (array form for `mcpServers`) |
| Zed | `agentmemory connect zed` (writes to `context_servers`, not `mcpServers`) |

---

## 13. Daily operations

### Commands

```bash
agentmemory                    # start the server
agentmemory stop               # stop cleanly
agentmemory status             # check health
agentmemory doctor             # interactive diagnostics
agentmemory connect <agent>    # wire another agent
agentmemory upgrade            # update runtime (mutates workspace)
agentmemory remove             # uninstall everything
```

### Ports

| Port | Purpose | Override env |
|---|---|---|
| 3111 | REST API, MCP HTTP, health checks | `III_REST_PORT` |
| 3112 | Internal streams worker | `III_STREAM_PORT` |
| 3113 | Real-time viewer | `III_VIEWER_PORT` |
| 49134 | WebSocket; worker registration | `III_ENGINE_PORT` |

`--port <N>` sets the REST anchor and derives the rest. `--instance 1` runs a
second daemon on 3211/3212/3213/49234.

### Storage location

| OS | Path |
|---|---|
| macOS | `~/Library/Application Support/agentmemory` |
| Linux | `$XDG_DATA_HOME/agentmemory` or `~/.local/share/agentmemory` |
| Windows | `%APPDATA%\agentmemory` |

Override: `--data-dir <path>` or `AGENTMEMORY_DATA_DIR`.

### Importing old Claude Code transcripts

```bash
npx -y @agentmemory/agentmemory@latest import-jsonl
npx -y @agentmemory/agentmemory@latest import-jsonl ~/.claude/projects/-my-project/abc123.jsonl
```

⚠️ Claude Code's `cleanupPeriodDays` (default **30**, in `~/.claude/settings.json`)
auto-deletes JSONL older than that. Run imports on a cron, raise the setting, or
just use the auto-capture hooks instead.

### The viewer (`http://localhost:3113`)

Live observation stream, two-pane session explorer, memory/lesson rows with full
JSON + provenance, knowledge graph, **session replay** (0.5x–4x), health
dashboard. Binds to `127.0.0.1`; bearer token required on protected endpoints
when `AGENTMEMORY_SECRET` is set.

---

## 14. Windows installation (3 options)

### Option A — prebuilt binary (recommended)

1. Download `iii-x86_64-pc-windows-msvc.zip` from
   <https://github.com/iii-hq/iii/releases/tag/iii%2Fv0.11.2>
2. Extract `iii.exe` to `%USERPROFILE%\.agentmemory\bin\iii.exe`
3. Verify: `& "$HOME\.agentmemory\bin\iii.exe" --version`  → should print `0.11.2`
4. Run: `npx -y @agentmemory/agentmemory@latest`

### Option B — Docker Desktop

```powershell
$env:AGENTMEMORY_USE_DOCKER = "1"
npx -y @agentmemory/agentmemory@latest
```

### Option C — standalone MCP (no engine)

```powershell
npx -y @agentmemory/agentmemory@latest mcp
```

MCP tools only — no REST API, viewer, or cron.

### Windows troubleshooting

| Symptom | Fix |
|---|---|
| Port in use | `netstat -ano \| findstr :3111`, then kill the PID |
| Engine not starting | re-run with `--verbose`; confirm `iii.exe` stays alive |
| Docker fallback skipped | make sure Docker Desktop is actually running |
| `.env` never loaded (integrations fail silently) | **known bug #1331** — `HOME` unset on Windows; set `HOME=%USERPROFILE%` |

---

## 15. Configuration

Config file: **`~/.agentmemory/.env`**. Providers are auto-detected from env vars.
LLM-written compression needs **both** a provider **and** `AGENTMEMORY_AUTO_COMPRESS=true`
(otherwise compression is synthetic/rule-based).

### LLM providers

| Provider | Config | Notes |
|---|---|---|
| Anthropic API | `ANTHROPIC_API_KEY=sk-ant-...` | per-token billing |
| Gemini | `GEMINI_API_KEY=...` | also enables embeddings |
| OpenAI API | `OPENAI_API_KEY=...` + `OPENAI_BASE_URL=...` | default `gpt-5.6-luna`; Azure via base URL |
| OpenRouter | `OPENROUTER_API_KEY=...` | multi-model proxy |
| Local (Ollama/LM Studio/vLLM) | `OPENAI_API_KEY=local` + base URL | zero cost |
| Claude subscription fallback | `AGENTMEMORY_ALLOW_AGENT_SDK=true` | opt-in only |

**Ollama:**

```bash
ollama pull qwen3:8b
ollama serve
```

```env
OPENAI_API_KEY=ollama
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_MODEL=qwen3:8b
```

**LM Studio:** start the local server, then:

```env
OPENAI_API_KEY=lmstudio
OPENAI_BASE_URL=http://localhost:1234/v1
OPENAI_MODEL=qwen3-8b
```

Recommended local compression models: `qwen3:8b` (5.2 GB, balanced),
`qwen3:4b` (2.6 GB, smallest), `qwen3-coder:30b` (19 GB, code).
→ On [[dev-machine]] (7.6 GB RAM) only `qwen3:4b` is realistic, and even that is tight.

### Embeddings

Keyless installs **disable vector embeddings** — `mem::search` falls back to
BM25. Enable free on-device embeddings:

```env
EMBEDDING_PROVIDER=local
```

First request downloads `Xenova/all-MiniLM-L6-v2`; then runs locally.

| Provider | Cost | Notes |
|---|---|---|
| Local | Free | on-device after model download |
| Gemini | Free tier | 100+ languages, 768/1536/3072 dims |
| OpenAI | $0.02 / 1M tokens | highest quality |
| Voyage AI | Paid | code-optimized |
| Cohere | Free trial | general |

### `.env` template

```env
# LLM provider (pick one)
# ANTHROPIC_API_KEY=sk-ant-...
# GEMINI_API_KEY=...
# OPENROUTER_API_KEY=...
# OPENAI_API_KEY=...
# OPENAI_BASE_URL=https://api.openai.com
# OPENAI_MODEL=gpt-5.6-luna

# Embedding provider
# EMBEDDING_PROVIDER=local
# OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Features
# AGENTMEMORY_AUTO_COMPRESS=false
# AGENTMEMORY_SLOTS=false
# AGENTMEMORY_REFLECT=false
# GRAPH_EXTRACTION_ENABLED=false
# CONSOLIDATION_ENABLED=false
# CLAUDE_MEMORY_BRIDGE=false

# Auth
# AGENTMEMORY_SECRET=your-secret

# Search tuning
# BM25_WEIGHT=0.4
# VECTOR_WEIGHT=0.6
# TOKEN_BUDGET=2000

# Multi-agent
# AGENT_ID=architect
# AGENTMEMORY_AGENT_SCOPE=isolated
# TEAM_ID=company
# USER_ID=engineering-team

# Tool visibility
# AGENTMEMORY_TOOLS=all
```

### Cost-aware model selection

Background compression is heavy (README example: 635 requests, 888K tokens over
35 hours):

| Model | $/1M in | $/1M out | Est. cost |
|---|---|---|---|
| DeepSeek V4 Flash | $0.07 | $0.14 | ~$0.07 |
| DeepSeek V4 Pro | $0.435 | $0.87 | ~$0.46 |
| Qwen3-Coder | $0.45 | $1.80 | ~$0.55 |
| Claude Sonnet 5 | $3.00 | $15.00 | ~$5.02 |

Premium-tier models print a cost warning; suppress with
`AGENTMEMORY_SUPPRESS_COST_WARNING=1`.

### Multi-agent / team scoping

```env
TEAM_ID=company
USER_ID=engineering-team
AGENT_ID=architect
AGENTMEMORY_AGENT_SCOPE=isolated   # "shared" (default) | "isolated"
```

- `shared` — tags writes with agent ID, recall **not** filtered (cross-agent visibility + audit trail)
- `isolated` — tags writes **and** filters recall by agent ID (strict separation)

Per-request override: `?agentId=<role>` or `?agentId=*`.

---

## 16. MCP surface

`@agentmemory/mcp` exposes **54 tools** only when it can reach a running server
via `AGENTMEMORY_URL`. With **no server**, it falls back to **7 local tools**:
`memory_save`, `memory_recall`, `memory_smart_search`, `memory_sessions`,
`memory_export`, `memory_audit`, `memory_governance_delete`.

Visibility modes: `AGENTMEMORY_TOOLS=core` (8 essentials) · `AGENTMEMORY_TOOLS=all`
(default, 54).

**17 skills** — 9 invocable: `/recall`, `/remember`, `/session-history`,
`/forget`, `/recap`, `/handoff`, `/lesson`, `/commit-context`, `/commit-history`
— plus 8 reference skills (memory discipline, MCP tools, REST API, config,
agents, hooks, architecture, skill authoring).

**6 resources** (status, project profiles, recent observations, latest memories,
graph stats, team profiles) · **3 prompts** (recall context, session handoff,
pattern detection).

### REST API

130 endpoints on port 3111. Bearer token required on protected endpoints when
`AGENTMEMORY_SECRET` is set. Key ones:

| Method | Path | Description |
|---|---|---|
| GET | `/agentmemory/health` | health check (always public) |
| GET | `/agentmemory/livez` | startup readiness probe |
| POST | `/agentmemory/session/start` | start session + get context |
| POST | `/agentmemory/session/end` | end session |
| POST | `/agentmemory/observe` | capture observation |
| POST | `/agentmemory/smart-search` | hybrid search |
| POST | `/agentmemory/remember` | save to long-term memory |
| POST | `/agentmemory/forget` | delete observations |
| GET | `/agentmemory/profile` | project profile |
| GET | `/agentmemory/export` | export all data |
| POST | `/agentmemory/import` | import from JSON |

---

## 17. How memory capture works internally

Raw observation → pipeline:

1. **SHA-256 dedup** (5-minute window)
2. **Privacy filter** — strips secrets, API keys, `<private>…</private>` tags
3. Raw storage
4. **Compression** — synthetic by default; LLM if provider + `AGENTMEMORY_AUTO_COMPRESS=true`
5. **Vector embedding** — when an embedding provider is active
6. **BM25 + vector indexing**

**Hybrid search** fuses three streams with Reciprocal Rank Fusion (k=60):

| Stream | Behavior | When |
|---|---|---|
| BM25 | stemmed keyword + synonym expansion | always |
| Vector | cosine similarity over dense embeddings | embedding provider configured |
| Graph | knowledge-graph entity traversal | entities detected in query |

Results are session-diversified (max 3 per session); superseded memory versions
excluded. BM25 handles Greek/Cyrillic/Hebrew/Arabic/accented Latin natively; CJK
needs `npm install @node-rs/jieba tiny-segmenter`.

---

## 18. Known issues (open as of 2026-09-10)

Pulled from <https://github.com/rohitg00/agentmemory/issues>. **Setup / MCP
issues are called out — read these before installing.**

| # | Title | Impact |
|---|---|---|
| **#1341** | `mem::summarize`: dead noop gate causes failure storm when no LLM key set | ⚠️ keyless installs — error storm on summarize |
| **#1340** | Viewer SPA dashboard flips between stats and "new install" hero under live capture | cosmetic / confusing |
| **#1339** | `graph/build` server-side batch loop outlives HTTP response; bulk backfill impossible on large graphs | ⚠️ can't backfill a big graph store |
| **#1338** | `createFallbackProvider` drops `baseURL` — custom-endpoint fallbacks hit wrong API host | ⚠️ **setup** — custom LLM endpoints misrouted |
| **#1335** | Shutdown index save lost to container teardown race; boot only reconciles empty index | ⚠️ **Docker** — data-persistence loss |
| **#1334** | `/agentmemory/export` returns oversized refusal under HTTP 200, materializes payload before refusing | export OOM risk |
| **#1333** | Pinned slot block silently dropped when exceeding `TOKEN_BUDGET` | context silently truncated |
| **#1331** | Windows: `~/.agentmemory/.env` never loaded (`HOME` unset); integrations fail silently | ⚠️ **Windows setup** — set `HOME=%USERPROFILE%` |
| **#1330** | Docker deployment: real-time viewer on `:3113` unreachable | ⚠️ **Docker** — viewer not exposed (loopback only by design; SSH-tunnel) |
| **#1328** | feat: allow custom HTTP headers on LLM provider requests | feature request |
| **#1326** | `/sessions` endpoint hangs indefinitely; `kv.list` never resolves — breaks viewer + MCP | ⚠️ **MCP** — hard hang, critical |
| **#1321** | Codex `prompt_submit` observation returned by same-turn recall (self-recall) | Codex — recall echoes the current turn |

### Practical takeaways for a first install

1. **Set an LLM provider key** (even a cheap/local one) to avoid the `#1341`
   keyless failure storm, or leave summarize features off.
2. **On Windows**, export `HOME` before running (`#1331`), or use WSL2.
3. **On Docker**, be aware of `#1335` (index loss on teardown) and `#1330`
   (viewer stays on loopback — tunnel to reach `:3113`).
4. If `/sessions` or the viewer hangs, it's likely `#1326` — restart the server.
5. Custom OpenAI-compatible endpoints: watch `#1338` — the fallback path may
   ignore your `OPENAI_BASE_URL`.

---

## 19. Should overpower use it?

- **For the overpower repo itself:** low value — it's 34 files you wrote, 90%
  Markdown, and Part I's hand-written memory already covers the project state.
- **Where it would help:** the 4 downstream build repos (`E:\tocgen`, `E:\snip`,
  `E:\op-viewer`, and future `/op-build` targets) — automatic session-to-session
  memory of decisions and dead-ends, without you maintaining `.md` files.
- **Cost/weight caveat:** on [[dev-machine]] run it keyless + local embeddings,
  or point compression at a hosted cheap model (DeepSeek Flash ~$0.07 for the
  README's example workload). Don't run `qwen3:8b` locally on 7.6 GB RAM.
- **Overlap with overpower's own design:** overpower already has durable
  `.overpower/progress.md` + `findings.md` per build. agentmemory is a
  *cross-build* layer on top of that, not a replacement.

---

## 20. Sources

- <https://github.com/rohitg00/agentmemory> — repo + README (transcribed 2026-09-10)
- <https://github.com/rohitg00/agentmemory/issues> — open issues
- <https://github.com/topics/agent-memory> — the broader landscape
- <https://github.com/NirDiamant/Agent_Memory_Techniques> — memory-pattern notebooks
- <https://www.cognee.ai/blog/guides/open-source-memory-frameworks-llm-agents> — framework comparison
