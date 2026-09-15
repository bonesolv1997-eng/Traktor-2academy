#!/usr/bin/env python3
"""
Traktor Academy — structural and protocol validation.

Enforces the directory contract, the governance documents, the frontmatter schemas,
citation integrity, link integrity and the phase-4 lock on apps/.

Dependency-free by design: a check that needs an install step is a check that gets
skipped. Run via tests/run_checks.sh.

Exit 0 = pass, 1 = one or more violations.
"""

from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Severity per docs/qa-protocol.md section 3.
S1 = "S1 CRITICAL"
S2 = "S2 MAJOR"
S3 = "S3 MODERATE"
S4 = "S4 MINOR"

violations: list[tuple[str, str, str]] = []


def fail(check: str, severity: str, message: str) -> None:
    violations.append((check, severity, message))


# --------------------------------------------------------------------------
# A1 — directory contract
# --------------------------------------------------------------------------

REQUIRED_DIRS = [
    "research/raw",
    "research/reports",
    "research/sources",
    "research/conflicts",
    "knowledge/software",
    "knowledge/hardware",
    "knowledge/audio",
    "knowledge/midi",
    "knowledge/hid",
    "knowledge/dvs",
    "knowledge/troubleshooting",
    "knowledge/workflows",
    "knowledge/glossary",
    "knowledge/versions",
    "content/guides",
    "content/tutorials",
    "content/courses",
    "content/faq",
    "content/reference",
    "database",
    "apps",
    "tests",
    "docs",
]

# --------------------------------------------------------------------------
# A2 — required governance documents
# --------------------------------------------------------------------------

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "TRAKTOR-ACADEMY-AGENT-SYSTEM.md",
    "docs/architecture.md",
    "docs/research-protocol.md",
    "docs/fact-checking-protocol.md",
    "docs/content-protocol.md",
    "docs/qa-protocol.md",
    "docs/versioning-strategy.md",
    "database/sources.schema.json",
    "tests/validate_structure.py",
    "tests/run_checks.sh",
]

# --------------------------------------------------------------------------
# A3 — required sections
# --------------------------------------------------------------------------

REQUIRED_SECTIONS: dict[str, list[str]] = {
    "AGENTS.md": [
        "one rule",
        "Hard prohibitions",
        "Evidence tiers",
        "Verification levels",
        "Version discipline",
        "Where things go",
        "Writing knowledge entries",
        "Definition of done",
        "Escalation",
        "Commit and branch hygiene",
    ],
    "TRAKTOR-ACADEMY-AGENT-SYSTEM.md": [
        "Why a system",
        "Roles",
        "Pipeline",
        "Gates",
        "Conflict handling",
        "Staleness",
        "Artifacts and naming",
        "Phase authority",
    ],
    "docs/architecture.md": [
        "Design goals",
        "Layers",
        "Directory contract",
        "Identity scheme",
        "Frontmatter contract",
        "unknown convention",
        "Technology decisions",
        "Decisions log",
        "Phase status",
    ],
    "docs/research-protocol.md": [
        "Principle",
        "Evidence tiers",
        "four research directories",
        "Capture standards",
        "Search discipline",
        "Anti-fabrication controls",
        "Research request format",
        "Phase 1 opening criteria",
    ],
    "docs/fact-checking-protocol.md": [
        "claim is the unit",
        "Verification levels",
        "Version scoping",
        "What counts as verification",
        "Conflicts",
        "Re-verification",
        "Audit sampling",
        "honest-unknown",
    ],
    "docs/content-protocol.md": [
        "Principle",
        "Content types",
        "Frontmatter",
        "Carrying provenance",
        "Writing standards",
        "Structure requirements",
        "Review workflow",
        "Updates and staleness",
        "Licensing",
        "Phase 3 opening criteria",
    ],
    "docs/qa-protocol.md": [
        "Principle",
        "Automated gate",
        "Severity levels",
        "Manual audit",
        "Release gate",
        "Re-verification windows",
        "Health metrics",
        "What QA does not do",
    ],
    "docs/versioning-strategy.md": [
        "core problem",
        "Version identifier syntax",
        "version registry",
        "Behavior change records",
        "Cross-version claims",
        "Knowledge-base versioning",
        "Per-entry versioning",
        "Tags, branches",
        "Open questions",
    ],
}

# --------------------------------------------------------------------------
# A5/A6 — knowledge and content schemas
# --------------------------------------------------------------------------

