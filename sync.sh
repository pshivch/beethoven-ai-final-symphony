#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./sync.sh [normal|force|nuclear] ["Commit message"]
# Examples:
#   ./sync.sh
#   ./sync.sh normal "Update notebooks"
#   ./sync.sh force
#   ./sync.sh nuclear "Hard reset to remote"

MODE="${1:-normal}"
MSG="${2:-"Sync update"}"

branch() { git rev-parse --abbrev-ref HEAD; }
assert_main() {
  local b; b="$(branch)"
  if [[ "$b" != "main" ]]; then
    echo "Switching to 'main' (was '$b')"
    git checkout main || git checkout -b main
  fi
}

ensure_remote() {
  git remote -v | grep -q '^origin' || {
    echo "No 'origin' remote found. Set it with:"
    echo "  git remote add origin https://github.com/pshivch/beethoven-ai-final-symphony.git"
    exit 1
  }
}

normal_sync() {
  echo "== Normal sync =="
  git fetch origin
  git pull --rebase origin main || true
  git add -A
  # Only commit if there’s a diff
  if ! git diff --cached --quiet; then
    git commit -m "$MSG"
  else
    echo "No staged changes; skipping commit."
  fi
  git push origin main
  echo "✅ Normal sync complete."
}

force_sync() {
  echo "== FORCE sync (keeps local edits via stash) =="
  local had_dirty=0
  if ! git diff --quiet || ! git diff --cached --quiet; then
    had_dirty=1
    echo "Stashing local changes…"
    git stash push -u -m "sync.sh auto-stash $(date +%F-%T)" || true
  fi
  git fetch origin
  git reset --hard origin/main
  if [[ "$had_dirty" -eq 1 ]]; then
    echo "Reapplying stashed changes…"
    git stash pop || true
    git add -A
    if ! git diff --cached --quiet; then
      git commit -m "$MSG"
    fi
  fi
  git push origin main
  echo "✅ FORCE sync complete."
}

nuclear_sync() {
  echo "== NUCLEAR sync (DESTROYS local changes not on remote) =="
  read -p "Type 'NUKE' to continue: " confirm
  [[ "$confirm" == "NUKE" ]] || { echo "Aborted."; exit 1; }

  git fetch origin
  git reset --hard origin/main
  git clean -fdx
  git pull --rebase origin main || true
  git push origin main
  echo "✅ Nuclear sync complete."
}

main() {
  assert_main
  ensure_remote

  case "$MODE" in
    normal)  normal_sync ;;
    force)   force_sync  ;;
    nuclear) nuclear_sync ;;
    *) echo "Unknown mode: $MODE. Use: normal | force | nuclear"; exit 2 ;;
  esac

  echo
  echo "Repo status:"
  git status -sb
}

main "$@"
