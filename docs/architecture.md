# Architecture

How Traktor Academy is structured, why it is structured this way, and what each layer
is allowed to do.

**Owner:** Lead Architect · **Status:** Phase 0 · **Last revised:** 2026-09-15

---

## 1. Design goals

1. **A fact is stored exactly once.** Duplication guarantees eventual divergence.
2. **A fact is never published without evidence attached to it.**
3. **A fact is never stated without a version scope** where version matters.
4. **Content is disposable; knowledge is not.** Any guide can be regenerated from the
   knowledge layer. The reverse is not true.
5. **The system degrades honestly.** When evidence is missing, the output says
   "unknown" instead of degrading into plausible invention.

## 2. Layers

```
┌────────────────────────────────────────────────────────────────────┐
│  L4  DELIVERY      apps/                                           │
│      Renders. Introduces no facts.                                 │
├────────────────────────────────────────────────────────────────────┤
│  L3  PRESENTATION  content/                                        │
│      Narrates. Assembles knowledge into human-facing material.     │
├────────────────────────────────────────────────────────────────────┤
│  L2  TRUTH         knowledge/                                      │
│      Asserts. Atomic, version-scoped, cited facts. The only        │
│      place in the system permitted to state what is true.          │
├────────────────────────────────────────────────────────────────────┤
│  L1  EVIDENCE      research/                                       │
│      Captures. Immutable provenance, tiered sources, conflicts.    │
├────────────────────────────────────────────────────────────────────┤
│  L0  CONTRACT      AGENTS.md · TRAKTOR-ACADEMY-AGENT-SYSTEM.md     │
│                    docs/ · database/ · tests/                      │
│      Constrains. Defines what the layers above may do.             │
└────────────────────────────────────────────────────────────────────┘
```

**Dependency rule:** each layer may read the layer directly below it and write only
to its own layer. No layer may write downward. L2 may never write to L1; L3 may never
write to L2.

The practical consequence: a Content Writer who notices a fact is wrong does not fix
it — they file a correction that a Knowledge Engineer action against evidence.

## 3. Directory contract

```
Traktor-2academy/
├── AGENTS.md                        # L0 binding rules for agents
├── TRAKTOR-ACADEMY-AGENT-SYSTEM.md  # L0 roles, pipeline, gates
├── README.md                        # orientation + phase status
├── research/                        # L1
│   ├── raw/          immutable captures, one dir per capture
│   ├── sources/      structured source records (src-####.json)
│   ├── reports/      analysis across multiple sources (RPT-####)
│   └── conflicts/    recorded contradictions (CF-####)
├── knowledge/                       # L2 — the truth layer
│   ├── software/     Traktor application features, settings, behavior
│   ├── hardware/     Controllers, interfaces, Traktor-hardware compatibility
│   ├── audio/        Audio setup, routing, latency, drivers, cueing
│   ├── midi/         MIDI mapping, MIDI messages, mapping files
│   ├── hid/          HID protocol, HID mappings, HID vs MIDI
│   ├── dvs/          Timecode, DVS setup, calibration, control records
│   ├── troubleshooting/  Diagnosed problems and resolutions
│   ├── workflows/    Verified working practices and setups
│   ├── glossary/     Term definitions
│   └── versions/     Version behavior and change records
├── content/                         # L3
│   ├── guides/       task-oriented, "how do I…"
│   ├── tutorials/    sequenced, learning-oriented
│   ├── courses/      multi-lesson curricula
│   ├── faq/          question-shaped answers
│   └── reference/    lookup material: tables, mappings, parameters
├── database/                        # L0 schemas, registries, indexes
├── apps/                            # L4 — EMPTY until Phase 4
├── tests/                           # L0 validation
└── docs/                            # L0 protocols
```

### Boundary cases, decided in advance

These are the questions that otherwise get answered inconsistently at 2am:

- **A controller's MIDI mapping** → `knowledge/midi/`. **Whether that controller works
  with Traktor at all** → `knowledge/hardware/`.
- **A setting that affects sound** → `knowledge/audio/` if the subject is the audio
  behavior; `knowledge/software/` if the subject is the setting itself.
