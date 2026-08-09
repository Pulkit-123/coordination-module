#!/usr/bin/env python3
"""Check a journey file for the gaps that matter, before anyone builds from it.

Two kinds of problem. Things that will visibly break — a `click` directive makes
GitHub refuse to render the whole diagram, and an oversized graph fails to lay
out. And things that are quietly incomplete — a flow with no failure branches
means nobody has thought about what goes wrong yet, which is the single most
common reason a feature ships badly.

Advisory, not a gate. A thin journey for a small feature is a reasonable choice;
the point is that it should be a choice rather than an oversight.

Usage: check_journey.py journeys/<slug>.md [more.md ...]
"""

import re
import sys

MAX_NODES = 40
PLACEHOLDER = re.compile(r"<[a-z][^>]{2,}>")

# Words that mark a branch as handling something going wrong, rather than
# another happy-path step. Matched against edge labels and node text.
TROUBLE = (
    "no", "not", "none", "empty", "error", "fail", "invalid", "denied", "reject",
    "missing", "expired", "offline", "timeout", "too large", "too many", "retry",
    "cancel", "unauthor", "forbidden", "duplicate", "conflict", "wrong", "zero",
    "unavailable", "limit", "refus", "block",
)


def mermaid_blocks(md):
    return re.findall(r"```mermaid\s*\n(.*?)```", md, re.S)


def diagram_nodes(src):
    """Node ids appearing in the diagram, however they're bracketed."""
    ids = set()
    for m in re.finditer(r"([A-Za-z_][\w-]*)\s*(?:\[|\(|\{|>)", src):
        ids.add(m.group(1))
    for m in re.finditer(r"-->\s*(?:\|[^|]*\|)?\s*([A-Za-z_][\w-]*)", src):
        ids.add(m.group(1))
    ids.discard("flowchart")
    ids.discard("graph")
    return ids


def has_trouble_branch(src):
    """Does the diagram acknowledge anything going wrong?"""
    labels = re.findall(r"\|([^|]+)\|", src)          # edge labels
    labels += re.findall(r"[\[\(\{]+([^\]\)\}]+)", src)  # node text
    joined = " ".join(labels).lower()
    return any(w in joined for w in TROUBLE)


# Where products actually die, with numbers attached. 84% of people who hit a
# blank screen with no guidance leave in that first session; 70-80% are gone
# within three days, most before anything of value has happened. Forcing an
# account before the user has seen anything work is the single most expensive
# mistake available, and past roughly seven steps conversion drops measurably.
GATE = re.compile(r"\b(sign\s?up|signup|register|create an account|log\s?in|login|"
                  r"sign\s?in|authenticate|verify your email|subscribe|payment|"
                  r"credit card|paywall)\b", re.I)
VALUE = re.compile(r"\b(see|view|browse|try|use|create|add|make|start|explore|"
                   r"result|works|preview|demo)\b", re.I)
BLANK_OK = re.compile(r"\b(empty|nothing yet|no .{0,20} yet|first one|get started|"
                      r"add your first|sample|example|placeholder|onboard)\b", re.I)


def check_onboarding(md, out):
    """Does a first-time user reach anything worthwhile before being asked for something?"""
    src = "".join(mermaid_blocks(md))
    if not src:
        return

    # id -> (text, is_decision). Decisions are branch points, not steps a user
    # performs, so they don't count toward the length of the path.
    nodes = {}
    ordered = []
    for m in re.finditer(r"([A-Za-z_][\w-]*)\s*(\(\[|\[|\{|\()\s*[\"']?(.+?)[\"']?\s*"
                         r"(?:\]\)|\]|\}|\))", src):
        nid, brack, text = m.group(1), m.group(2), m.group(3).strip()
        if nid not in nodes:
            nodes[nid] = (text, brack == "{")
            ordered.append(text)
    if len(ordered) < 3:
        return

    gate_at = next((i for i, s in enumerate(ordered) if GATE.search(s)), None)
    value_at = next((i for i, s in enumerate(ordered) if VALUE.search(s)), None)

    if gate_at is not None and (value_at is None or gate_at < value_at):
        out.append(
            f"GATE BEFORE VALUE: \"{ordered[gate_at]}\" comes before the user has seen "
            f"anything work.\n  Asking for an account, payment or verification before "
            f"delivering value is the most expensive onboarding mistake there is — most "
            f"of the people who leave do so in the first session, before anything "
            f"happened. Let them see it work first if there's any way to."
        )

    # Count only the path a user walks when things go right. Counting every node
    # would penalise a journey for handling failures well, which is precisely
    # backwards — the error branches are the part we want more of.
    trouble_words = re.compile("|".join(TROUBLE), re.I)
    off_path = {tgt for lbl, tgt in re.findall(
        r"-->\s*\|([^|]+)\|\s*([A-Za-z_][\w-]*)", src) if trouble_words.search(lbl)}
    happy = [text for nid, (text, is_decision) in nodes.items()
             if nid not in off_path
             and not is_decision
             and not trouble_words.search(text)]

    if len(happy) > 9:
        out.append(
            f"LONG PATH: about {len(happy)} steps before the user is done, not counting "
            f"the failure branches.\n  Conversion drops measurably past roughly seven, and "
            f"each extra step is another place to lose someone. Worth asking which of "
            f"these could happen later, or not at all."
        )

    if not BLANK_OK.search(md):
        out.append(
            "NO EMPTY STATE: nothing here says what a first-time user sees before there "
            "is any data.\n  84% of people who hit a blank screen with no guidance "
            "abandon in that first session — it is the highest-leverage screen in the "
            "whole flow, and the one most reliably forgotten."
        )


