# `apps/` — The Delivery Layer

**Layer 4. Intentionally empty.**

This directory will hold the public website and any internal tooling. It is empty in
Phase 0 and **must remain empty through Phase 3.**

---

## Why the delay is deliberate

A delivery layer built before the knowledge model is settled will shape that model to
suit rendering concerns — fields added because a template wants them, structures
flattened because a query is easier that way. Those distortions are expensive to
reverse and they quietly degrade the thing the project is actually for.

`tests/validate_structure.py` enforces this: the presence of application code in
`apps/` before Phase 4 is a validation failure, not a style preference.

## The contract, fixed now

When Phase 4 opens, `apps/` will:

- **read** from `knowledge/`, `content/` and `database/`;
- **never write** to any of them;
- consume a **tagged release snapshot**, so the live site is always a known state of
  the knowledge base rather than whatever `main` held at deploy time;
- render version banners, community-report markers and explicit unknowns **exactly as
  the content layer supplies them** — never softened, never omitted for design reasons.

If a rendering requirement needs a new data field, it is requested from the Lead
Architect. It is not added to the content layer as a workaround.

## Stack

**Undecided on purpose.** See [../docs/architecture.md](../docs/architecture.md) §7.
The knowledge layers are plain Markdown with YAML frontmatter and JSON schemas
precisely so this decision can be made late, with information, and reversed cheaply.

## Current state

Empty. Opening Phase 4 is a Lead Architect decision recorded in
`../docs/architecture.md` §8. An agent must not self-promote into it.
