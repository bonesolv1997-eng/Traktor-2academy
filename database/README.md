# `database/` — Schemas, Registries, Indexes

**Layer 0 (contract).** The machine-readable definitions that bind the layers
together. When a document and a schema disagree, **the schema wins** — it is what the
validator actually enforces.

---

## Contents

| File | Purpose |
|---|---|
| `sources.schema.json` | Normative schema for `research/sources/src-####.json`. |

Planned for later phases, added when first needed rather than now:

- `knowledge-index.json` — generated index of all knowledge entries, their verification
  levels, version scopes and source ids.
- `source-registry.json` — generated registry of all captured sources.
- `version-registry.json` — generated from `knowledge/versions/`, the authoritative
  list of Traktor versions in scope.
- `link-graph.json` — which content items depend on which knowledge entries, so a
  change to a fact can flag everything derived from it.

## Why schemas live here and not in `docs/`

`docs/` explains intent to humans. `database/` constrains machines. Keeping them
separate means the explanation can evolve in prose without silently desynchronising
from what is actually checked — and it gives the eventual delivery layer
(`apps/`) a single stable contract to read against.

## Change control

A schema change is a **MAJOR** knowledge-base version bump per
[../docs/versioning-strategy.md](../docs/versioning-strategy.md) §6. It requires a
migration note, Lead Architect approval, and a corresponding update to
`tests/validate_structure.py` in the same commit — a schema nobody enforces is
documentation, not a contract.

## Current state

**Phase 0.** `sources.schema.json` is in place because the research protocol depends on
it. The generated indexes arrive with the data they index; empty indexes would only
pretend to be structure.
