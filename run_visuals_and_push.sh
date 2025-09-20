#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_ROOT"

NOTEBOOK="notebooks/advanced/all_mirrors_visuals.ipynb"
MSG=${1:-"Refresh visuals"}

echo "▶︎ Pull latest"
git pull --rebase origin main || true

echo "▶︎ Execute notebook & save outputs into the file"
jupyter nbconvert \
  --to notebook \
  --inplace \
  --ExecutePreprocessor.timeout=1200 \
  --execute "$NOTEBOOK"

echo "▶︎ Stage changes"
git add "$NOTEBOOK"

# If there are changes, commit; otherwise skip
if ! git diff --cached --quiet; then
  git commit -m "$MSG"
  echo "▶︎ Push"
  git push origin main
  echo "✅ Done: pushed refreshed visuals."
else
  echo "ℹ️ No changes detected; nothing to commit."
fi

echo "📍 Repo status:"
git status -sb
