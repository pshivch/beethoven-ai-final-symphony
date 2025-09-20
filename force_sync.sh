#!/usr/bin/env bash
set -euo pipefail

# Optional: require a message, or fall back to timestamp
MSG="${1:-Force clean sync $(date '+%Y-%m-%d %H:%M:%S')}"

echo "==> Ensuring we're in a git repo and on 'main'..."
git rev-parse --is-inside-work-tree >/dev/null
# If you're on a different branch, switch (will fail if you have uncommitted changes that conflict)
git checkout main

echo "==> Fetching latest from origin..."
git fetch --all --prune

echo "==> HARD RESET local main to origin/main (discard local commits on main)..."
git reset --hard origin/main

echo "==> Staging ALL current files (tracked & untracked)..."
git add -A

echo "==> Commit (even if there were no changes, we make a tiny sync commit)..."
git commit -m "$MSG" || echo "No content changes to commit — proceeding."

echo "==> Pushing to GitHub..."
git push -u origin main

echo "✅ Force clean sync complete."
