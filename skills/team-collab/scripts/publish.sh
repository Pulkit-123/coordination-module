#!/usr/bin/env bash
# Commit and push the project's notes, surviving the case where someone else
# pushed first.
#
# Only touches the notes — never code. Code goes through a branch so nobody's
# half-finished work lands on everyone else's main.
#
# CLAUDE.md and .gitattributes are included deliberately: without the first, a
# friend who clones gets no brief and none of this works for them; without the
# second, union-merge is off and simultaneous entries get silently dropped.
set -uo pipefail

FILES=(CLAUDE.md .gitattributes CONTEXT.md JOURNAL.md IDEAS.md TASKS.md)
for j in journeys/*.md; do [ -e "$j" ] && FILES+=("$j"); done

MSG="${1:-notes: update}"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "not a git repo — skipping"; exit 0
fi

TRACKED=()
for f in "${FILES[@]}"; do [ -f "$f" ] && TRACKED+=("$f"); done
if [ ${#TRACKED[@]} -eq 0 ]; then
  echo "no notes files here"; exit 0
fi

git add -- "${TRACKED[@]}"
if git diff --cached --quiet -- "${TRACKED[@]}"; then
  echo "nothing to publish"; exit 0
fi

git commit -q -m "$MSG" -- "${TRACKED[@]}" || { echo "commit failed"; exit 1; }
echo "committed: $MSG"

if ! git remote | grep -q .; then
  echo "no remote — committed locally only"; exit 0
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)

# `merge=union` means the append-only notes never conflict — both sides survive.
# So a conflict reaching here is structural, usually two people rewriting the same
# journey, which is exactly the case a person should look at rather than have
# silently merged.
for attempt in 1 2 3 4 5 6; do
  if git push -q origin "$BRANCH" 2>/dev/null; then
    echo "pushed to origin/$BRANCH"
    exit 0
  fi
  echo "someone pushed first (attempt $attempt) — rebasing…"
  if ! git pull --rebase -q origin "$BRANCH" 2>/dev/null; then
    CONFLICTS=$(git diff --name-only --diff-filter=U | tr '\n' ' ')
    git rebase --abort 2>/dev/null
    echo
    echo "CONFLICT in: ${CONFLICTS:-unknown}"
    echo "Someone changed the same lines. Not force-pushing — your work is safe in"
    echo "the last local commit. Ask Claude Code to merge the two versions."
    exit 1
  fi
done

# A rejection that never resolves is usually not a race. For someone recently
# invited to a repo, it's an unaccepted invitation — and git's own error talks
# about permissions, which sends people looking in entirely the wrong place.
if ! git ls-remote --exit-code origin >/dev/null 2>&1; then
  echo
  echo "Can't reach the repo at all. Two likely reasons:"
  echo "  · you were invited but haven't accepted yet — check your email, or"
  echo "    look at https://github.com/notifications"
  echo "  · you're not a collaborator; ask whoever owns it to add you"
  echo
  echo "Your work is committed locally either way, so nothing is lost."
  exit 1
fi

echo "still couldn't push after 6 tries — try again shortly"
exit 1
