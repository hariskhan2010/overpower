# Agent Memory Report — overpower

**Snapshot:** 2026-09-10
**Source:** Claude Code file-based auto-memory for this project
**Store location (outside the repo):** `~/.claude/projects/E--colibri-patner/memory/`

This file is a committed, human-readable dump of the agent's persistent memory so
it is visible on GitHub. The live store is a directory of Markdown files that
Claude Code loads at the start of every session; this report reproduces every
memory verbatim plus context on how the system works.

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

## 8. How to regenerate this report

The memory store is at `~/.claude/projects/E--colibri-patner/memory/`. To refresh
this file, copy `MEMORY.md` and each `<slug>.md` body in verbatim and update the
snapshot date. There is no automated exporter — the store is meant to be read by
the agent, not published, so this report is a manual courtesy copy.
