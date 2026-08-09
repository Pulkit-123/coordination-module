#!/usr/bin/env python3
"""Turn the journey's happy path into a walkthrough to do by hand.

The standard pre-release check is five to ten manual steps — open it, do the one
main thing, confirm nothing crashed. That's exactly right for someone with no
test suite, and it's what catches the embarrassing breakage before anyone else
sees it.

Beginners tend to do one of two things: nothing at all, or conclude they need a
whole testing setup before they're allowed to check anything. This is the middle
that actually gets done.

Derived rather than written, because the happy path is already drawn in the
journey. Failure branches are listed separately and briefly — worth a look if
they're cheap to trigger, not worth blocking on.

Usage: smoke_test.py journeys/<slug>.md
"""

import os
import re
import sys

MAX_STEPS = 10

TROUBLE = re.compile(
    r"\b(no|not|none|empty|error|fail|invalid|denied|reject|missing|expired|"
    r"offline|timeout|too large|too many|retry|cancel|unauthor|forbidden|"
    r"duplicate|conflict|wrong|zero|unavailable|limit|refus|block|miss|spam|stuck|broke|break|lost|skip|abandon|ignore|pending)\b", re.I)


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip().splitlines()[-1])
        return 2
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as fh:
            md = fh.read()
    except OSError as e:
        print(f"can't read {path}: {e}")
        return 2

    m = re.search(r"```mermaid\s*\n(.*?)```", md, re.S)
    if not m:
        print("No diagram in this journey — nothing to walk through.")
        return 0
    src = m.group(1)

    nodes, order = {}, []
    for n in re.finditer(r"([A-Za-z_][\w-]*)\s*(\(\[|\[|\{|\()\s*[\"']?(.+?)[\"']?\s*"
                         r"(?:\]\)|\]|\}|\))", src):
        nid, brack, text = n.group(1), n.group(2), n.group(3).strip()
        if nid not in nodes:
            nodes[nid] = (text, brack == "{")
            order.append(nid)

    off_path = {tgt for lbl, tgt in re.findall(
        r"-->\s*\|([^|]+)\|\s*([A-Za-z_][\w-]*)", src) if TROUBLE.search(lbl)}

    happy, bad = [], []
    for nid in order:
        text, is_decision = nodes[nid]
        if is_decision:
            continue
        if nid in off_path or TROUBLE.search(text):
            bad.append(text)
        else:
            happy.append(text)

    title = re.search(r"^#\s+(.*)", md, re.M)
    print(f"Walk this before anyone else sees it — {title.group(1) if title else path}\n")

    if not happy:
        print("Couldn't pick out a happy path from the diagram.")
        return 0

    for i, step in enumerate(happy[:MAX_STEPS], 1):
        print(f"  {i}. {step}")
    if len(happy) > MAX_STEPS:
        print(f"     (+{len(happy) - MAX_STEPS} more — if the list is this long, the")
        print(f"      feature is probably several features)")

    print("\n  Then: nothing in the console, and a refresh doesn't lose anything.")

    if bad:
        print("\nIf they're quick to trigger, these are where it usually breaks:")
        for text in bad[:5]:
            print(f"  · {text}")

    print("\nTakes two minutes and catches the obvious breakage. Not a substitute for")
    print("tests once this matters to someone other than you.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
