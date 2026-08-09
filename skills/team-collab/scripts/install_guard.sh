#!/usr/bin/env bash
# Turn the pre-ship safety check on or off.
#
# This edits ~/.claude/settings.json, which affects Claude Code in *every*
# project on this machine — work repos included. So: it backs up first, it only
# ever touches its own entry, and `--uninstall` puts things back exactly as they
# were. People get better at this over time and should be able to take the
# training wheels off without hunting through config.
#
#   install_guard.sh              turn it on
#   install_guard.sh --uninstall  turn it off
#   install_guard.sh --status     say whether it's on
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUARD="$SCRIPT_DIR/git_guard.py"
SETTINGS="$HOME/.claude/settings.json"
MODE="${1:-install}"

python3 - "$MODE" "$GUARD" "$SETTINGS" <<'PY'
import json, os, shutil, sys, datetime

mode, guard, settings = sys.argv[1], sys.argv[2], sys.argv[3]
cmd = f"python3 {guard}"

data = {}
if os.path.isfile(settings):
    try:
        with open(settings) as fh:
            data = json.load(fh) or {}
    except (json.JSONDecodeError, ValueError):
        print(f"error: {settings} isn't valid JSON — not touching it.", file=sys.stderr)
        sys.exit(1)

hooks = data.setdefault("hooks", {})
pre = hooks.setdefault("PreToolUse", [])

def is_ours(entry):
    return any("git_guard.py" in (h.get("command") or "")
               for h in entry.get("hooks", []))

installed = any(is_ours(e) for e in pre)

if mode == "--status":
    print("on" if installed else "off")
    sys.exit(0)

if mode == "--uninstall":
    if not installed:
        print("wasn't on — nothing to do")
        sys.exit(0)
    shutil.copy2(settings, settings + ".bak")
    hooks["PreToolUse"] = [e for e in pre if not is_ours(e)]
    if not hooks["PreToolUse"]:
        hooks.pop("PreToolUse")
    if not hooks:
        data.pop("hooks")
    with open(settings, "w") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    print(f"off. previous settings saved to {os.path.basename(settings)}.bak")
    print("restart Claude Code for it to take effect.")
    sys.exit(0)

if installed:
    print("already on")
    sys.exit(0)

if os.path.isfile(settings):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(settings, f"{settings}.{stamp}.bak")
    print(f"backed up existing settings to {os.path.basename(settings)}.{stamp}.bak")

os.makedirs(os.path.dirname(settings), exist_ok=True)
pre.append({
    "matcher": "Bash",
    "hooks": [{"type": "command", "command": cmd}],
})
with open(settings, "w") as fh:
    json.dump(data, fh, indent=2)
    fh.write("\n")

print("on — commits and pushes are checked for leaked keys and a few other")
print("things that can't be undone. Everything else runs untouched.")
print()
print("Turn it off any time:")
print(f"  bash {os.path.join(os.path.dirname(guard), 'install_guard.sh')} --uninstall")
print()
print("restart Claude Code for it to take effect.")
PY
