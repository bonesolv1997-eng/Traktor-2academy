# `knowledge/` — The Truth Layer

**Layer 2.** The only place in this repository permitted to state what is true about
Traktor. Everything in `content/` and `apps/` derives from here.

Read [../AGENTS.md](../AGENTS.md) before writing an entry, and
[../docs/fact-checking-protocol.md](../docs/fact-checking-protocol.md) before assigning
a verification level.

---

## Rules

1. **One atomic claim per entry.** If it contains "and", it is probably two entries.
2. **No claim without a source id** that exists in `research/sources/`.
3. **Version scope is mandatory** wherever the fact is version-sensitive.
   `traktor_versions: ["unknown"]` is valid. An invented range is not.
4. **Unknown is written as `UNKNOWN`**, never left blank and never guessed.
5. **Never edit `research/raw/`** to support an entry.
6. **Never delete an entry** to resolve an inconsistency — mark it `superseded` or
   `disputed` and link the successor.

## Domain selection

| Directory | Contains | Not |
|---|---|---|
| `software/` | Traktor application features, preferences, panels, behavior | Hardware questions, audio theory |
| `hardware/` | Controllers, interfaces, and **whether** they work with Traktor | How to map them (that is `midi/` or `hid/`) |
| `audio/` | Audio setup, routing, latency, drivers, cueing, recording | DVS timecode specifics |
| `midi/` | MIDI mapping, MIDI messages, mapping files | HID protocol specifics |
| `hid/` | HID protocol, HID mapping, HID vs MIDI differences | Generic MIDI mapping |
| `dvs/` | Timecode control, DVS setup, calibration, control media | General audio routing |
| `troubleshooting/` | Diagnosed problems, causes, verified resolutions | Feature documentation |
| `workflows/` | Verified working practices and complete setups | Step-by-step teaching (that is `content/tutorials/`) |
| `glossary/` | Term definitions — **defined once, linked from everywhere** | Re-defining a term in another domain |
| `versions/` | The version registry and behavior change records | Feature documentation |

**Spans two domains?** File under the primary subject and cross-reference. Never
duplicate the fact — a fact stored twice will eventually be true in one place only.

## Required frontmatter

```yaml
---
id: kb-software-0001
title: <short factual title>
domain: software
status: verified                 # draft | verified | disputed | superseded | unknown
verification_level: V4           # V0 | V1 | V2 | V3 | V4 | VX
version_sensitive: true
traktor_versions: ["unknown"]
sources: ["src-0001"]
last_verified: 2026-09-15
---
```

Validated by `tests/validate_structure.py`. Ids follow `kb-<domain>-####`, are
sequential per domain, and are **never reused**.

## Entry body

```markdown
## Fact
One plain statement. No hedging, no marketing.

## Scope
Versions, operating systems, hardware the fact applies to. UNKNOWN where unknown.

## Evidence
- src-0001 — what that source actually says.

## Unknown
What is not established. Write UNKNOWN if nothing here is unknown.

## Related
Cross-references to other kb ids.
```

## Current state

**Phase 0 — empty by design.** No knowledge entry may be authored until Phase 1 has
produced admissible sources to cite. There is currently nothing in this repository that
is valid evidence, so there is nothing that can honestly be asserted.

An empty knowledge layer with a rigorous protocol will become an authority. A populated
knowledge layer built on recall will not, and cannot be repaired afterwards.
