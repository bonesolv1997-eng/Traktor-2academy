# Fact-Checking Protocol

How a captured source becomes a verified fact, how version scope is attached, and what
happens when sources disagree.

**Owner:** Fact-Checker role · **Status:** Phase 0

---

## 1. The claim is the unit

Verification operates on **atomic claims**, not documents or paragraphs.

An atomic claim is a single testable statement about one thing:

- ✅ "Traktor's audio setup exposes a latency control." *(atomic — though it still
  needs a version scope and a source)*
- ❌ "Traktor has flexible audio routing and low latency, making it suitable for DVS."
  *(three claims, two of them evaluative, one of them unsupportable)*

Split compound claims before verifying them. A claim joined by "and" is usually two
claims. Evaluative claims ("suitable", "easy", "best") are not verifiable facts and
belong in `content/` as clearly attributed opinion, or nowhere at all.

## 2. Verification levels

| Level | Definition | Publishable? |
|---|---|---|
| `V0` | Captured, not yet checked. | No |
| `V1` | Single T3/T4 source. A community report. | No |
| `V2` | Multiple independent T3/T4 sources agree; no official source. | Only with a community-report marker, and only where no official source exists |
| `V3` | T2 source, or consistent T3/T4 corroborated by partial official context. | Yes, with source shown |
| `V4` | Directly stated in T0/T1 official documentation. | Yes |
| `VX` | Contradicted. A conflict record exists. | No — must be resolved or clearly presented as disputed |

### Assignment rules

- **Independence is real or it isn't.** Three forum posts repeating the same tutorial
  are one source. Copy-paste chains are extremely common in DJ communities and inflate
  apparent corroboration. Check whether the "independent" sources cite each other.
- **A Fact-Checker may downgrade anything, and may never upgrade above what the
  sources' tiers permit.** Two T4 sources cannot produce `V3`.
- **Official context is not official confirmation.** A T0 document mentioning a feature
  in passing does not verify a detailed behavioral claim about it. The document must
  actually state the claim.
- **Absence of contradiction is not verification.** `V2` never becomes `V3` by
  surviving a while.
- When in doubt, assign the **lower** level. Downgrading later is cheap; retracting a
  published wrong fact is not.

## 3. Version scoping

A fact about Traktor is a fact about **some version of Traktor**. Every
version-sensitive entry declares its scope.

```yaml
version_sensitive: true
traktor_versions: ["unknown"]     # honest
traktor_versions: ["4.x"]         # scoped
traktor_versions: ["3.0", "3.1"]  # enumerated
```

Rules:

- `version_sensitive: true` with `traktor_versions: ["unknown"]` is **valid**. It means
  "this is version-dependent and we have not established the range." That is a real
  state of knowledge and is far better than a guessed range.
- `version_sensitive: false` asserts the fact holds across all versions in scope.
  **That is a strong claim and needs evidence for it**, not just an absence of
  contrary evidence. Most UI and behavior facts are version-sensitive.
- Where behavior **changed** between versions, record both behaviors as separate
  entries with their own scopes, plus a change record in `knowledge/versions/`. Never
  write "in older versions X, but now Y" as a single unsourced sentence — each half
  needs its own evidence.
- Version identifiers must match the taxonomy in
  [versioning-strategy.md](versioning-strategy.md). Inventing a version string is
  inventing a fact.

## 4. What counts as verification

For each claim, the Fact-Checker records:

```yaml
claim: <the atomic statement>
source_ids: ["src-0007", "src-0012"]
tier_of_best_source: T0
what_the_source_says: <exact quote or precise paraphrase>
version_context_of_source: <from the source record>
verification_level: V4
checked_by: fact-checker
checked_at: 2026-09-15
```

`what_the_source_says` is mandatory. It forces the check to be about the source's
actual words rather than the checker's impression of them, and it makes a later audit
possible without re-fetching everything.

### Reproduction

Where a claim can be tested — a mapping behaves a certain way, a DVS setup calibrates —
a documented reproduction in `research/reports/` is strong evidence. It must record:
software version, OS and version, hardware model and firmware, driver version, exact
steps, observed result. **An undocumented reproduction is an anecdote** and enters at
T4.

## 5. Conflicts

A conflict is recorded, never silently resolved.

**Trigger:** two sources of any tier disagree about a claim, or a source disagrees with
a previously verified entry.

**Record** (`research/conflicts/CF-####-<slug>.md`):

```markdown
# CF-0001 — <short description>

## Claim under dispute
<the atomic claim>

## Position A
<statement> — sources: src-0004 (T0), version context: <...>

## Position B
<statement> — sources: src-0019 (T3), version context: <...>

## Evidence comparison
<tier, recency, version context, independence, reproducibility>

## Status
open | investigating | resolved | unresolvable

## Resolution
<outcome, basis, decided_by, decided_at>
```

**Resolution ladder, in order of preference:**

1. A **T0/T1 source** that directly addresses the claim and its version context.
2. **Documented reproduction** on the specific software/hardware versions in dispute.
3. **Version reconciliation** — frequently both positions are correct within their own
   version scope. This is the most common real resolution and is a finding, not a
   failure.
4. **Explicit human decision**, recorded with name and date.

**Automatic escalation to a human:** two T0 sources in conflict. This almost always
means the behavior is version-dependent, or the documentation itself is inconsistent —
both of which a human needs to see.

**Never acceptable:** deleting the weaker position, averaging the two, or adopting
whichever is more convenient for the content being written.

The affected knowledge entry moves to `verification_level: VX`, `status: disputed`,
linked to the conflict record. It is not published while disputed.

## 6. Re-verification and decay

Every entry carries `last_verified`. Re-verification is triggered by:

- a new Traktor release intersecting the entry's `traktor_versions`;
- a source record moving to `link_broken`, `superseded` or `withdrawn`;
- age beyond the threshold in [qa-protocol.md](qa-protocol.md);
- a user or community report contradicting the entry.

Re-verification means **re-reading the source**, not re-asserting the claim. If the
source no longer says it, the level drops — even if the fact is probably still true.

## 7. Audit sampling

The QA Auditor re-checks a sample of entries against their sources each cycle. The
audit asks, for each sampled entry:

1. Does the cited source exist in `research/sources/` and is it `active`?
2. Does it actually state the claim, at the version scope claimed?
3. Is the verification level justified by the tier of the best source?
4. Is the version scope consistent with the source's version context?

Failure on (2) or (3) is a **critical** severity finding — see
[qa-protocol.md](qa-protocol.md) §3.

## 8. The honest-unknown requirement

Every research pass must report what it could **not** establish. Entries marked
`status: unknown` with `verification_level: V0` and body text `UNKNOWN` are expected
output, not failure output.

A knowledge base with zero unknowns is not thorough. It is fabricated.
