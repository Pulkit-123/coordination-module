#!/usr/bin/env python3
"""Hook body: run the safety check just before a commit or push happens.

Claude Code calls this before every Bash command. It ignores everything except
git commit and git push, because that is the last moment a leaked credential can
still be stopped — after a push, rotating the key is the only real fix.

Exit 0 lets the command through. Exit 2 blocks it and shows the reason.

Blocking is reserved for the unrecoverable cases. Everything else is printed as
a note and the command proceeds, because a guard that interrupts often is a
guard people disable.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "safety_check.py")

# `git commit` / `git push`, allowing for flags and paths in between.
GIT_SHIP = re.compile(r"\bgit\s+(?:-[^\s]+\s+)*(commit|push)\b")


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    if payload.get("tool_name") != "Bash":
        return 0
    command = (payload.get("tool_input") or {}).get("command", "")
    if not GIT_SHIP.search(command):
        return 0

    # Never let a broken guard block someone's work.
    if not os.path.isfile(CHECK):
        return 0
    try:
        r = subprocess.run([sys.executable, CHECK],
                           capture_output=True, text=True, timeout=25)
    except (OSError, subprocess.SubprocessError):
        return 0

    out = (r.stdout or "").strip()
    if not out:
        return 0

    if r.returncode == 2:
        print(
            "Blocked this commit/push — something here can't be undone once it "
            "ships:\n\n" + out +
            "\nFix it, or tell the user to run the command themselves if they "
            "genuinely want it anyway.",
            file=sys.stderr,
        )
        return 2

    print(out, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
