#!/usr/bin/env bash
# Commit and push the coordination files, surviving the race where several
# people's Claude Code push at the same time.
#
# Only ever touches the coordination files — never code. Code goes through a
# branch so half-finished work can't land on everyone else's main.
#
# CLAUDE.md and .gitattributes are included deliberately: without the first,
# friends who clone get no workflow brief; without the second, union-merge is off
# and simultaneous idea entries get silently dropped.
set -uo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Hand-written files: a conflict here is real and needs a human.
SOURCE_FILES=(CLAUDE.md .gitattributes IDEAS.md CONTEXT.md JOURNAL.md TASKS.md)
# Regenerated from the files above. A conflict here is meaningless — rebuilding
# always produces the correct result, so never make a person resolve one. This
# matters more than it sounds: leaving these to git blocked everyone but the
# first pusher, because generated files differ on every machine.
GENERATED_FILES=(PRIORITIES.md dashboard.html)

MSG="${1:-coordination: update}"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "not a git repo — skipping publish"; exit 0
fi

regen_dashboard() {
  [ -f "$SKILL_DIR/scripts/build_dashboard.py" ] || return 0
  python3 "$SKILL_DIR/scripts/build_dashboard.py" --dir . >/dev/null 2>&1 || true
}

TRACKED=()
for f in "${SOURCE_FILES[@]}" "${GENERATED_FILES[@]}"; do
  [ -f "$f" ] && TRACKED+=("$f")
done
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

is_generated() {
  local f="$1"
  for g in "${GENERATED_FILES[@]}"; do [ "$f" = "$g" ] && return 0; done
  return 1
}

# Resolve a rebase that stopped on conflicts. Generated files are rebuilt rather
# than merged; anything else is a genuine disagreement and stops the run.
resolve_rebase() {
  while true; do
    local conflicts unresolved=""
    conflicts=$(git diff --name-only --diff-filter=U)
    [ -z "$conflicts" ] && return 0

    while IFS= read -r f; do
      [ -z "$f" ] && continue
      if is_generated "$f"; then
        git checkout --ours -- "$f" 2>/dev/null || true
        git add -- "$f" 2>/dev/null || true
      else
        unresolved="$unresolved $f"
      fi
    done <<< "$conflicts"

    if [ -n "$unresolved" ]; then
      echo "  genuine conflict in:$unresolved"
      return 1
    fi

    # Only skip when the commit genuinely has nothing left in it (our change was
    # already applied upstream). Skipping a non-empty commit silently deletes
    # someone's work — verified the hard way, so check before skipping.
    if git diff --cached --quiet HEAD 2>/dev/null; then
      git rebase --skip >/dev/null 2>&1 || return 1
    elif ! GIT_EDITOR=true git rebase --continue >/dev/null 2>&1; then
      echo "  rebase could not continue"
      return 1
    fi
  done
}

# With four people active, several rounds of "someone pushed first" is normal.
for attempt in 1 2 3 4 5 6; do
  if git push -q origin "$BRANCH" 2>/dev/null; then
    echo "pushed to origin/$BRANCH"
    exit 0
  fi
  echo "push rejected (attempt $attempt) — rebasing on latest…"

  if ! git pull --rebase -q origin "$BRANCH" 2>/dev/null; then
    if ! resolve_rebase; then
      git rebase --abort 2>/dev/null
      echo
      echo "CONFLICT: someone edited the same lines you did. Not force-pushing —"
      echo "your work is safe in the last local commit. Resolve by hand, or ask"
      echo "Claude Code to merge the two versions."
      exit 1
    fi
  fi

  # Merged sources may differ from what we generated before rebasing.
  regen_dashboard
  git add -- "${GENERATED_FILES[@]}" 2>/dev/null || true
  git diff --cached --quiet || git commit -q --amend --no-edit
done

echo "still couldn't push after 6 tries — the repo is unusually busy, try again shortly"
exit 1
