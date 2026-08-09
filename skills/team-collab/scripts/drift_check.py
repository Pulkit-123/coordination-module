#!/usr/bin/env python3
"""Are we still debugging carefully, or just changing things and hoping?

The documented novice pattern is not "fails to find the bug" — it's **adding new
bugs while hunting the original one**, because fixes get tried at random and pile
up unverified. Experts change one thing, check it, and revert if it didn't help.

There is nothing to inspect in an artifact here; the signal is in the shape of
the working tree. Lots of edits across lots of files with nothing committed, in
the middle of chasing a problem, means nobody can now tell which change did what
— including the one that fixed it.

Usage: drift_check.py [--files N] [--lines N]
"""

import re
import subprocess
import sys

MAX_FILES = 4
MAX_LINES = 150


def run(*args):
    try:
        return subprocess.run(args, capture_output=True, text=True,
                              timeout=15).stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def arg(flag, default):
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if len(sys.argv) > i + 1:
            try:
                return int(sys.argv[i + 1])
            except ValueError:
                pass
    return default


def main():
    if not run("git", "rev-parse", "--git-dir").strip():
        return 0

    max_files = arg("--files", MAX_FILES)
    max_lines = arg("--lines", MAX_LINES)

    stat = run("git", "diff", "HEAD", "--numstat").strip()
    if not stat:
        return 0

    files, added, removed = [], 0, 0
    for line in stat.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        a, r, path = parts
        added += int(a) if a.isdigit() else 0
        removed += int(r) if r.isdigit() else 0
        files.append(path)

    churn = added + removed
    if len(files) <= max_files and churn <= max_lines:
        return 0

    # Files touched repeatedly in one uncommitted batch is the strongest tell:
    # it usually means the same thing has been changed, reverted, changed again.
    print(f"{len(files)} files changed, {churn} lines, nothing committed yet.\n")
    print("If this is one coherent piece of work, fine — commit it and carry on.")
    print()
    print("If it's a bug hunt, this is the shape that goes wrong: changes pile up")
    print("faster than they get verified, and when it finally works nobody knows")
    print("which change did it — or which of the others broke something else.")
    print()
    print("Worth doing instead: commit what's known good, then one change at a")
    print("time, checking after each. Revert anything that didn't help rather")
    print("than leaving it in.")
    print()
    for f in files[:8]:
        print(f"  {f}")
    if len(files) > 8:
        print(f"  … and {len(files) - 8} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