KNOWLEDGE_REQUIRED = [
    "id",
    "title",
    "domain",
    "status",
    "verification_level",
    "version_sensitive",
    "traktor_versions",
    "sources",
    "last_verified",
]

CONTENT_REQUIRED = [
    "title",
    "type",
    "status",
    "knowledge_refs",
    "traktor_versions",
    "last_reviewed",
]

DOMAINS = {
    "software",
    "hardware",
    "audio",
    "midi",
    "hid",
    "dvs",
    "troubleshooting",
    "workflows",
    "glossary",
    "versions",
}
KB_STATUS = {"draft", "verified", "disputed", "superseded", "unknown"}
V_LEVELS = {"V0", "V1", "V2", "V3", "V4", "VX"}
CONTENT_TYPES = {"guide", "tutorial", "course", "faq", "reference"}
CONTENT_STATUS = {"draft", "reviewed", "published", "stale"}

ISO_DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
SRC_ID = re.compile(r"^src-[0-9]{4,}$")
KB_ID = re.compile(r"^kb-[a-z]+-[0-9]{4,}$")

# A14 — banned patterns. Case-sensitive on purpose.
BANNED = [
    "Lorem ipsum",
    "PLACEHOLDER",
    "TODO: invent",
    "as an AI language model",
]

APP_CODE_EXTS = {
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".py", ".rb", ".go", ".rs",
    ".html", ".css", ".scss", ".vue", ".svelte", ".php", ".java",
}

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", ".cache", "dist", "build"}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def rel(path: str) -> str:
    return os.path.relpath(path, ROOT)


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def walk_files() -> list[str]:
    out: list[str] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            out.append(os.path.join(dirpath, name))
    return sorted(out)


def parse_frontmatter(text: str) -> tuple[dict, str] | None:
    """Minimal YAML-frontmatter parser.

    Supports the flat `key: value` form plus inline and block lists, which is all the
    project's schemas use. Deliberately not a general YAML parser.
    """
    if not text.startswith("---"):
        return None
    lines = text.split("\n")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None

    data: dict[str, object] = {}
    body = "\n".join(lines[end + 1:])
    current_key: str | None = None

    for raw_line in lines[1:end]:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.lstrip().startswith("- ") and current_key:
            item = raw_line.lstrip()[2:].strip().strip("'\"")
            value = data.get(current_key)
            if not isinstance(value, list):
                value = []
                data[current_key] = value
            value.append(item)
            continue

        if ":" not in raw_line:
            continue
        key, _, value = raw_line.partition(":")
        key = key.strip()
        value = value.strip()
        current_key = key

        if value == "":
            data[key] = []
            continue
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if not inner:
                data[key] = []
            else:
                data[key] = [p.strip().strip("'\"") for p in inner.split(",")]
            continue

        value = value.strip("'\"")
        if value.lower() in ("true", "false"):
            data[key] = value.lower() == "true"
        else:
            data[key] = value

    return data, body


def markdown_files() -> list[str]:
    return [p for p in walk_files() if p.endswith(".md")]


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

def check_directories() -> None:
    for d in REQUIRED_DIRS:
        if not os.path.isdir(os.path.join(ROOT, d)):
            fail("A1", S1, f"required directory missing: {d}/")


def check_required_files() -> None:
    for f in REQUIRED_FILES:
        full = os.path.join(ROOT, f)
        if not os.path.isfile(full):
            fail("A2", S1, f"required file missing: {f}")
        elif os.path.getsize(full) == 0:
            fail("A2", S2, f"required file is empty: {f}")


def check_sections() -> None:
    for doc, sections in REQUIRED_SECTIONS.items():
        full = os.path.join(ROOT, doc)
        if not os.path.isfile(full):
            continue  # already reported by A2
        headings = [
            line.lstrip("#").strip().lower()
            for line in read(full).split("\n")
            if line.lstrip().startswith("#")
        ]
        joined = "\n".join(headings)
        for section in sections:
            if section.lower() not in joined:
                fail("A3", S3, f"{doc}: missing required section '{section}'")


LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")


def check_links() -> None:
    for path in markdown_files():
        text = read(path)
        for _, target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#", "urn:")):
                continue
            clean = target.split("#")[0]
            if not clean:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), clean))
            if not os.path.exists(resolved):
                fail("A4", S3, f"{rel(path)}: broken internal link -> {target}")


