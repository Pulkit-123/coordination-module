#!/usr/bin/env bash
# Gather every trace of a topic across the coordination files and their history.
#
# The current files show what the record says now. Git shows what it said before —
# including entries someone later edited or deleted, which is often exactly the
# reasoning being asked about. Both matter, so collect both.
#
# Usage: trace.sh "<search terms>"
set -uo pipefail

Q="${1:-}"
[ -z "$Q" ] && { echo "usage: trace.sh \"<what to look for>\"" >&2; exit 2; }

FILES=(CONTEXT.md JOURNAL.md IDEAS.md PRIORITIES.md TASKS.md)
PRESENT=()
for f in "${FILES[@]}"; do [ -f "$f" ] && PRESENT+=("$f"); done

if [ ${#PRESENT[@]} -eq 0 ]; then
  echo "No coordination files here. Is this the right repo?" >&2
  exit 1
fi

# Search each significant word separately: the phrasing in the question rarely
# matches the phrasing in the record.
TERMS=$(echo "$Q" | tr 'A-Z' 'a-z' | tr -cs 'a-z0-9' '\n' \
  | grep -vE '^(the|a|an|to|for|of|and|in|on|is|was|why|we|our|did|do|not|it|that|this|about|with)$' \
  | grep -E '.{3,}' | head -8)
[ -z "$TERMS" ] && TERMS="$Q"
PATTERN=$(echo "$TERMS" | paste -sd'|' -)

echo "=============================================================="
echo "SEARCH TERMS: $(echo "$TERMS" | tr '\n' ' ')"
echo "=============================================================="

echo
echo "########## 1. CURRENT RECORD ##########"
echo "(what the files say right now — with 6 lines of context each)"
for f in "${PRESENT[@]}"; do
  hits=$(grep -inE -A6 -B2 "$PATTERN" "$f" 2>/dev/null)
  if [ -n "$hits" ]; then
    echo
    echo "----- $f -----"
    echo "$hits" | head -80
  fi
done

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo
  echo "(not a git repo — no history available)"
  exit 0
fi

echo
echo "########## 2. WHEN IT CHANGED ##########"
echo "(commits that added or removed these words — who, when, and the message)"
git log --format='%h  %ad  %an  %s' --date=short \
  --pickaxe-regex -S"$PATTERN" -- "${PRESENT[@]}" 2>/dev/null | head -25 \
  || echo "(none)"

echo
echo "########## 3. WHAT THOSE COMMITS ACTUALLY CHANGED ##########"
echo "(includes text since edited or deleted — often the reasoning being asked about)"
for sha in $(git log --format='%h' --pickaxe-regex -S"$PATTERN" -- "${PRESENT[@]}" 2>/dev/null | head -6); do
  echo
  echo "----- commit $sha -----"
  git show --format='%ad  %an  |  %s' --date=short "$sha" -- "${PRESENT[@]}" 2>/dev/null \
    | grep -E '^[+-]|^[0-9]{4}-|^\s*$' | grep -vE '^[+-]{3}' | head -30
done

echo
echo "########## 4. DELETED LINES MENTIONING IT ##########"
echo "(reasoning that was removed rather than amended)"
git log -p --format='%h %ad %an' --date=short -- "${PRESENT[@]}" 2>/dev/null \
  | grep -iE "^-.*($PATTERN)" | grep -vE '^---' | sort -u | head -20 \
  || echo "(none)"

echo
echo "=============================================================="
echo "If sections 1-4 are all empty, the reasoning was never written down."
echo "Say that plainly rather than inferring a plausible-sounding rationale."
echo "=============================================================="
