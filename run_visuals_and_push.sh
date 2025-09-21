#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing/refreshing basics (safe to re-run)"
python -m pip install --upgrade pip >/dev/null
python -m pip install jupyter nbconvert nbformat matplotlib plotly pandas numpy >/dev/null
# If present, try project deps (ignore failures)
python -m pip install -r requirements.txt >/dev/null 2>&1 || true

echo "==> Ensuring docs/ exists"
mkdir -p docs

echo "==> Executing: notebooks/advanced/all_mirrors_visuals.ipynb"
python -m jupyter nbconvert \
  --to notebook \
  --execute notebooks/advanced/all_mirrors_visuals.ipynb \
  --ExecutePreprocessor.timeout=1200 \
  --output notebooks/advanced/all_mirrors_visuals_executed.ipynb

echo "==> Exporting HTML to docs/all_mirrors_visuals.html"
python -m jupyter nbconvert \
  --to html \
  notebooks/advanced/all_mirrors_visuals_executed.ipynb \
  --output docs/all_mirrors_visuals.html

echo "==> Verifying outputs exist"
ls -lh notebooks/advanced/all_mirrors_visuals_executed.ipynb
ls -lh docs/all_mirrors_visuals.html

echo "==> Opening HTML locally (macOS)"
open docs/all_mirrors_visuals.html || true

echo "==> Commit & push"
git add notebooks/advanced/all_mirrors_visuals_executed.ipynb docs/all_mirrors_visuals.html
git commit -m "Add executed visuals (bar/line/heatmaps) + HTML export" || echo "No changes to commit."
git push origin main

echo "✅ Done: visuals executed, HTML exported, repo pushed."