def check_knowledge() -> None:
    entries = [
        p
        for p in markdown_files()
        if p.startswith(os.path.join(ROOT, "knowledge") + os.sep)
        and os.path.basename(p) != "README.md"
    ]
    for path in entries:
        where = rel(path)
        parsed = parse_frontmatter(read(path))
        if parsed is None:
            fail("A5", S2, f"{where}: no YAML frontmatter")
            continue
        data, body = parsed

        for field in KNOWLEDGE_REQUIRED:
            if field not in data or data[field] in ("", []):
                fail("A5", S2, f"{where}: missing required frontmatter field '{field}'")

        domain = data.get("domain")
        if domain is not None and domain not in DOMAINS:
            fail("A6", S2, f"{where}: invalid domain '{domain}'")

        status = data.get("status")
        if status is not None and status not in KB_STATUS:
            fail("A6", S2, f"{where}: invalid status '{status}'")

        level = data.get("verification_level")
        if level is not None and level not in V_LEVELS:
            fail("A6", S2, f"{where}: invalid verification_level '{level}'")

        kb_id = data.get("id")
        if isinstance(kb_id, str) and kb_id and not KB_ID.match(kb_id):
            fail("A5", S3, f"{where}: id '{kb_id}' does not match kb-<domain>-####")

        # A7 — version scope
        sensitive = data.get("version_sensitive")
        versions = data.get("traktor_versions")
        if sensitive is True and (not isinstance(versions, list) or not versions):
            fail("A7", S2, f"{where}: version_sensitive but traktor_versions is empty")

        # A8 — sources
        sources = data.get("sources")
        if level in ("V3", "V4"):
            if not isinstance(sources, list) or not sources:
                fail("A9", S1, f"{where}: {level} entry cites no sources")
            else:
                for sid in sources:
                    if not SRC_ID.match(str(sid)):
                        fail("A8", S3, f"{where}: malformed source id '{sid}'")

        # A9 — disputed entries must link a conflict record
        if level == "VX" and "CF-" not in body:
            fail("A9", S2, f"{where}: VX (contradicted) entry links no CF- conflict record")

        last = data.get("last_verified")
        if isinstance(last, str) and last and not ISO_DATE.match(last):
            fail("A5", S3, f"{where}: last_verified '{last}' is not an ISO date")


def check_content() -> None:
    items = [
        p
        for p in markdown_files()
        if p.startswith(os.path.join(ROOT, "content") + os.sep)
        and os.path.basename(p) != "README.md"
    ]
    for path in items:
        where = rel(path)
        parsed = parse_frontmatter(read(path))
        if parsed is None:
            fail("A10", S2, f"{where}: no YAML frontmatter")
            continue
        data, _ = parsed

        for field in CONTENT_REQUIRED:
            if field not in data or data[field] in ("", []):
                fail("A10", S2, f"{where}: missing required frontmatter field '{field}'")

        ctype = data.get("type")
        if ctype is not None and ctype not in CONTENT_TYPES:
            fail("A10", S2, f"{where}: invalid type '{ctype}'")

        cstatus = data.get("status")
        if cstatus is not None and cstatus not in CONTENT_STATUS:
            fail("A10", S2, f"{where}: invalid status '{cstatus}'")

        refs = data.get("knowledge_refs")
        if isinstance(refs, list) and refs:
            for ref in refs:
                if not KB_ID.match(str(ref)):
                    fail("A10", S3, f"{where}: malformed knowledge_ref '{ref}'")

        # A11 — content must declare a version scope
        if "traktor_versions" not in data or data["traktor_versions"] in ("", []):
            fail("A11", S2, f"{where}: content declares no traktor_versions")

        reviewed = data.get("last_reviewed")
        if isinstance(reviewed, str) and reviewed and not ISO_DATE.match(reviewed):
            fail("A10", S3, f"{where}: last_reviewed '{reviewed}' is not an ISO date")


def load_schema() -> dict | None:
    path = os.path.join(ROOT, "database", "sources.schema.json")
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        fail("A12", S1, f"database/sources.schema.json is not valid JSON: {exc}")
        return None


