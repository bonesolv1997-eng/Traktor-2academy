# `research/` — The Evidence Layer

**Layer 1.** Everything the project knows about Traktor ultimately traces back to a
capture held here. Read [../docs/research-protocol.md](../docs/research-protocol.md)
before capturing anything.

---

## Directories

| Directory | Holds | Mutability |
|---|---|---|
| `raw/` | Captured artifacts — pages, PDFs, manuals, screenshots, logs. One directory per capture with a `manifest.yml`. | **Immutable.** Append corrections, never revise. |
| `sources/` | Structured source records, `src-####.json`, validated against [../database/sources.schema.json](../database/sources.schema.json). | Update `status` as links break or sources are superseded. |
| `reports/` | Analysis across multiple sources, `RPT-####-<slug>.md`. | Additive. |
| `conflicts/` | Recorded contradictions, `CF-####-<slug>.md`. | Status advances; positions are never deleted. |

## The tier assigned at capture time

| Tier | Source |
|---|---|
| T0 | Official NI documentation — manuals, knowledge base, release notes |
| T1 | Official NI-adjacent — product pages, official support answers, official videos |
| T2 | Third-party hardware manufacturer documentation |
| T3 | Reputable, attributable community sources |
| T4 | Forums, anecdotes, unattributed reports |

T0/T1 can establish a fact alone. T2 can establish hardware behavior but never Traktor
software behavior. **T3/T4 can never establish a fact alone** — they trigger research or
corroborate, and cap any claim at `V2`.

## Every capture records

Exact URL · retrieval date · tier · version context · content hash.

An undated citation is worthless, because web sources change silently and a claim that
cannot be re-checked cannot be maintained.

## Negative results are findings

Record the query even when it found nothing, and state plainly when NI does not
document something. **"NI does not document this" is a finding. "This does not exist"
is an inference** the evidence usually does not support — and the gap between those two
sentences is where most fabricated knowledge bases go wrong.

## Current state

**Phase 0 — empty by design.** Phase 1 opens the source corpus: the official NI
documentation inventory, the Traktor version registry built from official sources, and
the source registry index.
