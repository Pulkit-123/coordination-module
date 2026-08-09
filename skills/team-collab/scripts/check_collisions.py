#!/usr/bin/env python3
"""Find the collisions that union-merge deliberately hides.

Keeping both sides of a simultaneous edit means nobody's work is lost — but it
also means two people can claim the same task, or record contradictory
decisions, and git will report success to everyone. Nothing surfaces the clash.

This is that missing alarm. Run it after pulling and after publishing.
"""

import os
import re
import sys
from datetime import date, datetime
from difflib import SequenceMatcher

STALE_DAYS = 10
SIMILAR = 0.72

STOP = {"the", "a", "an", "to", "for", "of", "and", "in", "on", "add", "make", "up"}


def stem(w):
    # Crude, deliberately: "notifications" and "notification" must collide, but
    # the goal is flagging candidates for a human, not linguistic accuracy.
    for suf in ("ies", "es", "s"):
        if len(w) > 4 and w.endswith(suf):
            return w[: -len(suf)] + ("y" if suf == "ies" else "")
    return w


def norm(s):
    words = re.findall(r"[a-z0-9]+", s.lower())
    return " ".join(stem(w) for w in words if w not in STOP)


def alike(a, b):
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    ta, tb = set(na.split()), set(nb.split())
    if not ta or not tb:
        return False

    # Words unique to one side. "user login" vs "user logout" share "user" but
    # differ on the word carrying the meaning, so token overlap alone says
    # "same" when they're opposites. Require the distinct words to be close too.
    only_a, only_b = ta - tb, tb - ta
    if not only_a and not only_b:
        return True
    if only_a and only_b:
        best = max(SequenceMatcher(None, x, y).ratio()
                   for x in only_a for y in only_b)
        # 'login'/'logout' score ~0.83 as strings but mean opposite things, so
        # near-miss words are treated as different, not the same.
        if best >= 0.95:
            return len(ta & tb) / min(len(ta), len(tb)) >= 0.6
        if best > 0.6:
            return False

    overlap = len(ta & tb) / min(len(ta), len(tb))
    if overlap >= 0.75 and max(len(only_a), len(only_b)) <= 1:
        return True
    return SequenceMatcher(None, na, nb).ratio() >= SIMILAR


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def parse_days(s):
    for m in re.findall(r"\d{4}-\d{2}-\d{2}", s):
        try:
            return (date.today() - datetime.strptime(m, "%Y-%m-%d").date()).days
        except ValueError:
            pass
    return None


def task_rows(md):
    """Rows from the In-progress table: (who, what, status, branch, claimed)."""
    rows = []
    in_done = False
    for line in md.splitlines():
        s = line.strip()
        if s.lower().startswith("## done"):
            in_done = True
        elif s.startswith("## "):
            in_done = False
        if in_done or not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 3:
            continue
        who, what = cells[0], cells[1]
        if not who or not what or who.lower() in ("who", "_(nobody yet)_"):
            continue
        if set(who) <= set("-: "):
            continue
        rows.append(cells)
    return rows


def check_tasks(md, out):
    rows = task_rows(md)
    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            if a[0].lower() != b[0].lower() and alike(a[1], b[1]):
                out.append(
                    f"DUPLICATE WORK: {a[0]} is on \"{a[1]}\" and {b[0]} is on \"{b[1]}\".\n"
                    f"  Two people are likely building the same thing. Agree who keeps it "
                    f"before either goes further."
                )
    for r in rows:
        status = r[2].lower() if len(r) > 2 else ""
        if "progress" not in status:
            continue
        age = parse_days(r[-1]) if len(r) > 3 else None
        if age is not None and age > STALE_DAYS:
            out.append(
                f"STALE CLAIM: {r[0]} claimed \"{r[1]}\" {age} days ago and it's still "
                f"in-progress.\n  Check whether it's abandoned — it's blocking anyone "
                f"else from picking it up."
            )


def decisions(md):
    """(topic, chose, who) per decision heading."""
    found = []
    topic = None
    chose = who = ""
    for line in md.splitlines() + ["### __end__"]:
        s = line.strip()
        if s.startswith("###"):
            if topic:
                found.append((topic, chose, who))
            head = s.lstrip("#").strip()
            head = re.sub(r"^\d{4}-\d{2}-\d{2}\s*[—-]\s*", "", head)
            topic, chose, who = head, "", ""
        elif topic:
            m = re.match(r"[-*]\s*\*\*Chose:\*\*\s*(.+)", s)
            if m:
                chose = m.group(1).strip()
            m = re.match(r"[-*]\s*\*\*By:\*\*\s*(.+)", s)
            if m:
                who = m.group(1).strip()
    return [d for d in found if d[0] and d[0] != "__end__"]


def check_decisions(md, out):
    ds = decisions(md)
    for i, a in enumerate(ds):
        for b in ds[i + 1:]:
            if alike(a[0], b[0]) and a[1] and b[1] and not alike(a[1], b[1]):
                who_a = f" ({a[2]})" if a[2] else ""
                who_b = f" ({b[2]})" if b[2] else ""
                out.append(
                    f"CONTRADICTORY DECISION on \"{a[0]}\": "
                    f"\"{a[1]}\"{who_a} vs \"{b[1]}\"{who_b}.\n"
                    f"  Both are recorded as settled, so whoever reads this next picks "
                    f"one arbitrarily. Resolve it and delete the losing entry."
                )


