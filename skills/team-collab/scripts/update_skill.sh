#!/usr/bin/env bash
# Sync the installed skills from the canonical meta-repo.
# Explicit-only: never call this from the other subcommands. A tool that
# silently rewrites itself mid-task is impossible to reason about.
set -uo pipefail

REPO="${TEAM_COLLAB_REPO:-$HOME/Claude Code Projects/Coordination Module}"
SRC="$REPO/skills"
DEST="$HOME/.claude/skills"

if [ ! -d "$SRC" ]; then
  echo "error: no skills/ directory in the meta-repo at: $REPO" >&2
  echo "set TEAM_COLLAB_REPO to your clone of the Coordination Module repo." >&2
  exit 1
fi

if git -C "$REPO" remote 2>/dev/null | grep -q .; then
  echo "pulling $REPO ..."
  git -C "$REPO" pull --ff-only || echo "warning: pull failed; using local copy as-is"
else
  echo "no git remote on the meta-repo — using local copy as-is"
fi

echo
for skill_path in "$SRC"/*/; do
  [ -d "$skill_path" ] || continue
  name=$(basename "$skill_path")
  target="$DEST/$name"

  if [ -d "$target" ] && diff -rq "$target" "$skill_path" >/dev/null 2>&1; then
    echo "$name: already up to date"
    continue
  fi

  if [ -d "$target" ]; then
    echo "$name: updating"
    diff -rq "$target" "$skill_path" 2>/dev/null | sed 's/^/    /'
  else
    echo "$name: installing (new)"
  fi

  mkdir -p "$target"
  rsync -a --delete "$skill_path" "$target/"
  chmod +x "$target"/scripts/*.sh "$target"/scripts/*.py 2>/dev/null || true
done

echo
echo "installed into: $DEST"
