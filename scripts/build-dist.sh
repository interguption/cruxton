#!/usr/bin/env bash
# Build the distributable skill zip: dist/cruxton-decision-records.zip
#
# This is (1) the claude.ai upload (Settings → Features → Skills) and
# (2) a GitHub release asset. It packages the self-contained skill bundle at
# skills/cruxton-decision-records/ — nothing else. Run from anywhere in the repo.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SKILL_PARENT="skills"
SKILL_NAME="cruxton-decision-records"
OUT_DIR="dist"
OUT="$OUT_DIR/$SKILL_NAME.zip"

if [ ! -f "$SKILL_PARENT/$SKILL_NAME/SKILL.md" ]; then
  echo "error: $SKILL_PARENT/$SKILL_NAME/SKILL.md not found — run this from the Cruxton repo." >&2
  exit 1
fi

command -v zip >/dev/null 2>&1 || { echo "error: 'zip' is not installed." >&2; exit 1; }

mkdir -p "$OUT_DIR"
rm -f "$OUT"

# Archive contains cruxton-decision-records/SKILL.md, …/bootstrap.py, …/templates/*.
# -X drops extra OS attributes; exclude caches and OS cruft so the asset is clean.
( cd "$SKILL_PARENT" && zip -r -X "../$OUT" "$SKILL_NAME" \
    -x '*/__pycache__/*' -x '*.pyc' -x '*/.DS_Store' >/dev/null )

echo "Built $OUT"
unzip -l "$OUT"
