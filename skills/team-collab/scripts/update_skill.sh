#!/usr/bin/env bash
# Sync the installed team-collab skill from the canonical meta-repo.
# Explicit-only: never call this from the other subcommands.
set -euo pipefail

REPO="${TEAM_COLLAB_REPO:-$HOME/Claude Code Projects/Coordination Module}"
SRC="$REPO/skills/team-collab"
DEST="$HOME/.claude/skills/team-collab"

if [ ! -d "$SRC" ]; then
  echo "error: canonical skill not found at: $SRC" >&2
  echo "set TEAM_COLLAB_REPO to your clone of the Coordination Module repo." >&2
  exit 1
fi

if git -C "$REPO" remote | grep -q .; then
  echo "pulling $REPO ..."
  git -C "$REPO" pull --ff-only || echo "warning: pull failed; using local copy as-is"
else
  echo "no git remote configured on the meta-repo — using local copy as-is"
fi

echo
echo "changes to be applied:"
if diff -rq "$DEST" "$SRC" 2>/dev/null; then
  echo "  (none — already up to date)"
else
  diff -rq "$DEST" "$SRC" 2>/dev/null | sed 's/^/  /' || true
fi

mkdir -p "$DEST"
rsync -a --delete "$SRC/" "$DEST/"
chmod +x "$DEST/scripts/"*.sh "$DEST/scripts/"*.py 2>/dev/null || true

echo
echo "installed: $DEST"
