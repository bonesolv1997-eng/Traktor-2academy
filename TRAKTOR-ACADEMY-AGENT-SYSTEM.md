# TRAKTOR ACADEMY AGENT SYSTEM

The multi-agent operating model for Traktor Academy. It defines **who does what, in
what order, with what authority, and what stops a bad fact from reaching a reader.**

This document describes the system. [AGENTS.md](AGENTS.md) describes the rules every
agent in it must obey.

---

## 1. Why a system and not a single agent

A single agent asked to "write a Traktor guide" will produce fluent prose built on
recall, and recall about Traktor is unreliable across versions. Splitting the work
creates the friction that produces accuracy:

- The agent that **gathers** evidence cannot publish it.
- The agent that **verifies** evidence did not gather it, so it has no attachment to
  the conclusion.
- The agent that **writes** content cannot introduce facts — it may only assemble
  entries that already passed verification.
- The agent that **audits** can fail any of the above.

No single role has the authority to move an unverified statement into `content/`.
That separation is the entire point.

## 2. Roles

### 2.1 Lead Architect / Technical PM
Owns structure, protocols and sequencing. Approves changes to `docs/`, `AGENTS.md`,
`database/` schemas and this file. Decides phase gates. Does not write facts or content.
**Authority:** highest, but only over process — never over evidence.

### 2.2 Researcher
Retrieves and captures sources. Writes to `research/raw/`, `research/sources/`,
`research/reports/`. Assigns evidence tiers. **May not** write to `knowledge/` or
`content/`. Must record retrieval date, exact URL, and version context for every
capture. Explicitly reports when a search found nothing — an empty result is data.

### 2.3 Fact-Checker
Reads sources and knowledge entries. Assigns verification levels `V0`–`V4`/`VX`.
Creates `research/conflicts/` records. May **downgrade** any entry. **May not** raise
an entry above the tier its sources support. May not write prose content.

### 2.4 Knowledge Engineer
Authors and maintains entries in `knowledge/`. Owns atomicity, id stability,
version scoping and cross-references. May only cite sources the Researcher captured.
When the needed source is missing, files a research request rather than writing the
entry from recall.

### 2.5 Content Writer
Produces `content/`. Assembles verified knowledge into guides, tutorials, courses,
FAQ and reference. **May not introduce any fact not present in `knowledge/`.** Must
carry version banners and community-report markers through into the prose. Where
knowledge is `V2` or unknown, must say so in the reader's language.

### 2.6 QA Auditor
Runs `tests/run_checks.sh`, audits a sample of entries against their sources, and
owns the gate definitions in [docs/qa-protocol.md](docs/qa-protocol.md).
**Can block a release.** Reports severity per the QA protocol.

### 2.7 Versioning Librarian
Maintains `knowledge/versions/` and the version taxonomy in
[docs/versioning-strategy.md](docs/versioning-strategy.md). Detects when a Traktor
release changes documented behavior and opens re-verification tasks for every entry
scoped to the affected versions. The project's defense against silent staleness.

### 2.8 Community Intelligence Analyst
Monitors T3/T4 signals: forums, user reports, mapping files. **Converts noise into
research requests, never into facts.** Every finding is labeled community-sourced and
enters at `V1` or below.

### 2.9 Site Engineer
Phase 4 only. Builds `apps/`. Consumes `knowledge/` and `content/` as inputs.
**Cannot edit either.** If a rendering requirement needs a new data field, it is
requested from the Lead Architect, not hacked into the content layer.

## 3. Pipeline

```
        ┌─────────────────────────────────────────────────────────┐
        │                      PIPELINE                           │
        └─────────────────────────────────────────────────────────┘

 [signal]                [capture]              [verify]
 question, release,  ->  Researcher         ->  Fact-Checker
 community report,       research/raw           assigns V-level
 gap detected            research/sources       creates conflicts
                         (tiers assigned)
                                                       │
                            ┌──────────────────────────┤
                            │                          │
                       V3 / V4                    V0–V2 or VX
                            │                          │
                            v                          v
                     [knowledge]                  [hold]
                     Knowledge Engineer       stays in research/,
                     atomic entry,            visible internally,
                     version scope,           NOT publishable
                     source ids
                            │
                            v
                       [content]
                       Content Writer
                       narrative + version banners
                       + provenance markers
                            │
                            v
                          [audit]
                          QA Auditor
                          automated + sampled manual
                            │
                     ┌──────┴──────┐
                  pass            fail
                     │              │
                     v              v
                 [publish]      [rework, with
                                 severity + owner]
```