- **A DVS calibration problem** → `knowledge/dvs/` for the behavior;
  `knowledge/troubleshooting/` for the diagnosed fault and fix, cross-referenced.
- **A term used in DVS docs** → defined once in `knowledge/glossary/`, linked from
  everywhere else. Never redefined.
- **"Traktor Pro 4 changed X"** → the new behavior lives in the relevant domain entry
  with a version scope; the *change itself* is recorded in `knowledge/versions/`.

When an entry legitimately spans domains, file it under its **primary subject** and
cross-reference. Never duplicate the fact.

## 4. Identity scheme

| Entity | Pattern | Example |
|---|---|---|
| Knowledge entry | `kb-<domain>-####` | `kb-dvs-0014` |
| Source record | `src-####` | `src-0042` |
| Analysis report | `RPT-####` | `RPT-0007` |
| Conflict record | `CF-####` | `CF-0003` |
| Content item | slug, no numeric id | `dvs-calibration-guide` |

Ids are sequential per namespace, never reused, never renumbered. A deleted entry
retires its id permanently — reuse would silently rewrite every citation pointing at
it.

## 5. Frontmatter contract

Knowledge entries (`knowledge/**/*.md`) must carry:

```yaml
---
id: kb-software-0001
title: <short factual title>
domain: software
status: verified            # draft | verified | disputed | superseded | unknown
verification_level: V4      # V0 | V1 | V2 | V3 | V4 | VX
version_sensitive: true
traktor_versions: ["unknown"]
sources: ["src-0001"]
last_verified: 2026-09-15
---
```

Content items (`content/**/*.md`) must carry:

```yaml
---
title: <reader-facing title>
type: guide                 # guide | tutorial | course | faq | reference
status: draft               # draft | reviewed | published | stale
knowledge_refs: ["kb-software-0001"]
traktor_versions: ["unknown"]
last_reviewed: 2026-09-15
---
```

Validation of both is enforced by `tests/validate_structure.py`. The schemas are
normative — the validator is the tie-breaker, not this document.

## 6. The unknown convention

`unknown` is a **value**, not an absence. Three equivalent spellings exist for
different contexts and all three are validated:

- In frontmatter: `traktor_versions: ["unknown"]`
- In a body field: `UNKNOWN`
- In prose: an explicit sentence stating the information is not documented and no
  verified source was found.

What is **not** permitted: an empty field, an omitted field, or a confident sentence
where the evidence should be. Silence is indistinguishable from certainty, and that is
the failure this project is built to eliminate.

## 7. Technology decisions

**Deliberately undecided.** The delivery stack is a Phase 4 decision and choosing it
now would constrain the knowledge model for no benefit. What *is* fixed at Phase 0:

- Knowledge and content are **plain Markdown with YAML frontmatter** — portable,
  diffable, greppable, and independent of any framework.
- Structured data (source records, indexes) is **JSON** with published schemas.
- Validation is **dependency-free Python 3**, so it runs anywhere with no install step.
- Nothing in L1–L3 may depend on a rendering framework.

## 8. Decisions log

| # | Date | Decision | Rationale |
|---|---|---|---|
| D-001 | 2026-09-15 | Four-layer architecture with write-downward prohibited | Prevents unverified claims reaching readers |
| D-002 | 2026-09-15 | Markdown + YAML frontmatter for L1–L3 | Portability; no framework lock-in before Phase 4 |
| D-003 | 2026-09-15 | `unknown` is a first-class value, validated | Honesty must be machine-checkable, not aspirational |
| D-004 | 2026-09-15 | Ids never reused | Citation integrity across the life of the project |
| D-005 | 2026-09-15 | `apps/` remains empty through Phase 3 | Prevents delivery concerns distorting the knowledge model |
| D-006 | 2026-09-15 | Conflicts are artifacts, not errors | Preserves evidence that a silent resolution would destroy |

## 9. Phase status

Phase 0 complete. Phase 1 (source corpus) is the next opening and is described in the
[research protocol](research-protocol.md). No phase may be self-opened by an agent.
