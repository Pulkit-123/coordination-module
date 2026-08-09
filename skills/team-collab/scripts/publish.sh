#!/usr/bin/env bash
# Commit and push the coordination files, surviving the race where several
# people's Claude Code push markdown at the same time.
#
# Only ever touches the coordination files — never code. Code goes through a
# branch so half-finished work can't land on everyone else's main.
set -uo pipefail

# CLAUDE.md and .gitattributes are included deliberately: without the first, friends who
# clone get no workflow brief; without the second, union-merge is off and simultaneous
# idea entries get silently dropped. Both rarely change, so committing them costs nothing.
FILES=(CLAUDE.md .gitattributes IDEAS.md CONTEXT.md JOURNAL.md TASKS.md PRIORITIES.md dashboard.html)
MSG="${1:-coordination: update ideas/tasks/priorities}"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "not a git repo — skipping publish"; exit 0
fi

TRACKED=()
for f in "${FILES[@]}"; do [ -f "$f" ] && TRACKED+=("$f"); done
[ ${#TRACKED[@]} -eq 0 ] && { echo "no coordination files found"; exit 0; }

git add -- "${TRACKED[@]}"
if git diff --cached --quiet -- "${TRACKED[@]}"; then
  echo "no coordination changes to publish"; exit 0
fi

git commit -q -m "$MSG" -- "${TRACKED[@]}" || { echo "commit failed"; exit 1; }
echo "committed: $MSG"

if ! git remote | grep -q .; then
  echo "no remote configured — committed locally only"; exit 0
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Someone else almost certainly pushed since we last pulled. Rebase rather than
# merge so the history stays readable instead of filling with merge commits.
for attempt in 1 2 3; do
  if git push -q origin "$BRANCH" 2>/dev/null; then
    echo "pushed to origin/$BRANCH"; exit 0
  fi
  echo "push rejected (attempt $attempt) — rebasing on latest…"
  if ! git pull --rebase -q origin "$BRANCH"; then
    git rebase --abort 2>/dev/null
    echo
    echo "CONFLICT: someone edited the same lines. Not force-pushing — your work is"
    echo "safe in the last local commit. Resolve by hand, or ask Claude Code to."
    exit 1
  fi
done

echo "still couldn't push after 3 tries — the repo is busy, try again shortly"
exit 1
