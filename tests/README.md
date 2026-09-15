# `tests/` — Validation

**Layer 0 (contract).** The project's principles are only real if something fails when
they are broken. This directory holds that something.

---

## Running

```bash
./tests/run_checks.sh
```

Or directly:

```bash
python3 tests/validate_structure.py
```

Exits `0` on success, `1` on any violation. No third-party dependencies — it runs on a
bare Python 3 install, because a check that needs setup is a check that gets skipped.

## What it enforces

| # | Check |
|---|---|
| A1 | Directory contract — every required directory exists |
| A2 | Required governance documents exist and are non-empty |
| A3 | Required sections present in each `docs/` protocol |
| A4 | Every internal Markdown link resolves to an existing path |
| A5 | Knowledge frontmatter parses and carries all required fields |
| A6 | `verification_level` and `status` use permitted values |
| A7 | Version-sensitive entries declare a non-empty `traktor_versions` |
| A8 | `sources` non-empty and correctly formatted |
| A9 | `V3`/`V4` cite a source; `VX` links a conflict record |
| A10 | Content carries non-empty `knowledge_refs` |
| A11 | Content declares `traktor_versions` |
| A12 | Source records validate against `database/sources.schema.json` |
| A13 | Conflict records contain all required sections |
| A14 | No banned placeholder or fabrication patterns |
| A15 | No application code in `apps/` before Phase 4 |

Severity mapping for these checks is in [../docs/qa-protocol.md](../docs/qa-protocol.md) §3.

## Rules for changing the checks

- **Never weaken a check to make it pass.** The fix belongs in the content.
- A new protocol rule in `docs/` should arrive with the check that enforces it, in the
  same commit. An unenforced rule is a wish.
- Removing or relaxing a check requires Lead Architect approval and a decision logged
  in `../docs/architecture.md` §8.

## What this cannot check

Stated plainly, so nobody mistakes a green run for a verified knowledge base:

- **Whether a source actually says what an entry claims.** That is the manual audit in
  [../docs/qa-protocol.md](../docs/qa-protocol.md) §4, and it is the most important
  check in the project.
- **Whether a claim is true.** Automation verifies traceability and structure. Truth
  requires evidence and a reader.
- **Whether content is well written.** Structure passes; clarity may not.

A passing run means the system's *shape* is intact. It does not mean the facts are
right, and no one should read it that way.

## Current state

Phase 0. The validator runs against the infrastructure itself; as `research/`,
`knowledge/` and `content/` fill, the same checks begin doing real work.
