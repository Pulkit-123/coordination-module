#!/usr/bin/env python3
"""Leave the project in a state that's cheap to come back to.

Returning to a side project after a break costs "an hour or two" just rebuilding
context, and that reload cost is a large part of why side projects quietly die.
Experienced people leave themselves a breadcrumb without thinking about it.
Beginners don't know to, so every return starts cold.

Two halves of the same moment, which is why they're one script rather than two
separate nags: is it left in a state that runs, and is there a note saying what
was happening and what's next.

Reports what git can see. The "what's next" line has to come from whoever was
actually doing the work — that part can't be inferred, and it's the part that
matters most.

Usage:
  stopping_point.py                 what state is this in
  stopping_point.py --note "..."    record where things were left
"""

import datetime
import os
import re
import subprocess
import sys

JOURNAL = "JOURNAL.md"
MARKER = "## Where we left off"


def run(*args):
    try:
        return subprocess.run(args, capture_output=True, text=True,
                              timeout=15).stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def state():
    if not run("git", "rev-parse", "--git-dir").strip():
        return None
    dirty = [l for l in run("git", "status", "--porcelain").splitlines() if l.strip()]
    branch = run("git", "rev-parse", "--abbrev-ref", "HEAD").strip()
    last = run("git", "log", "-1", "--format=%s (%cr)").strip()
    unpushed = run("git", "log", "--oneline", "@{u}..HEAD").splitlines() \
        if run("git", "rev-parse", "--abbrev-ref", "@{u}").strip() else []
    return {"dirty": dirty, "branch": branch, "last": last, "unpushed": unpushed}


def write_note(text):
    """Keep one 'where we left off' block, replacing any previous one."""
    stamp = datetime.date.today().isoformat()
    block = f"{MARKER}\n\n_{stamp}_ — {text.strip()}\n"

    if not os.path.isfile(JOURNAL):
        with open(JOURNAL, "w", encoding="utf-8") as fh:
            fh.write(f"# Journal\n\n{block}\n")
        return

    with open(JOURNAL, encoding="utf-8") as fh:
        md = fh.read()

    if MARKER in md:
        md = re.sub(rf"{re.escape(MARKER)}\n\n.*?(?=\n## |\Z)", block, md, flags=re.S)
    else:
        # Above the log so it's the first thing seen on returning.
        anchor = "\n## Log"
        md = md.replace(anchor, f"\n{block}\n## Log", 1) if anchor in md \
            else md.rstrip() + f"\n\n{block}"

    with open(JOURNAL, "w", encoding="utf-8") as fh:
        fh.write(md)


def main():
    if "--note" in sys.argv:
        i = sys.argv.index("--note")
        if len(sys.argv) <= i + 1:
            print("give me the note text")
            return 2
        write_note(sys.argv[i + 1])
        print(f"recorded in {JOURNAL} under '{MARKER}'")
        return 0

    st = state()
    if st is None:
        print("not a git repo — nothing to check")
        return 0

    problems = []
    if st["dirty"]:
        problems.append(
            f"{len(st['dirty'])} uncommitted file(s). Tomorrow starts with working out "
            f"what these were, which is the worst possible restart."
        )
    if st["unpushed"]:
        problems.append(
            f"{len(st['unpushed'])} commit(s) not pushed. Nobody else can see them, and "
            f"they only exist on this machine."
        )

    print(f"branch {st['branch']}, last commit: {st['last'] or 'none'}\n")
    if not problems:
        print("Clean and pushed. Worth leaving a line on what's next:")
        print('  stopping_point.py --note "auth works; next is the reset email"')
        return 0

    for p in problems:
        print(f"  · {p}")
    print()
    print("Before stopping: get it back to something that runs, commit it, and leave")
    print("a line saying what's next. Coming back to a half-broken thing with no note")
    print("is the single most reliable way for a project to be quietly abandoned.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
