---
name: architecture
description: Use for T2/T3 changes after research, before planning — writes .overpower/architecture.md with a component diagram, interfaces, data flow, UI wireframe if any, and risks. Keeps the plan honest about shape before tasks are cut.
---

# architecture

Design the **shape** of the change so tasks can be cut cleanly and run in parallel.

## Write `.overpower/architecture.md`

1. **Component map** — the **first** ```mermaid block in the file (op-viewer renders
   only the first). Show existing parts touched and new parts, with classDefs:
   ```mermaid
   flowchart LR
     A["routes/reports.ts<br/>(changed)"]:::changed --> B["export.ts<br/>(new)"]:::new
     classDef new fill:#d1fae5,stroke:#059669;
     classDef changed fill:#fef3c7,stroke:#d97706;
   ```
2. **Interfaces** — exact signatures, routes, schema changes, events. These are
   the contracts tasks build against; parallel tasks may only meet at these.
3. **Data flow** — one short paragraph or sequence diagram for the main path,
   plus what happens on failure.
4. **UI (if any)** — text wireframe + a table: element id | content | look |
   states (empty, loading, error).
5. **Risks** — each risk with the task that de-risks it (do risky things first).
6. **Alternatives rejected** — one line each, why not.

## Design rules

- Follow the patterns `research` found. A new pattern needs a stated reason.
- YAGNI: no hooks, options or abstractions the spec doesn't need.
- Draw boundaries so tasks touch disjoint files — that's what makes parallel
  subagents safe.
- Keep it short. If it's longer than the code it describes, cut it.
