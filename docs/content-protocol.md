# Content Protocol

How verified knowledge becomes material a person can actually use — and the
constraints that keep content from becoming a second, less accurate source of truth.

**Owner:** Content Writer role · **Status:** Phase 0

---

## 1. Principle

Content **narrates**. It never **asserts**.

Every factual statement in `content/` must resolve to a knowledge entry that already
exists at `V3` or `V4` (or `V2` with a marker). If the fact you need is not in
`knowledge/`, you file a research request — you do not write it.

This is the rule that makes the whole system work. The moment a writer adds a fact
from recall, the knowledge layer stops being the source of truth, staleness detection
breaks, and the project is just a website with opinions.

## 2. Content types

| Directory | Shape | Use for |
|---|---|---|
| `content/guides/` | Task-oriented, one goal | "How do I set up DVS?" |
| `content/tutorials/` | Sequenced steps, learning goal | "Learn mapping from scratch" |
| `content/courses/` | Multi-lesson curriculum, ordered | Structured programmes; each lesson is its own item with a `course` and `order` |
| `content/faq/` | One question, one answer | High-frequency specific questions |
| `content/reference/` | Lookup, scannable | Parameter tables, mapping lists, compatibility matrices |

**Do not blur them.** A guide that drifts into a tutorial confuses the reader about
whether they are being told how to do a thing or taught a subject.

## 3. Frontmatter

```yaml
---
title: <reader-facing title>
type: guide                      # guide | tutorial | course | faq | reference
status: draft                    # draft | reviewed | published | stale
knowledge_refs: ["kb-dvs-0001", "kb-audio-0004"]
traktor_versions: ["unknown"]
last_reviewed: 2026-09-15
audience: beginner | intermediate | advanced | all
---
```

- `knowledge_refs` is **mandatory and non-empty**. An item with no knowledge
  references has no factual basis and cannot be reviewed.
- `traktor_versions` must be the **union of the scopes of the entries it uses**, and
  must never be broader than them. Content may not claim wider applicability than its
  evidence.
- `status: stale` is applied automatically by the maintenance loop when any referenced
  entry changes or exceeds its re-verification window. A stale item stays visible but
  carries a staleness marker.

## 4. Carrying provenance into prose

Markers do not stop at the knowledge layer. They reach the reader.

**Version banners.** Where the material is version-scoped, say so near the top, in
plain language:

> Applies to: Traktor Pro 4.x. Behavior differs in earlier versions.

Where the scope is genuinely unknown:

> Version applicability is not documented. The steps below were verified against the
> version noted on each source; check your own version before relying on them.

**Community-report markers.** For material resting on `V2`:

> Not confirmed in official NI documentation. This reflects consistent user reports
> and may not hold for your version or hardware.

**Unknowns.** Say it directly. Do not paper over it, do not omit the section, and do
not substitute a plausible answer:

> NI does not document this setting. No verified source was found.

A reader who is told "this is undocumented" can act sensibly. A reader given a
confident guess wastes an afternoon.

## 5. Writing standards

- **Second person, imperative, concrete.** "Open the Audio Setup panel" — not "One may
  access the audio configuration."
- **Name UI elements exactly as the official documentation names them**, at the version
  in scope. Never paraphrase a menu path from memory; copy it from the source.
- **One instruction per step.** Steps that bundle three actions cannot be followed or
  debugged.
- **State prerequisites and outcomes.** Every guide opens with what the reader needs
  and closes with what should now be true.
- **No invented troubleshooting.** If a step can fail, the failure mode and remedy must
  come from `knowledge/troubleshooting/` — which means from evidence.
- **No marketing register.** "Powerful", "intuitive", "seamless" convey nothing and
  erode the authority of everything around them.
- **Attribution for opinion.** Where judgment is offered, mark it as the project's
  assessment, not a fact about Traktor.

## 6. Structure requirements

Every guide and tutorial contains:

1. **Applies to** — version scope, from §4.
2. **What you need** — hardware, software versions, prior setup.
3. **Outcome** — what will be true when finished.
4. **Steps** — numbered, one action each.
5. **If something goes wrong** — only sourced failure modes.
6. **Sources** — the knowledge ids and, through them, the underlying sources.

FAQ items contain: the question as a heading, a direct answer in the first sentence,
then detail, then scope and sources.

Reference items are tables wherever tables work, with a version column **whenever the
table is version-sensitive**. A compatibility matrix without a version column is not a
reference; it is a rumour.

## 7. Review workflow

| Stage | Actor | Check |
|---|---|---|
| Draft | Content Writer | Every claim maps to a `knowledge_refs` entry; markers present |
| Self-review | Content Writer | Version banner present; prerequisites and outcome stated |
| Fact review | Fact-Checker | Sampled claims re-checked against the cited knowledge entries |
| QA gate | QA Auditor | `tests/run_checks.sh` passes; see [qa-protocol.md](qa-protocol.md) |
| Publish | Lead Architect | Gate cleared |

Content may be sent back at any stage. A rejection names the specific claim and the
specific missing evidence — not "needs more detail".

## 8. Updates and staleness

When a referenced knowledge entry changes:

1. The content item moves to `status: stale`.
2. The writer re-reads the affected sections against the updated entry.
3. Version scope is recomputed as the union of the new entry scopes.
4. `last_reviewed` is set only when a human or agent has actually re-read it — never
   set automatically.

Deleting a knowledge entry does not delete the content that cites it. The citation
breaks loudly in validation, which is the intended behavior.

## 9. Licensing and reuse

- Original text and structure produced here are project content, licensed separately
  from the evidence.
- Third-party material in `research/raw/` is **never** copied into `content/`. Quotations
  are short, attributed, and limited to what verification requires.
- Community reports used at `V2` attribute the community generally, and never present
  an individual's report as official guidance.

## 10. Phase 3 opening criteria

No content may be authored until Phase 3 is opened by the Lead Architect, which
requires:

- Phase 2 knowledge entries existing at `V3`/`V4` for the topic in question;
- the version inventory in `knowledge/versions/` established from official sources;
- the reference templates in this document validated against at least one real item
  end to end.

`content/` remains empty until then. Placeholder guides written ahead of the evidence
would be indistinguishable, to a reader, from verified ones — which is the exact harm
this project exists to prevent.