def headings(md):
    return [re.sub(r"\s*\(.*\)\s*$", "", l.strip().lstrip("#").strip())
            for l in md.splitlines() if l.strip().startswith("### ")]


def check_ideas(md, out):
    hs = [h for h in headings(md) if h and not h.lower().startswith("example")]
    for i, a in enumerate(hs):
        for b in hs[i + 1:]:
            if alike(a, b):
                out.append(
                    f"DUPLICATE IDEA: \"{a}\" and \"{b}\" look like the same thing.\n"
                    f"  Merge them at the next triage so they aren't ranked twice."
                )


# Pairs that pull a project in opposite directions. Two people can each propose
# something sensible and only the combination is incoherent — nobody sees it,
# because each arrived at their idea alone. Flagged as candidates for a human to
# judge, never auto-rejected: plenty of projects legitimately do both.
TENSIONS = [
    ({"offline", "local", "on-device"}, {"realtime", "sync", "live", "collaborative"}),
    ({"minimal", "simple", "lightweight", "stripped"}, {"dashboard", "analytics", "customizable", "plugin"}),
    ({"free", "opensource", "self-hosted"}, {"subscription", "paid", "billing", "premium"}),
    ({"anonymous", "nologin", "guest"}, {"account", "profile", "login", "signup"}),
    ({"native", "desktop", "app"}, {"web", "browser", "url"}),
    ({"automatic", "auto", "inferred"}, {"manual", "explicit", "configurable"}),
]


def check_tensions(md, out):
    hs = [h for h in headings(md) if h and not h.lower().startswith("example")]
    for i, a in enumerate(hs):
        wa = set(norm(a).split())
        for b in hs[i + 1:]:
            wb = set(norm(b).split())
            for left, right in TENSIONS:
                if (wa & left and wb & right) or (wa & right and wb & left):
                    out.append(
                        f"POSSIBLE TENSION: \"{a}\" and \"{b}\" may pull in opposite "
                        f"directions.\n  Two people proposed these separately, so neither "
                        f"saw the clash. Worth a decision before both get built."
                    )
                    break


def scope_lines(md):
    """The 'what this is / isn't' block, if the project defined one."""
    keep, on = [], False
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("##"):
            on = "scope" in s.lower() or "what this" in s.lower()
            continue
        if on and s and not s.startswith("<!--"):
            keep.append(s)
    return keep


def check_scope(context_md, ideas_md, tasks_md, out):
    scope = scope_lines(context_md)
    if not scope:
        out.append(
            "NO SCOPE DEFINED: CONTEXT.md has no \"Scope\" section.\n"
            "  Without one there's nothing to check new work against, so drift is "
            "invisible until someone has already built the wrong thing. Worth "
            "writing two lines on what this project is and isn't."
        )
        return
    nots = [s for s in scope if re.search(r"\bis not\b|\bnot a\b|never|out of scope|won'?t", s, re.I)]
    if not nots:
        out.append(
            "SCOPE HAS NO LIMITS: the Scope section says what the project is, but not "
            "what it isn't.\n  The 'isn't' half is what actually catches drift — "
            "\"is\" statements rarely exclude anything."
        )
        return

    # Words the project explicitly excludes, e.g. "not multi-tenant SaaS".
    excluded = set()
    for line in nots:
        tail = re.split(r"\bis not\b|\bnot a\b|\bnot\b", line, maxsplit=1, flags=re.I)
        if len(tail) > 1:
            for w in re.findall(r"[a-z][a-z-]{3,}", tail[1].lower()):
                if w not in STOP and w not in ("replacement", "app"):
                    excluded.add(stem(w))

    for src, label in ((ideas_md, "idea"), (tasks_md, "task")):
        titles = headings(src) if label == "idea" else [r[1] for r in task_rows(src)]
        for t in titles:
            hit = excluded & set(norm(t).split())
            if hit:
                out.append(
                    f"OUT OF SCOPE ({label}): \"{t}\" mentions "
                    f"{', '.join(sorted(hit))}, which the Scope section rules out.\n"
                    f"  Either it genuinely doesn't belong, or the scope has moved and "
                    f"should be rewritten — but not silently."
                )


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    out = []
    ideas = read(os.path.join(root, "IDEAS.md"))
    context = read(os.path.join(root, "CONTEXT.md"))
    tasks = read(os.path.join(root, "TASKS.md"))
    check_tasks(tasks, out)
    check_decisions(context, out)
    check_ideas(ideas, out)
    check_tensions(ideas, out)
    check_scope(context, ideas, tasks, out)

    # Same title twice is normal in a journal (threads recur); only decisions matter.
    reminder = (
        "\nThis check is lexical — it compares words. It cannot see that "
        "\"push notifications\nwhen a plan changes\" and \"alert members if the plan "
        "is updated\" are the same idea,\nor that \"team billing\" contradicts a "
        "\"not multi-tenant\" scope. Read IDEAS.md and\nthe Scope section yourself "
        "for those; a clean report here does not mean no clash."
    )

    if not out:
        print("no lexical collisions found")
        print(reminder)
        return 0

    print(f"{len(out)} thing(s) need attention:\n")
    for line in out:
        print("- " + line)
    print("\nThese are hidden by design: git keeps both sides so nobody's work is lost,")
    print("which means it never reports a clash. Raise them with the people involved.")
    print(reminder)
    return 1


if __name__ == "__main__":
    sys.exit(main())
