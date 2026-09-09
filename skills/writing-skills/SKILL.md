---
name: writing-skills
description: Use when creating a new overpower skill or editing an existing one. Keeps skills consistent, valid, and testable.
---

# Writing skills

A skill is a short instruction file the agent reads when its `description`
matches the situation. It is prompt text — treat it like code that runs in a
model.

## The file

```
skills/<kebab-name>/SKILL.md          # required
skills/<kebab-name>/<supporting>.md   # optional deep-dives, referenced from SKILL.md
```

### Frontmatter — exactly two keys, valid YAML

```yaml
---
name: <kebab-name>            # MUST equal the directory name
description: <when to use it> # a trigger, not a summary: "Use when …", "Use before …"
---
```

- **Only `name` and `description`.** No `triggers:`, no `tags:`, no lists. A
  stray non-`key: value` line makes the whole block invalid YAML and the skill
  silently fails to register (this is a real, filed bug in the project we
  learned from). The `test_skills_lint.py` test enforces this.
- The `description` is the only thing the router sees when deciding to load the
  skill. Make it specific about the *situation*, not the *topic*.

### Body

- Opens with a `#` heading.
- States the rule in the first two lines. The agent may only read that far.
- Uses tables and short sections. No wall of prose.
- Concrete examples over abstract advice. Show a good and a bad case.
- If it references another skill, name it in backticks (`` `reviewing-changes` ``)
  — the lint test checks every referenced skill exists or is listed as planned
  in `CHANGELOG.md`.

## Prose vs. a script

Put a step in **prose** when it needs judgement (classify this, decide whether…).

Extract it to a **script** (`hooks/` or a skill-local `.py`) when it is
deterministic and the agent would otherwise re-derive it every time or get it
subtly wrong — JSON building, path resolution, parsing. The session-start hook
is a script for exactly this reason: hand-rolled JSON escaping in prose is a bug
factory.

## Links inside the repo

Relative links break when you move a file and don't notice. Prefer:
- referencing skills by name in backticks (checked by the lint test), not by path
- for a genuine file link, use a repo-root-relative path (`docs/design.md`) and
  add a line to the PR checklist to grep for the old path after a move

## Before you commit a skill

1. `python -m unittest discover -s tests` — green (frontmatter + references).
2. Read the `description` cold: would you know from that line alone when this
   skill should fire? If not, rewrite it.
3. Read the first two lines of the body: is the rule stated? The agent might
   not read further.
4. Add or update a test if the skill makes a checkable claim (a required
   phrase, a referenced skill, a file it writes).
5. Update `CHANGELOG.md`.
