#!/usr/bin/env python3
"""Have we hit this before? Search problems already solved, in any project.

A gotcha recorded in one repo is invisible from every other repo, so people
solve the same library quirk three times across three projects. This searches a
single global list the user has built up deliberately — it never scans other
repositories, because reading someone's unrelated projects to answer a question
they didn't ask is not a trade worth making.

Usage:
  recall.py "error text or symptom"     search
  recall.py --list                      show everything known
  recall.py --add                       print the format to append
"""

import os
import re
import sys
from difflib import SequenceMatcher

STORE = os.path.expanduser("~/.claude/known-issues.md")

# Words that appear in almost every error and would match everything.
NOISE = {
    "error", "exception", "failed", "failure", "cannot", "could", "unable",
    "invalid", "unexpected", "the", "and", "for", "with", "from", "this", "that",
    "was", "not", "you", "your", "when", "while", "trying", "there", "have",
    "line", "file", "call", "called", "returned", "return", "none", "null",
    "true", "false", "warning", "traceback", "most", "recent", "last",
}


def tokens(text):
    out = set()
    for w in re.findall(r"[A-Za-z_][A-Za-z0-9_.-]{2,}", text.lower()):
        w = w.strip("._-")
        if len(w) > 2 and w not in NOISE:
            out.add(w)
    return out


def parse(md):
    """Entries look like:  ### title (project, date) / **Looks like:** / **Fix:**"""
    entries = []
    for block in re.split(r"\n(?=###\s)", md):
        if not block.strip().startswith("###"):
            continue
        title = block.split("\n", 1)[0].lstrip("#").strip()
        looks = re.search(r"\*\*Looks like:\*\*\s*(.+?)(?=\n\*\*|\n###|\Z)", block, re.S)
        fix = re.search(r"\*\*Fix:\*\*\s*(.+?)(?=\n\*\*|\n###|\Z)", block, re.S)
        entries.append({
            "title": title,
            "looks": (looks.group(1).strip() if looks else ""),
            "fix": (fix.group(1).strip() if fix else ""),
        })
    return entries


def score(query_tokens, entry):
    hay = tokens(entry["title"] + " " + entry["looks"])
    if not hay or not query_tokens:
        return 0.0
    shared = query_tokens & hay
    if not shared:
        # Fall back to fuzzy string similarity for reworded symptoms.
        return SequenceMatcher(None, " ".join(sorted(query_tokens)),
                               " ".join(sorted(hay))).ratio() * 0.5
    # Distinctive shared words matter more than common ones. A library name
    # appearing in both is far stronger evidence than "request".
    weight = sum(1.5 if len(w) > 7 else 1.0 for w in shared)
    return weight / (len(query_tokens) ** 0.5)


TEMPLATE = """### <short title>  (<project>, YYYY-MM-DD)
**Looks like:** <the error text or symptom, in the words it actually appears in>
**Fix:** <what actually worked>
"""


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return 2

    if sys.argv[1] == "--add":
        print(f"Append to {STORE} under '## Known issues':\n\n{TEMPLATE}")
        return 0

    if not os.path.isfile(STORE):
        print(f"nothing recorded yet ({STORE} does not exist)")
        return 0

    with open(STORE, encoding="utf-8") as fh:
        entries = parse(fh.read())

    if not entries:
        print("nothing recorded yet")
        return 0

    if sys.argv[1] == "--list":
        for e in entries:
            print(f"- {e['title']}")
        return 0

    q = tokens(" ".join(sys.argv[1:]))
    hits = sorted(((score(q, e), e) for e in entries), key=lambda x: -x[0])
    hits = [(s, e) for s, e in hits if s >= 0.55][:3]

    if not hits:
        print("no match — this looks new")
        return 1

    print("Seen before:\n")
    for s, e in hits:
        print(f"  {e['title']}")
        if e["looks"]:
            print(f"    looks like: {e['looks'][:160]}")
        if e["fix"]:
            print(f"    fix: {e['fix'][:300]}")
        print()
    print("Check it's actually the same thing before applying — a similar message")
    print("can have a different cause.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
