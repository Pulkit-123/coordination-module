#!/usr/bin/env python3
"""Track what this person has picked up, so the help can get out of the way.

Guidance that helps a novice actively *harms* someone experienced — they have to
reconcile the explanation against knowledge they already hold, which adds load
instead of removing it. That's the expertise reversal effect, and it means fading
support isn't a courtesy, it's necessary. But you can only fade what you can
measure.

Measured the way stealth assessment does it: infer competence from ordinary
activity, never by testing. The cleanest signal available here is **who raised it
first**. If the empty state gets mentioned by the person before the agent brings
it up, that's the skill showing itself. No quiz, no interruption.

Per-area rather than one overall level, because competence isn't uniform —
someone can be religious about commits and completely blind to permissions.

Deliberately slow. Habits take a median of ~66 days to become automatic (range
18–254), so a couple of good moments is not mastery, and dropping support at week
three removes it before the habit exists.

The file is plain markdown on purpose. Seeing "you now handle this without being
asked" is the one piece of genuine reflection in the whole toolkit, and it costs
nothing because the record already has to exist.

Usage:
  learning_profile.py                        show the profile
  learning_profile.py --level <area>         explicit | brief | silent
  learning_profile.py --raised <area>        agent had to bring it up
  learning_profile.py --self <area>          they got there first
"""

import datetime
import os
import re
import sys

STORE = os.path.expanduser("~/.claude/learning-profile.md")

# Small on purpose. Tracking thirty things produces noise and a file nobody reads.
AREAS = {
    "empty-states": "what the screen shows before there's any data",
    "error-handling": "what happens when something fails",
    "security": "secrets, permissions, who can see what",
    "decomposition": "breaking work into pieces that each run",
    "save-points": "committing at working states so there's a way back",
    "debugging": "a hypothesis before changing things",
    "scope": "shipping the slice instead of polishing forever",
    "users": "checking with a real person rather than assuming",
}

# Enough observations that a lucky moment doesn't read as mastery.
BRIEF_AT = 3
SILENT_AT = 6
STALE_DAYS = 120


def today():
    return datetime.date.today()


def parse():
    data = {a: {"raised": 0, "self": 0, "last": None} for a in AREAS}
    if not os.path.isfile(STORE):
        return data
    try:
        with open(STORE, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return text if False else data
    # The last column is a date or an em dash for "never". Match anything that
    # isn't a pipe and validate after — matching a date pattern here means every
    # never-seen row silently fails to parse and reads as zero, which quietly
    # discards hand edits.
    for m in re.finditer(
        r"^\|\s*([a-z-]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|([^|]*)\|", text, re.M
    ):
        area, raised, slf, last = m.groups()
        if area not in data:
            continue
        last = last.strip()
        data[area] = {
            "raised": int(raised),
            "self": int(slf),
            "last": last if re.fullmatch(r"\d{4}-\d{2}-\d{2}", last) else None,
        }
    return data


def level(rec):
    """How much to say about this area."""
    slf, raised = rec["self"], rec["raised"]

    # Explicit guidance is what novices actually need — implicit learning is
    # weakest exactly for beginners. So start here rather than staying quiet and
    # hoping they infer it.
    if slf < BRIEF_AT:
        return "explicit"

    # Skills decay, and a long gap means the habit may not have stuck. Drift back
    # one step rather than assuming what was true in March still holds.
    if rec["last"]:
        try:
            gap = (today() - datetime.date.fromisoformat(rec["last"])).days
            if gap > STALE_DAYS:
                return "brief" if slf >= SILENT_AT else "explicit"
        except ValueError:
            pass

    if slf >= SILENT_AT and slf >= raised:
        return "silent"
    return "brief"


def write(data):
    lines = [
        "# What you've picked up",
        "",
        "Maintained automatically. It exists so the help can get out of the way as",
        "things become second nature — guidance that's useful early gets annoying, and",
        "eventually counterproductive, once you already do the thing.",
        "",
        "**self** counts the times you raised something before Claude did. That's the",
        "whole measurement — there's no test.",
        "",
        "| area | prompted | self | last | how much Claude says |",
        "|---|---|---|---|---|",
    ]
    for area, desc in AREAS.items():
        r = data[area]
        lines.append(
            f"| {area} | {r['raised']} | {r['self']} | {r['last'] or '—'} | {level(r)} |"
        )
    lines += [
        "",
        "## What these mean",
        "",
    ]
    for area, desc in AREAS.items():
        lines.append(f"- **{area}** — {desc}")
    lines += [
        "",
        "Edit this freely. If Claude keeps explaining something you already know, set",
        "**self** higher. If you'd like more help somewhere, set it to 0.",
        "",
    ]
    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    with open(STORE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main():
    args = sys.argv[1:]
    data = parse()

    if not args:
        if not os.path.isfile(STORE):
            print("no profile yet — everything starts at 'explicit'")
            return 0
        with open(STORE, encoding="utf-8") as fh:
            print(fh.read())
        return 0

    flag = args[0]
    area = args[1] if len(args) > 1 else ""

    if area and area not in AREAS:
        print(f"unknown area '{area}'. known: {', '.join(AREAS)}")
        return 2

    if flag == "--level":
        print(level(data[area]))
        return 0

    if flag in ("--raised", "--self"):
        key = flag[2:]
        data[area][key] += 1
        data[area]["last"] = today().isoformat()
        write(data)
        lv = level(data[area])
        if flag == "--self":
            print(f"{area}: they got there first ({data[area]['self']}x) → {lv}")
        else:
            print(f"{area}: prompted ({data[area]['raised']}x) → {lv}")
        return 0

    print(__doc__.strip())
    return 2


if __name__ == "__main__":
    sys.exit(main())
