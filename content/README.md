# `content/` — The Presentation Layer

**Layer 3.** Human-facing material assembled from verified knowledge. Read
[../docs/content-protocol.md](../docs/content-protocol.md) before writing.

---

## The rule that matters

**Content narrates. It never asserts.**

Every factual statement here must resolve to a `knowledge/` entry at `V3`/`V4` — or
`V2` carrying a community-report marker. If the fact you need is not in `knowledge/`,
file a research request. Do not write it from recall.

## Directories

| Directory | Shape | Use for |
|---|---|---|
| `guides/` | Task-oriented, single goal | "How do I set up DVS?" |
| `tutorials/` | Sequenced, learning goal | "Learn mapping from scratch" |
| `courses/` | Ordered multi-lesson curricula | Structured programmes |
| `faq/` | One question, one answer | High-frequency questions |
| `reference/` | Lookup, scannable tables | Parameters, mappings, compatibility |

## Frontmatter

```yaml
---
title: <reader-facing title>
type: guide                    # guide | tutorial | course | faq | reference
status: draft                  # draft | reviewed | published | stale
knowledge_refs: ["kb-dvs-0001"]
traktor_versions: ["unknown"]
last_reviewed: 2026-09-15
audience: all
---
```

`knowledge_refs` is mandatory and non-empty. `traktor_versions` is the union of the
referenced entries' scopes and **may never be broader than them** — content does not
get to claim wider applicability than its evidence.

## Markers reach the reader

Version banners, community-report markers and explicit unknowns are carried through
into the prose. A reader who is told "this is undocumented" can act sensibly; a reader
given a confident guess wastes an afternoon.

## Current state

**Phase 0 — empty by design**, and stays empty through Phase 3.

Placeholder guides written ahead of the evidence would be indistinguishable, to a
reader, from verified ones. That is the exact harm this project exists to prevent, so
the delay is the point rather than a cost.