def section(md, name):
    m = re.search(rf"^##\s+{name}\s*$(.*?)(?=^##\s|\Z)", md, re.M | re.S)
    return m.group(1) if m else ""


def check(path):
    try:
        with open(path, encoding="utf-8") as fh:
            md = fh.read()
    except OSError as e:
        return [f"can't read {path}: {e}"], []

    problems, notes = [], []
    check_onboarding(md, problems)
    blocks = mermaid_blocks(md)

    if not blocks:
        problems.append(
            "No mermaid diagram. The picture is the thing people actually look at — "
            "without it this is just a document."
        )

    for src in blocks:
        if re.search(r"^\s*click\s", src, re.M):
            problems.append(
                "Diagram contains a `click` directive. GitHub blocks the entire diagram "
                "when it sees one — it renders as \"This content is blocked\". Remove it."
            )
        if re.search(r"^\s*journey\s*$", src, re.M):
            problems.append(
                "Diagram uses mermaid's `journey` type, which cannot branch at all. "
                "Failure and empty states can't be expressed in it. Use `flowchart TD`."
            )
        n = len(diagram_nodes(src))
        if n > MAX_NODES:
            problems.append(
                f"Diagram has ~{n} nodes (over {MAX_NODES}). Mermaid layout degrades and "
                f"often fails past this, and a journey this big is really several "
                f"journeys — split it."
            )
        elif n and not has_trouble_branch(src):
            problems.append(
                "Every path through the diagram succeeds. Nothing is empty, nothing is "
                "refused, nothing fails. That's almost never true — the missing branches "
                "are usually where the real requirements are hiding."
            )

    # Unresolved template scaffolding left behind
    stripped = re.sub(r"```mermaid.*?```", "", md, flags=re.S)
    leftovers = {m.group(0) for m in PLACEHOLDER.finditer(stripped)}
    if len(leftovers) > 3:
        problems.append(
            f"{len(leftovers)} template placeholders still unfilled "
            f"(e.g. {', '.join(sorted(leftovers)[:3])}). Delete the ones that don't apply "
            f"rather than leaving them — otherwise nobody can tell what was considered."
        )

    rules = re.findall(r"^\s*-\s*\[[ x]\]", section(md, "Rules"), re.M)
    qs = re.findall(r"^\s*-\s*\[[ x]\]", section(md, "Open questions"), re.M)

    if not rules:
        problems.append("No acceptance rules yet — nothing says when this is finished.")
    if len(qs) > len(rules) and qs:
        notes.append(
            f"{len(qs)} open questions against {len(rules)} rules. More unknowns than "
            f"decisions usually means this isn't understood well enough to build yet."
        )
    if len(rules) > 12:
        notes.append(
            f"{len(rules)} rules is a lot for one journey — worth splitting into "
            f"separate features."
        )
    if not section(md, "First slice").strip():
        notes.append("No first slice identified — nothing says what to build first.")

    return problems, notes


def main():
    paths = sys.argv[1:]
    if not paths:
        print(__doc__.strip().splitlines()[-1])
        return 2

    worst = 0
    for path in paths:
        problems, notes = check(path)
        print(f"\n=== {path} ===")
        if not problems and not notes:
            print("looks complete")
            continue
        for p in problems:
            print(f"  [gap]  {p}")
        for n in notes:
            print(f"  [note] {n}")
        worst = max(worst, 1 if problems else 0)

    print("\nAdvisory only — a deliberately thin journey is fine. An accidental one isn't.")
    return worst


if __name__ == "__main__":
    sys.exit(main())
