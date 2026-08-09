#!/usr/bin/env bash
# One command instead of two, and an unmissable restart instruction.
#
# The onboarding flow was ten steps before someone was contributing, which is
# past the point people drop out. This removes one, and turns the riskiest step
# into something that can be checked rather than failing in silence.
#
# That step is the restart: Claude Code reads its skill list once at startup, so
# installing without restarting leaves everything invisible — no error, nothing
# happens, no way to tell why. It cost real confusion during development.
set -uo pipefail

REPO="https://github.com/Pulkit-123/coordination-module.git"
DEST="${COORDINATION_MODULE_DIR:-$HOME/coordination-module}"

command -v git >/dev/null 2>&1 || { echo "git is required and isn't installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || {
  echo "python3 is required and isn't installed."
  echo "On a Mac: xcode-select --install"
  exit 1
}

if [ -d "$DEST/.git" ]; then
  echo "Updating $DEST …"
  git -C "$DEST" pull --ff-only --quiet || echo "  (couldn't pull; using what's there)"
else
  echo "Getting it from GitHub …"
  git clone --quiet "$REPO" "$DEST" || { echo "clone failed"; exit 1; }
fi

# Point it at the clone we just made. Without this it falls back to guessing
# likely locations and can pick a different, stale copy.
TEAM_COLLAB_REPO="$DEST" bash "$DEST/skills/team-collab/scripts/update_skill.sh" || exit 1

cat <<'DONE'

────────────────────────────────────────────────────────────
  ONE MORE STEP, AND IT WON'T WORK WITHOUT IT

  Quit Claude Code completely and open it again.

  It only looks for new skills when it starts. Skip this and
  nothing works — and there's no error message to tell you
  why, which is the confusing part.
────────────────────────────────────────────────────────────

  To check it worked, open any project after restarting and type:

      what can you remember about this project

  If it talks about notes or setting the project up, you're done.
  If it has no idea what you mean, you didn't restart.

DONE
