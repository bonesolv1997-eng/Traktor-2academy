# Research Protocol

How evidence enters Traktor Academy, how it is classified, and what makes a capture
admissible.

**Owner:** Researcher role, ratified by Lead Architect · **Status:** Phase 0

---

## 1. Principle

Research produces **evidence**, not conclusions about Traktor. A researcher's job is
to capture what a source actually says, with enough provenance that someone else can
re-check it later. Interpreting that evidence into a verified fact is the
Fact-Checker's job, in a separate step, by a separate agent.

The separation exists because the agent that hunted for a source becomes attached to
finding one.

## 2. Evidence tiers

| Tier | Source class | Authority |
|---|---|---|
| **T0** | Official NI documentation | Highest. NI manuals (PDF/HTML), official NI knowledge-base and support articles, official release notes and changelogs. |
| **T1** | Official NI-adjacent | NI product pages, official NI support responses, NI-produced video/audio walkthroughs, official NI mapping downloads. |
| **T2** | Third-party manufacturer documentation | Manuals and firmware notes from vendors of Traktor-compatible controllers, interfaces and timecode media. Authoritative for **their hardware**, never for Traktor software behavior. |
| **T3** | Reputable community, attributable | Named reviewers, established tutorial authors, published mapping files with an identifiable author and date. |
| **T4** | Unattributed community | Forum thread replies, social media, comments, hearsay. |

### Classification rules

- Tier is assigned **at capture time** and recorded in the source record. It is a
  property of the source, not of the claim.
- **T1 is not T0.** A product marketing page is official but is not documentation.
  Marketing copy may establish that a feature is *named*; it may not establish *how it
  behaves*.
- A **T2 source describing Traktor software** is downgraded to T3 for that claim.
  Vendor manuals frequently describe Traktor's behavior inaccurately.
- **A source may be official and still wrong**, or right for one version only. Tier
  measures authority, not truth.
- When a page has both official documentation and a forum thread, capture both and
  tier them separately. Do not let the convenient one absorb the other.

### What T3/T4 may do

- Trigger a research task ("someone reports X — is it real?").
- Corroborate a T0–T2 source.
- Establish that a behavior was *reported*, which is itself a fact worth recording in
  `knowledge/troubleshooting/` with a community marker.

### What T3/T4 may never do

- Establish a fact alone. A claim resting only on T3/T4 is capped at `V2` and must
  render with a community-report marker.
- Contradict a T0 source without producing either a newer T0 source or a documented
  reproduction.

## 3. The four research directories

### `research/raw/` — immutable captures

One directory per capture event:

```
research/raw/2026-09-15-ni-traktor-manual/
├── manifest.yml
├── source.html          # or .pdf, .png, .txt, .log
└── notes.md             # optional, additive only
```

`manifest.yml`:

```yaml
capture_id: raw-2026-09-15-ni-traktor-manual
captured_at: 2026-09-15
captured_by: researcher
url: <exact URL at time of capture>
access_method: manual | fetched | provided
tier: T0
version_context: <Traktor version the document covers, or "unknown">
sha256: <hash of the primary file>
notes: <one line>
```

**Rules:** never edit or delete a capture. If a capture was wrong or superseded, add a
new capture and a `notes.md` entry pointing at the old one. Raw captures are the
project's audit trail; a gap in them makes every downstream claim unverifiable.

### `research/sources/` — structured source records

One JSON file per source: `src-####.json`, validated against
[../database/sources.schema.json](../database/sources.schema.json).

```json
{
  "id": "src-0001",
  "title": "Traktor Pro manual",
  "publisher": "Native Instruments",
  "tier": "T0",
  "url": "https://...",
  "captured_at": "2026-09-15",
  "published_at": "unknown",
  "raw_ref": "raw-2026-09-15-ni-traktor-manual",
  "version_context": "unknown",
  "applies_to": ["unknown"],
  "confidence_notes": "",
  "status": "active"
}
```

`status` is `active`, `link_broken`, `superseded` or `withdrawn`. A source is never
deleted — a broken link is recorded, because a claim citing it still needs to explain
why it can no longer be checked.

### `research/reports/` — analysis

`RPT-####-<slug>.md`. Used when several sources bear on one question and the
*reasoning* needs to be preserved, not just the citations. Required sections:
`## Question`, `## Sources consulted`, `## Findings`, `## Gaps`, `## Recommendations`.

The `## Gaps` section is mandatory even when empty. **A report that documents what
could not be found is as valuable as one that documents what was.**

### `research/conflicts/` — contradictions

`CF-####-<slug>.md`. Required sections: `## Claim under dispute`, `## Position A`,
`## Position B`, `## Evidence comparison`, `## Status`, `## Resolution`.

See [fact-checking-protocol.md](fact-checking-protocol.md) §5 for the resolution
ladder. A conflict record is **never** closed by deleting the losing position.

## 4. Capture standards

Every capture must record:

1. **Exact URL** at time of capture — not a cleaned-up or canonicalized version.
2. **Retrieval date.** Web sources change silently; an undated citation is worthless.
3. **Tier**, assigned per §2.
4. **Version context** — which Traktor version(s) the document addresses. `unknown` is
   acceptable and common; a guess is not.
5. **Content hash** of the primary artifact, so later tampering or drift is detectable.

For sources that cannot be captured (paywalled, login-gated, video, deleted pages),
record the metadata, mark `access_method`, and note precisely what could not be
verified. **Never paraphrase a source you did not read into a factual claim.**

## 5. Search discipline

- Record the query used, even when it returned nothing. Negative results prevent the
  next researcher repeating the work and, more importantly, prevent a future agent
  assuming the absence of evidence was never checked.
- Prefer the NI domain and NI support properties first. Exhaust T0/T1 before treating
  T3/T4 as the best available.
- Distinguish **"NI does not document this"** from **"this does not exist."** The
  first is a finding. The second is an inference the evidence usually does not support.
- Community mapping files are data. Record their existence, author, date and target
  version — not a summary of what the author believes.

## 6. Anti-fabrication controls

Non-negotiable, and the reason this protocol is long:

- **No synthetic sources.** A source id must correspond to a real capture in
  `research/raw/`.
- **No reconstructed quotes.** Quote only what is in the capture.
- **No plausible URLs.** If the URL is not the one actually retrieved, the capture is
  invalid.
- **No confident paraphrase of an unread source.** If you did not read it, you may
  only record that it exists.
- **Volume targets never override evidence.** If the request is for fifty entries and
  the evidence supports twelve, deliver twelve and report the shortfall.

A fabricated source is the worst possible failure in this system: it launders an
invented fact into `V4` and it will not be caught by any downstream gate, because
every downstream gate trusts the citation.

## 7. Research request format

When another role needs evidence, the request states:

```yaml
request_id: REQ-####
asked_by: knowledge-engineer
question: <one specific, answerable question>
context: <why it matters, which entry is blocked>
scope: <versions / hardware in question>
acceptance: <what a sufficient answer looks like>
```

Vague requests produce vague research. "Everything about DVS" is not a question;
"Which control vinyl variants does NI document for Traktor Pro, and what speed
settings are specified for each?" is.

## 8. Phase 1 opening criteria

Phase 1 begins when the Lead Architect opens it. Its first deliverables are:

1. The official NI documentation inventory — every T0/T1 source located and captured.
2. The Traktor version inventory in `knowledge/versions/`, built **from official
   sources only**, with no version number entered that is not documented.
3. A source registry in `database/` indexing all captured sources.

Until then, `research/` stays empty apart from this protocol's own conventions, and no
knowledge entry may be authored — there is nothing admissible to cite yet.
