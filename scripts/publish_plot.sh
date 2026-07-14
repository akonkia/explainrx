#!/usr/bin/env bash
#
# publish_plot.sh — copy the latest crawl-progress SVG into the GitHub repo and
# push it, so the plot embedded in the README stays up to date. Idempotent:
# clones the repo on first run, pulls on later runs, only commits when the plot
# actually changed, and adds the README embed once if it's missing.
#
# Usage:
#   ./scripts/publish_plot.sh
# Override defaults via env:
#   REPO_SSH=git@github.com:akonkia/explainrx.git \
#   CLONE_DIR="$HOME/.explainrx-publish" ./scripts/publish_plot.sh

set -euo pipefail

REPO_SSH="${REPO_SSH:-git@github.com:akonkia/explainrx.git}"
CLONE_DIR="${CLONE_DIR:-$HOME/.explainrx-publish}"
PROJECT="${PROJECT:-/Users/akonkia/Documents/New project/explainrx}"

SVG_REL="docs/metrics/crawl_daily_growth.svg"
SRC_SVG="$PROJECT/$SVG_REL"
SUMMARY_REL="docs/metrics/crawl_daily_summary.md"
SRC_SUMMARY="$PROJECT/$SUMMARY_REL"

if [[ ! -f "$SRC_SVG" ]]; then
  echo "ERROR: source plot not found: $SRC_SVG" >&2
  echo "Run scripts/crawl_progress_rollup.py first to generate it." >&2
  exit 1
fi
if [[ ! -f "$SRC_SUMMARY" ]]; then
  echo "ERROR: source summary not found: $SRC_SUMMARY" >&2
  echo "Run scripts/crawl_progress_rollup.py first to generate it." >&2
  exit 1
fi

# Clone on first run, otherwise refresh the existing clone.
if [[ -d "$CLONE_DIR/.git" ]]; then
  echo "==> Updating existing clone at $CLONE_DIR"
  git -C "$CLONE_DIR" pull --ff-only
else
  echo "==> Cloning $REPO_SSH -> $CLONE_DIR"
  git clone "$REPO_SSH" "$CLONE_DIR"
fi

echo "==> Copying plot into repo"
mkdir -p "$CLONE_DIR/$(dirname "$SVG_REL")"
cp "$SRC_SVG" "$CLONE_DIR/$SVG_REL"
cp "$SRC_SUMMARY" "$CLONE_DIR/$SUMMARY_REL"

README="$CLONE_DIR/README.md"
echo "==> Syncing README crawl progress block"
python3 - "$README" "$SVG_REL" "$SUMMARY_REL" "$SRC_SUMMARY" <<'PY'
from pathlib import Path
import re
import sys

readme_path = Path(sys.argv[1])
svg_rel = sys.argv[2]
summary_rel = sys.argv[3]
summary_path = Path(sys.argv[4])

readme = readme_path.read_text() if readme_path.exists() else ""
summary = summary_path.read_text()

summary_lines = []
for line in summary.splitlines():
    if line.startswith("# ExplainRx crawl daily summary"):
        continue
    if line.strip() == "![ExplainRx crawl growth](crawl_daily_growth.svg)":
        continue
    if line.startswith("## "):
        line = "### " + line[3:]
    summary_lines.append(line)
summary_body = "\n".join(summary_lines).strip()

block = (
    "## Crawl Progress\n\n"
    f"![ExplainRx crawl progress]({svg_rel})\n\n"
    "<!-- CRAWL_PROGRESS:START -->\n"
    f"Latest daily summary: [{summary_rel}]({summary_rel})\n\n"
    f"{summary_body}\n"
    "<!-- CRAWL_PROGRESS:END -->\n"
)

section_re = re.compile(r"\n## Crawl Progress\n.*?(?=\n## |\Z)", re.S)
if section_re.search(readme):
    readme = section_re.sub("\n" + block.rstrip() + "\n", readme, count=1)
else:
    if readme and not readme.endswith("\n"):
        readme += "\n"
    readme += "\n" + block

readme_path.write_text(readme)
PY

echo "==> Committing and pushing (if anything changed)"
git -C "$CLONE_DIR" add "$SVG_REL" "$SUMMARY_REL" README.md
if git -C "$CLONE_DIR" diff --cached --quiet; then
  echo "    Nothing changed — plot already up to date. Done."
  exit 0
fi
git -C "$CLONE_DIR" commit -m "Update crawl progress plot ($(date +%Y-%m-%d))"
git -C "$CLONE_DIR" push
echo "==> Pushed. The README plot is refreshed."
