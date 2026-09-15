#!/usr/bin/env bash
#
# Traktor Academy — project check runner.
#
# Run before every commit. Exits non-zero on any violation, which blocks the commit.
# See docs/qa-protocol.md section 2 for the checks and their severity mapping.

set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. The validator is dependency-free but needs Python 3." >&2
  exit 1
fi

exec python3 tests/validate_structure.py "$@"