def check_sources() -> None:
    schema = load_schema()
    src_dir = os.path.join(ROOT, "research", "sources")
    records = [
        p for p in walk_files()
        if p.startswith(src_dir + os.sep) and p.endswith(".json")
    ]
    if schema is None:
        if records:
            fail("A12", S1, "source records exist but schema is unavailable")
        return

    required = schema.get("required", [])
    props = schema.get("properties", {})

    for path in records:
        where = rel(path)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            fail("A12", S1, f"{where}: invalid JSON: {exc}")
            continue

        if not isinstance(data, dict):
            fail("A12", S1, f"{where}: top level must be an object")
            continue

        for field in required:
            if field not in data or data[field] in ("", [], None):
                fail("A12", S2, f"{where}: missing required field '{field}'")

        if schema.get("additionalProperties") is False:
            for key in data:
                if key not in props:
                    fail("A12", S3, f"{where}: field '{key}' is not in the schema")

        for key, spec in props.items():
            if key not in data:
                continue
            value = data[key]
            enum = spec.get("enum")
            if enum and value not in enum:
                fail("A12", S2, f"{where}: '{key}' = {value!r} not in {enum}")
            pattern = spec.get("pattern")
            if pattern and isinstance(value, str) and not re.match(pattern, value):
                fail("A12", S2, f"{where}: '{key}' = {value!r} does not match {pattern}")
            expected = spec.get("type")
            if expected == "array" and not isinstance(value, list):
                fail("A12", S3, f"{where}: '{key}' must be an array")
            min_items = spec.get("minItems")
            if min_items and isinstance(value, list) and len(value) < min_items:
                fail("A12", S3, f"{where}: '{key}' needs at least {min_items} item(s)")


CONFLICT_SECTIONS = [
    "Claim under dispute",
    "Position A",
    "Position B",
    "Evidence comparison",
    "Status",
    "Resolution",
]


def check_conflicts() -> None:
    cf_dir = os.path.join(ROOT, "research", "conflicts")
    for path in markdown_files():
        if not path.startswith(cf_dir + os.sep):
            continue
        if os.path.basename(path) == "README.md":
            continue
        where = rel(path)
        text = read(path).lower()
        for section in CONFLICT_SECTIONS:
            if section.lower() not in text:
                fail("A13", S2, f"{where}: conflict record missing section '{section}'")


def check_banned() -> None:
    # This file is the check definition, not content: the banned tokens appear here as
    # the patterns to look for. Exempting it is not weakening the check — every content
    # file is still scanned.
    self_path = os.path.abspath(__file__)
    for path in walk_files():
        if not path.endswith((".md", ".json", ".yml", ".yaml", ".txt", ".py", ".sh")):
            continue
        if os.path.abspath(path) == self_path:
            continue
        where = rel(path)
        text = read(path)
        for token in BANNED:
            if token in text:
                fail("A14", S1, f"{where}: banned pattern '{token}'")


def check_apps_locked() -> None:
    apps_dir = os.path.join(ROOT, "apps")
    if not os.path.isdir(apps_dir):
        return
    for dirpath, dirnames, filenames in os.walk(apps_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if os.path.splitext(name)[1].lower() in APP_CODE_EXTS:
                fail(
                    "A15",
                    S2,
                    f"{rel(os.path.join(dirpath, name))}: application code in apps/ "
                    "before Phase 4 (see docs/architecture.md §8, decision D-005)",
                )


def main() -> int:
    check_directories()
    check_required_files()
    check_sections()
    check_links()
    check_knowledge()
    check_content()
    check_sources()
    check_conflicts()
    check_banned()
    check_apps_locked()

    md = len(markdown_files())
    kb = len([
        p for p in markdown_files()
        if p.startswith(os.path.join(ROOT, "knowledge") + os.sep)
        and os.path.basename(p) != "README.md"
    ])
    ct = len([
        p for p in markdown_files()
        if p.startswith(os.path.join(ROOT, "content") + os.sep)
        and os.path.basename(p) != "README.md"
    ])
    src = len([
        p for p in walk_files()
        if p.startswith(os.path.join(ROOT, "research", "sources") + os.sep)
        and p.endswith(".json")
    ])

    print("Traktor Academy — validation")
    print("=" * 60)
    print(f"directories required : {len(REQUIRED_DIRS)}")
    print(f"governance documents : {len(REQUIRED_FILES)}")
    print(f"markdown files       : {md}")
    print(f"knowledge entries    : {kb}")
    print(f"content items        : {ct}")
    print(f"source records       : {src}")
    print("-" * 60)

    if violations:
        print(f"FAIL — {len(violations)} violation(s):\n")
        for check, severity, message in violations:
            print(f"  [{check}][{severity}] {message}")
        print()
        print("A failing check blocks the commit. Fix the violation, not the check.")
        return 1

    print("PASS — all checks clean.")
    print()
    print("Note: this validates structure and traceability only. It cannot verify that a")
    print("source actually says what an entry claims. See docs/qa-protocol.md §4.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
