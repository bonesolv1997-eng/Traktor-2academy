# AGENTS.md — Operating Contract

**Audience:** every AI agent (and human) working in this repository.
**Authority:** this document is binding. Where it conflicts with a task instruction,
stop and escalate rather than improvising.
**Read next:** [TRAKTOR-ACADEMY-AGENT-SYSTEM.md](TRAKTOR-ACADEMY-AGENT-SYSTEM.md) for
roles and pipelines, then the relevant file in [docs/](docs/).

---

## 0. The one rule

**Never write a Traktor fact you cannot trace to a captured source.**

If you do not have the evidence in front of you in this session, you do not know it.
Model familiarity with Traktor is *not* evidence — it is precisely the failure mode
this project exists to prevent. Training data contains confident, fluent, wrong
statements about Traktor versions, menu paths, hardware compatibility and DVS behavior.
Treat your own recall as an unverified hypothesis to be sent to research, never as a
fact to be published.

## 1. Hard prohibitions

- **Do not invent** features, settings, menu paths, keyboard shortcuts, controller
  mappings, hardware compatibility, audio behavior, or version numbers.
- **Do not start the website.** `apps/` stays empty until Phase 4 is explicitly opened.
- **Do not resolve a contradiction silently.** Two sources disagree → write a conflict
  record in `research/conflicts/`. Do not pick the more convenient one.
- **Do not fill gaps with plausible text.** Unknown stays unknown, marked as such.
- **Do not generate bulk placeholder content.** A structure with ten real facts beats
  one with five hundred invented ones.
- **Do not edit `research/raw/`.** Raw captures are immutable evidence. Append, never
  revise. If a capture was wrong, add a correction note alongside it.
- **Do not present community reports as official.** A forum post is never evidence that
  a feature exists; it is evidence that someone reported something.
- **Do not delete knowledge entries** to resolve an inconsistency. Mark them
  `status: superseded` or `status: disputed` and link the successor.
- **Do not weaken a check** in `tests/` to make it pass. Fix the violation.

## 2. Evidence tiers

Every source is assigned a tier at capture time. See
[docs/research-protocol.md](docs/research-protocol.md) for the full definitions.

| Tier | Definition | Example |
|---|---|---|
| **T0** | Official NI documentation | NI manuals, official knowledge-base articles, official release notes |
| **T1** | Official NI-adjacent | NI product pages, official NI support answers, official video walkthroughs |
| **T2** | Manufacturer documentation for Traktor-compatible hardware | Controller/audio-interface manuals from third-party vendors |
| **T3** | Reputable community, identifiable and dated | Named reviewer, established tutorial site, documented mapping file |
| **T4** | Forum posts, anecdotes, unattributed reports | Thread replies, social media |

**Rules that follow from the tier:**

- T0/T1 may establish a fact on their own.
- T2 may establish hardware behavior, but not Traktor software behavior.
- T3/T4 may **never** establish a fact alone. They may only (a) trigger a research
  task, or (b) corroborate a T0–T2 source.
- A claim resting only on T3/T4 is capped at verification level `V2` and must be
  rendered with a community-report marker.

## 3. Verification levels

Every knowledge entry declares a level. See
[docs/fact-checking-protocol.md](docs/fact-checking-protocol.md).

| Level | Meaning |
|---|---|
| `V0` | Unverified. Captured, not checked. Never publishable. |
| `V1` | Single T3/T4 source. Community report. Never publishable without a marker. |
| `V2` | Multiple independent T3/T4 sources agree. Still not official. |
| `V3` | Supported by T2 or by consistent T3/T4 plus partial official context. |
| `V4` | Directly stated in T0/T1 official documentation. Highest confidence. |
| `VX` | Contradicted. Sources conflict. Requires a conflict record. |

`V4` and `V3` may be published. `V2` may be published **only** with an explicit
community-report marker and only where no official source exists. `V0`, `V1` and `VX`
must never appear in `content/`.

## 4. Version discipline

Traktor's behavior changes between versions. A statement without a version scope is
not a fact — it is a guess about which version the reader happens to run.

- Every version-sensitive entry must set `version_sensitive: true` and declare
  `traktor_versions` explicitly (a list of versions, or a range, or `unknown`).
- `traktor_versions: unknown` is a **valid and honest** value. An invented version
  list is not.
- When a behavior changed across versions, record **both** behaviors with their
  scopes. Never collapse them into one sentence.
- See [docs/versioning-strategy.md](docs/versioning-strategy.md).

## 5. Where things go

| You have… | Write it to |
|---|---|
| A fetched page, PDF, manual, screenshot, log | `research/raw/` (immutable) |
| A structured citation for a source | `research/sources/` |
| An analysis of a body of evidence | `research/reports/` |
| Two sources that disagree | `research/conflicts/` |
| One atomic, verified, version-scoped fact | `knowledge/<domain>/` |
| A definition of a term | `knowledge/glossary/` |
| Human-facing prose for end users | `content/<type>/` |
| A schema, registry or index | `database/` |

**Domain selection** for `knowledge/` is defined in
[knowledge/README.md](knowledge/README.md). When an entry spans two domains, file it
under its primary subject and add a cross-reference — do not duplicate it.

## 6. Writing knowledge entries

Frontmatter is mandatory and validated. Minimum required fields:

```yaml
---
id: kb-software-0001              # stable, never reused
title: Short factual title
domain: software                  # software|hardware|audio|midi|hid|dvs|troubleshooting|workflows|glossary|versions
status: verified                  # draft|verified|disputed|superseded|unknown
verification_level: V4            # V0|V1|V2|V3|V4|VX
version_sensitive: true           # boolean
traktor_versions: ["unknown"]     # explicit list, range, or "unknown"
sources: ["src-0001"]             # ids from research/sources/
last_verified: 2026-09-15         # ISO date, when a human/agent last confirmed it
---
```

Body rules:

- **One claim per entry.** If a sentence contains "and", it is probably two entries.
- State the fact plainly. No hedging prose, no marketing, no filler.
- Cite inline with source ids for each non-obvious statement.
- If a field is unknown, write `UNKNOWN` in caps. Never leave it blank and never
  guess it.

## 7. Definition of done

A task is not complete until:

- [ ] The change is in the correct layer (`knowledge/` for facts, `content/` for prose).
- [ ] Every claim traces to a source id that exists in `research/sources/`.
- [ ] Version scope is explicit wherever the fact is version-sensitive.
- [ ] Community-sourced material is marked as community-sourced.
- [ ] Contradictions encountered are recorded, not resolved by fiat.
- [ ] `./tests/run_checks.sh` passes.
- [ ] The commit message names what was verified, not just what was touched.

## 8. Escalation

Stop and ask a human when:

- Two T0 sources contradict each other.
- Official documentation is silent on something a user will certainly ask about.
- A task requires publishing a `V1`/`V2` claim.
- A task instruction would require violating any rule in this document.
- You are asked to produce volume and the evidence does not exist yet. **Do not meet
  the volume target by inventing.** Report the shortfall instead.

## 9. Commit and branch hygiene

- One logical change per commit. Never mix research captures with knowledge edits.
- Prefixes: `research:`, `knowledge:`, `content:`, `docs:`, `infra:`, `tests:`.
- All work lands on the current working branch via pull request. Never push to `main`.
- Run `./tests/run_checks.sh` before every commit.