Nothing skips a stage. The most common failure this prevents: a Researcher finding
something interesting and writing it straight into a guide.

## 4. Gates

| Gate | Between | Criterion | Owner |
|---|---|---|---|
| **G1 Capture** | research/raw → research/sources | Provenance complete: URL, date, tier, version context | Researcher |
| **G2 Verification** | sources → knowledge | V-level assigned, contradictions filed | Fact-Checker |
| **G3 Knowledge** | knowledge → content | Atomic, version-scoped, source ids resolve, `tests` pass | Knowledge Engineer |
| **G4 Content** | content → review | Every claim maps to a knowledge entry; markers preserved | Content Writer |
| **G5 Audit** | review → publish | Automated checks pass + sampled manual audit | QA Auditor |

G5 is the only gate with release authority. Gates G1–G4 are self-certified and
sampled retrospectively by G5.

## 5. Conflict handling

A conflict is a **first-class artifact**, not an error to be cleaned up.

1. Either agent detects disagreement → creates `research/conflicts/CF-####.md`.
2. Both positions are recorded with full citations. Neither is deleted.
3. The affected knowledge entry is set to `verification_level: VX`,
   `status: disputed`, and linked to the conflict record.
4. Resolution requires one of:
   - a **T0/T1 source** that settles it (preferred), or
   - reproduction on the specific hardware/software version (documented in
     `research/reports/`), or
   - an explicit human decision, recorded with name and date.
5. On resolution the conflict record is closed with the outcome, and the superseded
   position is retained in the record for history.

**Two T0 sources in conflict is an automatic escalation to a human.** It usually means
the behavior is version-dependent and both are correct within their own scope.

## 6. Staleness and re-verification

Every entry carries `last_verified`. Re-verification is triggered by:

- a new Traktor release touching the entry's version scope;
- a broken or changed source URL;
- an age threshold — see [docs/qa-protocol.md](docs/qa-protocol.md) for the current
  values;
- a user report contradicting the entry.

An entry past its threshold does not get deleted. It gets a re-verification task and,
if unresolved, a visible staleness marker in any content derived from it.

## 7. Artifacts and naming

| Artifact | Location | Naming |
|---|---|---|
| Raw capture | `research/raw/` | `YYYY-MM-DD-<slug>/` containing the capture + `manifest.yml` |
| Source record | `research/sources/` | `src-####.json` (schema: `database/sources.schema.json`) |
| Analysis report | `research/reports/` | `RPT-####-<slug>.md` |
| Conflict record | `research/conflicts/` | `CF-####-<slug>.md` |
| Knowledge entry | `knowledge/<domain>/` | `<id>.md`, id = `kb-<domain>-####` |
| Content item | `content/<type>/` | `<slug>.md` with frontmatter linking knowledge ids |

Ids are **never reused**, including for deleted entries. Reuse silently rewrites
history and breaks every citation pointing at it.

## 8. Phase authority

| Phase | Open? | What may be built |
|---|---|---|
| 0 — Infrastructure | **Open** | Directories, protocols, schemas, validation |
| 1 — Source corpus | Not opened | Research captures, source registry, version inventory |
| 2 — Knowledge base | Not opened | `knowledge/` entries, glossary, version scoping |
| 3 — Content | Not opened | `content/` items derived from verified knowledge |
| 4 — Delivery | Not opened | `apps/`, the public website |
| 5 — Maintenance | Continuous | Re-verification, change detection, decay handling |

Opening a phase is a Lead Architect decision, recorded in `docs/architecture.md`
under Decisions. **An agent must not self-promote into a later phase.**

## 9. What "done" means for this project

There is no completion state. Traktor ships updates, hardware is discontinued, and
community practice shifts. Success is measured by:

- the proportion of published claims at `V3`/`V4`;
- time from a Traktor release to re-verification of affected entries;
- the number of open conflicts (a healthy number is non-zero and shrinking);
- the count of entries explicitly marked `unknown` — **this should be high**, because
  it measures honesty, not failure.
