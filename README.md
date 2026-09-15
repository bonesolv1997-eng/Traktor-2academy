# TRAKTOR ACADEMY

A comprehensive, authoritative and continuously maintained knowledge platform for
Native Instruments **Traktor**, **Traktor Pro**, and compatible Traktor hardware.

> **Current phase: Phase 0 — Infrastructure.**
> The engineering and knowledge infrastructure is in place. The public website has
> **not** been started and must not be started until the research and knowledge
> layers contain verified content.

---

## What this project is

Traktor Academy is not a website with articles attached to it. It is a **living
knowledge system**: a versioned, evidence-backed database of facts about Traktor,
from which guides, tutorials, courses and reference material are *derived*.

The distinction matters:

- Content is an **output**, not the source of truth.
- Facts are stored **once**, atomically, each with its own evidence and version scope.
- When Traktor changes, we update the fact, and the affected content is flagged
  automatically — we do not go hunting through prose.
- Every claim is traceable to a named source captured at a known date, or it is
  explicitly marked unknown.

## Core principles

These are non-negotiable and are enforced by automated checks where possible.

1. **Accuracy over speed.** An unfinished page beats a wrong page.
2. **Evidence over assumptions.** No claim without a source.
3. **Official Native Instruments documentation has the highest authority.**
4. **Never invent** Traktor features, settings, menus, compatibility or behavior.
5. **Version-sensitive information must always identify the relevant version.**
6. **Community reports are clearly distinguished from official documentation.**
7. **Unknown information remains explicitly marked as unknown.** We never fill a gap
   with a plausible guess.
8. **Conflicting evidence is recorded, never silently resolved.**
9. **This is a living knowledge system, not a static website.**

## Repository map

| Path | Purpose |
|---|---|
| `AGENTS.md` | Binding operating contract for any AI agent working in this repo. Read first. |
| `TRAKTOR-ACADEMY-AGENT-SYSTEM.md` | The multi-agent system: roles, pipelines, handoffs, gates. |
| `research/` | Evidence layer. Raw captures, structured source records, analysis, contradictions. |
| `knowledge/` | Truth layer. Atomic, verified, version-scoped facts. The only source of truth. |
| `content/` | Presentation layer. Human-facing material *derived from* `knowledge/`. |
| `database/` | Schemas, registries and indexes that bind the layers together. |
| `apps/` | Application code (site, tooling). **Empty by design in Phase 0.** |
| `tests/` | Validation. Structure, frontmatter, citation and link integrity. |
| `docs/` | The protocols that define how this system operates. |

### Protocol documents

| Document | Governs |
|---|---|
| [docs/architecture.md](docs/architecture.md) | System layers, data flow, identity scheme, frontmatter contract |
| [docs/research-protocol.md](docs/research-protocol.md) | How evidence is captured, tiered and stored |
| [docs/fact-checking-protocol.md](docs/fact-checking-protocol.md) | How claims are verified, scoped and conflicted |
| [docs/content-protocol.md](docs/content-protocol.md) | How knowledge becomes publishable content |
| [docs/qa-protocol.md](docs/qa-protocol.md) | Gates, severity levels and release criteria |
| [docs/versioning-strategy.md](docs/versioning-strategy.md) | Traktor version taxonomy and knowledge-base versioning |

## Data flow

```
   research/          knowledge/          content/           apps/
  (evidence)   ->     (facts)      ->    (narrative)   ->   (delivery)

  raw captures       atomic claims       guides, FAQs       public site
  source records     verification lvl    tutorials          (Phase 3+)
  analysis reports   version scope       courses
  conflict records   citations           reference
```

Information only ever flows left to right. Content may never introduce a fact that
does not already exist in `knowledge/`. This is the single most important structural
rule in the project.

## Validation

```bash
./tests/run_checks.sh
```

This runs `tests/validate_structure.py`, which enforces:

- the directory contract and required documents are present;
- every internal Markdown link in the repo resolves to a real file;
- knowledge entries carry valid frontmatter (id, status, verification level,
  version scope, sources, last-verified date);
- version-sensitive entries declare an explicit version scope;
- high-verification claims cite sources of sufficient authority tier;
- no banned placeholder or fabrication patterns exist.

The check exits non-zero on any violation. Nothing merges with a failing check.

## Phase status

| Phase | Scope | Status |
|---|---|---|
| 0 | Engineering & knowledge infrastructure | **Complete** |
| 1 | Official documentation corpus & source registry | Not started |
| 2 | Knowledge base construction (facts, versions, glossary) | Not started |
| 3 | Content production (guides, tutorials, reference) | Not started |
| 4 | Delivery layer (public website) | Not started |
| 5 | Maintenance loop (change detection, re-verification) | Continuous |

## Licensing and attribution

All third-party evidence remains the property of its originator and is recorded with
full attribution in `research/sources/`. Captured material in `research/raw/` is
retained for provenance and internal verification only. Original content produced by
this project is licensed separately — see `docs/content-protocol.md`.
