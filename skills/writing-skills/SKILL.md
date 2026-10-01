---
name: writing-skills
description: Use when creating or editing a Claude skill (for overpower or any project) — write the description so it triggers at the right moment, keep the body procedural and short, and test it against real prompts with and without the skill.
---

# writing-skills

A skill is instructions that load **when they're relevant**. Its two jobs:
trigger at the right moment (description) and change behaviour for the better (body).

## Layout

```
skills/<name>/SKILL.md        # required
skills/<name>/<reference>.md  # optional — loaded only when SKILL.md points to it
skills/<name>/scripts/...     # optional — deterministic helpers
```
Frontmatter: `name` (kebab-case, matches folder) and `description`.

## The description decides everything

- Start with **when**: "Use when …" plus concrete triggers (phrases users say,
  situations, file types).
- Then **what it does** in one clause.
- Specific beats clever: "Use for any bug, failing test, crash, or flaky
  behaviour" triggers; "Debugging wisdom" doesn't.
- Not so broad it fires on everything. Overlapping skills → sharpen both.

## The body

- **Procedure, not essay.** Numbered steps, tables, checklists, exact formats.
- Say **why** for any rule that seems arbitrary — the model generalises from reasons.
- Include the failure modes you've seen ("red flags") — they're the highest-value lines.
- Point to other skills by name instead of repeating them.
- Keep it under ~150 lines; push detail into reference files.
- Write for proportion: say when **not** to apply the skill.

## Test it

1. Write 3–5 realistic prompts that should trigger it, and 2 that shouldn't.
2. Run them in fresh sessions; check it triggered (or didn't) and the behaviour changed.
3. Compare against no skill: is the output actually better? If not, cut or rewrite.
4. If your harness has a plugin eval runner (Claude Code: `claude plugin eval
   <plugin-dir>`), use it to compare against a no-plugin baseline.
5. Fix the description first when triggering is wrong; fix the body when behaviour is.
