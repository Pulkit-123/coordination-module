#!/usr/bin/env python3
"""Turn a journey's steps into the handful of events worth tracking.

Analytics gets skipped for a specific reason, not laziness: wiring it up takes a
week when the build took a day, so it gets cut — and the app ships with no
behavioural data and a vague feeling that nobody is sticking around.

The way out is that the journey already *is* the funnel. The steps someone drew
are exactly the points worth measuring, so the events can be derived rather than
designed, and dropped in during the build that was happening anyway. Cost to the
person: nothing.

Keep it to a handful. Tracking everything produces a dashboard nobody reads,
which is the same failure as tracking nothing but more work.

Usage: journey_events.py journeys/<slug>.md
"""

import os
import re
import sys

MAX_EVENTS = 8


def mermaid(md):
    m = re.search(r"```mermaid\s*\n(.*?)```", md, re.S)
    return m.group(1) if m else ""


# Event names get typed, grepped and read on a chart, so they have to be short.
# Dropping filler words keeps the part that identifies the step.
FILLER = {"a", "an", "the", "to", "of", "for", "on", "in", "and", "or", "it",
          "is", "are", "they", "them", "their", "i", "we", "you", "my", "our",
          "this", "that", "with", "from", "into", "onto", "at", "as", "be",
          "do", "does", "did", "then", "so", "if", "no", "not", "yet"}


def slug(text, words=3):
    parts = [w for w in re.findall(r"[a-z0-9]+", text.lower())
             if w not in FILLER]
    return "_".join(parts[:words]) or "step"


def nodes(src):
    """(id, label, kind) in the order they appear."""
    out, seen = [], set()
    pattern = re.compile(
        r"([A-Za-z_][\w-]*)\s*(\(\[|\[\[|\[|\{|\(\(|\()\s*[\"']?(.+?)[\"']?\s*"
        r"(\]\)|\]\]|\]|\}|\)\)|\))"
    )
    for m in pattern.finditer(src):
        nid, open_b, label, _ = m.group(1), m.group(2), m.group(3), m.group(4)
        if nid in seen:
            continue
        seen.add(nid)
        kind = ("terminal" if open_b == "([" else
                "decision" if open_b == "{" else "step")
        out.append((nid, label.strip(), kind))
    return out


def edge_labels(src):
    """Which node ids are reached by a labelled (branch) edge."""
    reached = {}
    for m in re.finditer(r"-->\s*\|([^|]+)\|\s*([A-Za-z_][\w-]*)", src):
        reached.setdefault(m.group(2), m.group(1).strip())
    return reached


BAD = re.compile(r"\b(no|not|none|empty|error|fail|invalid|denied|reject|expired|"
                 r"offline|timeout|too\s+large|too\s+many|cancel|unauthor|forbidden|"
                 r"conflict|wrong|zero|unavailable|limit|block|refus)\b", re.I)


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

    src = mermaid(md)
    if not src:
        print("No diagram in this journey — nothing to derive events from.")
        return 0

    ns = nodes(src)
    branch = edge_labels(src)
    if not ns:
        print("Couldn't read any steps out of the diagram.")
        return 0

    title = re.search(r"^#\s+(.*)", md, re.M)
    feature = slug(title.group(1) if title else os.path.basename(path)[:-3], words=2)

    started, finished, dropped = None, None, []
    steps = []
    for nid, label, kind in ns:
        reached_by = branch.get(nid, "")
        is_bad = bool(BAD.search(label) or BAD.search(reached_by))
        if kind == "terminal" and started is None:
            started = label
        elif kind == "terminal":
            finished = label
        elif is_bad:
            dropped.append(label)
        elif kind == "step":
            steps.append(label)

    print(f"Events for {os.path.basename(path)} — add these while building, not after.\n")
    print("The funnel (did they get through?):")
    if started:
        print(f"  {feature}_started{' ' * 19}— {started}")
    for label in steps[:MAX_EVENTS - 2]:
        print(f"  {feature}_{slug(label):<26} — {label}")
    if finished:
        print(f"  {feature}_completed{' ' * 17}— {finished}")

    if dropped:
        print("\nWhere it goes wrong (this is the half people forget, and it's the")
        print("half that tells you *why* the funnel leaks):")
        for label in dropped[:5]:
            print(f"  {feature}_{slug(label):<26} — {label}")

    print("\nOne line each, at the point the thing actually happens:")
    print(f'  track("{feature}_started")')
    print("\nWhatever the project already uses is fine — PostHog, Plausible, or a")
    print("row in your own database. The tool matters far less than having any")
    print("answer at all two weeks from now.")
    print("\nDon't add more than these. A long event list becomes a dashboard")
    print("nobody opens, which is the same as no data plus extra work.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
