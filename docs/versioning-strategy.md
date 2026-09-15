# Versioning Strategy

Two different versioning problems, deliberately separated:

- **§1–§5 — Traktor version taxonomy.** How we scope facts to the software and
  hardware they are true of.
- **§6–§8 — Knowledge-base versioning.** How this repository itself evolves.

Conflating them is how projects end up with a `v2` tag that means nothing about which
Traktor the content describes.

**Owner:** Versioning Librarian, ratified by Lead Architect · **Status:** Phase 0

---

> **Important.** This document defines the *scheme*. It contains **no authoritative
> Traktor version inventory.** The real list of Traktor products and versions, with
> release dates and behavior changes, is a **Phase 1 deliverable** and must be built
> exclusively from official Native Instruments sources per
> [research-protocol.md](research-protocol.md). Any version string appearing below is a
> formatting illustration, not a claim about Traktor.

## 1. Why versioning is the core problem

Traktor has shipped for well over a decade across multiple major versions, on multiple
operating systems, with a changing set of supported hardware. Almost every statement
about it is true of some versions and false of others.

An unscoped fact is therefore not a weaker fact — it is usually an *incorrect* one for
a meaningful fraction of readers. Version scoping is not metadata hygiene; it is the
difference between accurate and wrong.

## 2. Version identifier syntax

```
<product-line> <major>[.<minor>[.<patch>]]
```

Scoping in frontmatter uses either an exact list or a range:

```yaml
traktor_versions: ["3.11.1"]            # exact
traktor_versions: ["3.x"]               # whole major line
traktor_versions: ["3.5 - 3.11"]        # inclusive range
traktor_versions: ["unknown"]           # version-sensitive, range not established
```

Rules:

- **Version strings must come from the official registry** (`knowledge/versions/`),
  never from memory or inference. A version number that is not in the registry is not
  used.
- `x` wildcards and ranges are permitted only where evidence covers the whole span.
  Evidence for one point release does not license `3.x`.
- **`unknown` is a complete, valid value.** It is the correct entry whenever the source
  does not state applicability. Guessing a range to look more precise is an S2 finding
  under [qa-protocol.md](qa-protocol.md) §3.
- Operating system and hardware context are separate dimensions, recorded in the
  entry body or in dedicated fields — never folded into the Traktor version string.

## 3. The version registry

`knowledge/versions/` holds the registry: one entry per Traktor product/version with
evidence, plus change records.

Registry entry frontmatter follows the standard knowledge schema with
`domain: versions`. Body must contain:

```markdown
## Identification
Official product name, version string, release date — or UNKNOWN.

## Evidence
Source ids. Every line above traces to one.

## Documented changes
Changes NI documents for this version, each with its own source id.

## Knowledge impact
Knowledge entries whose scope intersects this version, and whether they have been
re-verified.
```

**A version is not added to the registry because someone mentioned it.** It is added
because an official source documents it.

## 4. Behavior change records

When a version changes documented behavior:

1. The **old** behavior entry keeps its scope and gains `status: superseded`, linked
   forward to the successor.
2. A **new** entry is created for the new behavior with its own scope, sources and
   `V` level.
3. A **change record** in `knowledge/versions/` links both and cites the release notes.
4. Every content item referencing either entry moves to `status: stale`.

Superseded entries are **never deleted**. They remain the answer for readers on legacy
versions, who are a real and permanent audience — DJs do not upgrade mid-gig.

## 5. Cross-version claims

Statements like "in earlier versions X, now Y" are **two claims**, each needing its
own scope and source. They are written as two entries plus a change record. A single
unsourced sentence spanning versions is an S2 finding.

Where the *change itself* is not officially documented but is consistently reported,
it is recorded at `V2` with a community marker and a clear note that the transition
point between versions is not established.

## 6. Knowledge-base versioning

This repository uses **semantic versioning for the knowledge base as a whole**, not
per-file:

- **MAJOR** — a structural break: schema change, id scheme change, layer redesign.
  Requires a migration note and invalidates prior consumers.
- **MINOR** — new knowledge domains, new content types, backward-compatible schema
  additions.
- **PATCH** — content corrections, re-verifications, new entries. The normal case.

Phase 0 lands at `0.1.0`. The `1.0.0` tag is reserved for the first release in which
the core knowledge domains are populated at `V3`/`V4` and pass a full QA cycle — not
for the first time the website goes live. Shipping `1.0.0` on a site launch would
claim authority the content had not earned.

## 7. Per-entry versioning

Entries do not carry their own version numbers. They carry:

- `status` — draft, verified, disputed, superseded, unknown;
- `verification_level` — V0–V4 / VX;
- `traktor_versions` — the scope the fact is true of;
- `last_verified` — when it was last checked.

History lives in git, which records every revision with author and date far better than
a hand-maintained version field would. Duplicating that in frontmatter would create a
second, drifting account of the same thing.

## 8. Tags, branches and releases

- All work lands on a working branch, reviewed, then merged. Never pushed directly to
  `main`.
- Release tags follow §6.
- A release snapshot is a tag, not a copy. Content is reproducible from the knowledge
  layer at any tag.
- The eventual delivery layer (`apps/`) reads from a tagged snapshot, so the published
  site is always a known state of the knowledge base rather than whatever `main`
  happened to hold at deploy time.

## 9. Open questions for Phase 1

Recorded rather than resolved, per the conflict-and-unknown principles:

1. **Which Traktor versions does the project scope?** Supporting every historical
   release is impractical; the cutoff needs an explicit, documented decision.
2. **How are non-Traktor-branded variants handled** (bundled, mobile, LE-style
   editions)? Whether these are in scope is **UNKNOWN** and requires official
   documentation to resolve.
3. **How is hardware compatibility scoped when a controller works with some Traktor
   versions and not others?** The registry needs a compatibility-scoping decision
   before Phase 2, or `knowledge/hardware/` will fill with unscoped claims.
4. **What is the re-verification cadence for discontinued hardware?** Currently
   inherited from the level-based windows in [qa-protocol.md](qa-protocol.md) §6,
   which may be wasteful for hardware that can no longer change.
