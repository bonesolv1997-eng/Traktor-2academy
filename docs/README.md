# `docs/` — Protocols

**Layer 0 (contract).** The rules that define how Traktor Academy operates. These are
normative, not descriptive: they state what must happen, and `tests/` enforces as much
of them as a machine can.

---

| Document | Governs | Owner |
|---|---|---|
| [architecture.md](architecture.md) | Layers, directory contract, identity scheme, frontmatter, decisions log | Lead Architect |
| [research-protocol.md](research-protocol.md) | Evidence tiers, capture standards, the four research directories | Researcher |
| [fact-checking-protocol.md](fact-checking-protocol.md) | Atomic claims, verification levels V0–V4/VX, conflicts, re-verification | Fact-Checker |
| [content-protocol.md](content-protocol.md) | Content types, provenance markers, review workflow | Content Writer |
| [qa-protocol.md](qa-protocol.md) | Gates, automated checks, severity levels, release criteria | QA Auditor |
| [versioning-strategy.md](versioning-strategy.md) | Traktor version taxonomy and knowledge-base versioning | Versioning Librarian |

Read alongside [../AGENTS.md](../AGENTS.md) (the binding rules) and
[../TRAKTOR-ACADEMY-AGENT-SYSTEM.md](../TRAKTOR-ACADEMY-AGENT-SYSTEM.md) (roles,
pipeline and gates).

## Precedence

When documents disagree:

1. `../AGENTS.md` — the binding contract.
2. The schemas in `../database/` — what is actually enforced.
3. The protocol in this directory.
4. Any `README.md` in a layer directory.

A lower-ranked document that contradicts a higher-ranked one is a bug. Fix it rather
than working around it, and log the decision in `architecture.md` §8.

## Changing a protocol

A protocol change is a governance change: it needs Lead Architect approval, and
wherever the change is machine-checkable it arrives **with** the corresponding check in
`../tests/` in the same commit.

## Deliberate omissions

- **No Traktor version inventory.** That is a Phase 1 deliverable built from official
  NI sources, per `research-protocol.md`. It is not written from memory.
- **No editorial style guide for prose.** Style is S4 under `qa-protocol.md` §3 and
  does not gate publication; traceability does.
- **No technology stack decision.** Deferred to Phase 4 by design — see
  `architecture.md` §7.
