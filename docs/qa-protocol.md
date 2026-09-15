# QA Protocol

The gates, severity levels and release criteria for Traktor Academy. QA is the only
function with authority to block publication.

**Owner:** QA Auditor role · **Status:** Phase 0

---

## 1. Principle

QA does not judge whether content is *good*. It judges whether content is
**traceable, version-scoped, and consistent with its evidence.** Quality is the
writer's job; verifiability is QA's.

A piece of content can be beautifully written and still fail QA — because it states
something no source supports. That failure is the important one.

## 2. Automated gate

```bash
./tests/run_checks.sh
```

Runs `tests/validate_structure.py`, which enforces:

| # | Check |
|---|---|
| A1 | Directory contract: every required directory exists |
| A2 | Required governance documents exist and are non-empty |
| A3 | Required protocol sections present in each `docs/` file |
| A4 | Every internal Markdown link in the repo resolves to an existing path |
| A5 | Knowledge frontmatter parses and carries all required fields |
| A6 | `verification_level` and `status` use permitted values |
| A7 | Version-sensitive entries declare a non-empty `traktor_versions` |
| A8 | `sources` ids are non-empty and correctly formatted |
| A9 | `V3`/`V4` entries cite at least one source; `VX` entries link a conflict record |
| A10 | Content frontmatter carries non-empty `knowledge_refs` |
| A11 | Content `traktor_versions` is declared |
| A12 | Source records validate against `database/sources.schema.json` |
| A13 | Conflict records contain all required sections |
| A14 | No banned placeholder or fabrication patterns anywhere in the repo |
| A15 | No `apps/` application code exists before Phase 4 |

The check exits non-zero on any violation. **A failing check blocks the commit.** An
agent may not weaken, skip or annotate-away a check to make it pass — the fix belongs
in the content, not the validator.

## 3. Severity levels

| Level | Definition | Action |
|---|---|---|
| **S1 Critical** | A published claim is unsupported, contradicts its source, or is invented. | Block immediately. Remove or mark. Notify Lead Architect same cycle. |
| **S2 Major** | Version scope missing or wrong; community report presented as official; a `V0`/`V1`/`VX` entry reached `content/`. | Block the affected item. Fix before publication. |
| **S3 Moderate** | Frontmatter incomplete, marker missing, dead citation, stale `last_reviewed`. | Fix before merge; does not block unrelated items. |
| **S4 Minor** | Style, structure, clarity, naming. | Track and fix opportunistically. |

**S1 is the only level that triggers retrospective retraction.** Anything already
published at S1 is corrected in place with a visible correction note — never silently
rewritten, because readers may have already acted on it.

## 4. Manual audit

Automation catches structure, not meaning. Each cycle the QA Auditor samples entries
and content and answers, for each:

1. **Does the cited source exist and is it `active`?**
2. **Does the source actually state the claim**, at the claimed version scope?
3. **Is the verification level justified** by the tier of the best source?
4. **Is the version scope consistent** with the source's version context?
5. **Are markers carried through** from knowledge into content?
6. **Is any "unknown" actually a gap that could be filled**, or correctly recorded?

Failure on (2) or (3) is **S1**. Failure on (4) or (5) is **S2**.

Sample size: every entry touched since the last cycle, plus a random sample of
untouched ones. Newly authored entries are audited at 100% until a role has three
clean cycles.

## 5. Release gate

Publication requires all of:

- [ ] `./tests/run_checks.sh` passes clean.
- [ ] Fact review complete for the item.
- [ ] Manual audit sample for the cycle complete, no open S1 or S2.
- [ ] Version banner present and consistent with `traktor_versions`.
- [ ] Community-report markers present wherever a `V2` source is used.
- [ ] Unknowns stated explicitly, not omitted.
- [ ] `last_reviewed` set by whoever actually reviewed it.
- [ ] Lead Architect sign-off.

## 6. Re-verification windows

Entries past their window are not deleted — they are queued for re-verification, and
content derived from them is marked stale.

| Verification level | Re-verify within |
|---|---|
| `V4` (official, current version) | 12 months, or immediately on a new Traktor release in scope |
| `V4` (official, legacy version) | 24 months — legacy behavior changes rarely |
| `V3` | 6 months |
| `V2` (community) | 3 months |
| `VX` (disputed) | On conflict resolution, no fixed window |

**Any new Traktor release triggers immediate review of every entry whose
`traktor_versions` intersects it**, regardless of age. This is the Versioning
Librarian's responsibility and the project's primary defense against silent staleness.

## 7. Health metrics

Tracked per cycle:

- Share of published claims at `V3`/`V4` — target: rising.
- Share of content carrying a version banner — target: 100% of version-sensitive items.
- Open conflicts, and their age — a healthy count is **non-zero and shrinking**.
- Entries past their re-verification window.
- Entries marked `unknown` — **expected to be substantial.** A near-zero count means
  the project has stopped admitting what it does not know, which is an S1 in itself.
- Mean time from a Traktor release to re-verification of affected entries.

## 8. What QA does not do

- Does not rewrite content. Findings name the problem and its owner.
- Does not resolve conflicts. That is the Fact-Checker's ladder, per
  [fact-checking-protocol.md](fact-checking-protocol.md) §5.
- Does not decide phase openings. That is the Lead Architect.
- Does not approve its own exceptions. A waiver requires the Lead Architect and is
  recorded in `docs/architecture.md` §8.
