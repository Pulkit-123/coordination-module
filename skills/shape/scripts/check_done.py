#!/usr/bin/env python3
"""Before calling something finished, check it against what was agreed.

The classic failure this catches: build the feature, it works when you try it,
ship it, and it breaks the first time the list is empty or the request fails —
because those were written down in the plan and then never implemented.

This is a prefilter, not a verifier. It finds rules that were agreed and shows
no sign of existing in the code, plus assumptions and questions nobody came
back to. Whether a rule is genuinely met is a judgment call the model has to
make by reading the code — a keyword search cannot tell you that.

Usage: check_done.py journeys/<slug>.md [--src .]
"""

import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", "dist", "build", "target", ".next",
             "venv", ".venv", "__pycache__", "vendor", "journeys"}
CODE_EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".rs", ".go", ".rb", ".java",
            ".kt", ".swift", ".php", ".vue", ".svelte", ".html", ".css", ".sql"}

# Words too common in both prose and code to be evidence of anything.
NOISE = {
    "the", "a", "an", "and", "or", "of", "to", "for", "in", "on", "is", "are",
    "be", "with", "when", "then", "that", "this", "it", "its", "as", "at", "by",
    "from", "should", "must", "can", "will", "shows", "show", "user", "users",
    "page", "screen", "data", "value", "item", "items", "list", "new", "all",
    "one", "any", "not", "no", "yes", "if", "so", "into", "out", "up", "down",
}


def words(text):
    out = set()
    for w in re.findall(r"[a-z][a-z0-9_-]{2,}", text.lower()):
        if w in NOISE:
            continue
        # Crude stemming so "exports" in the rule matches "export" in the code.
        if len(w) > 4 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.add(w)
    return out


def section(md, name):
    m = re.search(rf"^##\s+{name}\s*$(.*?)(?=^##\s|\Z)", md, re.M | re.S)
    return m.group(1) if m else ""


def bullets(text):
    """(done, text) for each checkbox or plain bullet."""
    out = []
    for line in text.splitlines():
        m = re.match(r"\s*-\s*\[([ xX])\]\s*(.+)", line)
        if m:
            out.append((m.group(1).lower() == "x", m.group(2).strip()))
            continue
        m = re.match(r"\s*-\s+(?!\*\*)(.+)", line)
        if m and not m.group(1).startswith("<"):
            out.append((False, m.group(1).strip()))
    return [(d, t) for d, t in out if not t.startswith("<") and len(t) > 8]


def codebase_words(root):
    seen = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                       and not d.startswith(".")]
        for fn in filenames:
            if os.path.splitext(fn)[1] not in CODE_EXT:
                continue
            try:
                with open(os.path.join(dirpath, fn), encoding="utf-8",
                          errors="ignore") as fh:
                    seen |= words(fh.read())
            except OSError:
                continue
            if len(seen) > 60000:
                return seen
    return seen


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__.strip().splitlines()[-1])
        return 2
    path = args[0]
    src = args[1] if len(args) > 1 else "."

    try:
        with open(path, encoding="utf-8") as fh:
            md = fh.read()
    except OSError as e:
        print(f"can't read {path}: {e}")
        return 2

    rules = bullets(section(md, "Rules"))
    if not rules:
        print("No acceptance rules in this journey — nothing to check against.")
        return 0

    have = codebase_words(src)
    unticked = [t for done, t in rules if not done]
    ticked = len(rules) - len(unticked)

    print(f"{ticked}/{len(rules)} rules ticked off in {os.path.basename(path)}\n")

    if unticked:
        print("Still open — verify each against the code before calling it done:")
        for t in unticked:
            key = words(t)
            missing = key - have
            # Requiring *every* word to be absent is useless: almost any rule
            # shares a word or two with the code ("export", "download") while
            # the part that matters — "empty", "failed" — is nowhere. Judge by
            # proportion instead, so a rule that's mostly unrepresented shows up.
            if key and len(missing) / len(key) >= 0.7:
                print(f"  [no sign in code] {t}")
            else:
                print(f"  [check]           {t}")
        print()

    for label, name in (("Assumption never confirmed", "Assumptions"),
                        ("Question never answered", "Open questions")):
        items = bullets(section(md, name))
        open_items = [t for done, t in items if not done]
        if open_items:
            print(f"{label}:")
            for t in open_items[:6]:
                print(f"  - {t}")
            print()

    print("A keyword search can't tell whether a rule is actually met — read the")
    print("code for the ones above and say plainly which are done and which aren't.")
    return 1 if unticked else 0


if __name__ == "__main__":
    sys.exit(main())
