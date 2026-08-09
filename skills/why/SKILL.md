---
name: why
description: Explain the history and reasoning behind a decision, a rejected idea, or a deprioritized feature in a shared project, by tracing the coordination files (CONTEXT.md, JOURNAL.md, IDEAS.md, PRIORITIES.md) and their git history. Use this whenever someone asks why something was decided, declined, rejected, dropped, deprioritized, postponed, or changed - phrasings like "why was X rejected", "why did we choose Y over Z", "why isn't X being built", "who decided this and when", "what happened to my idea about X", "why did we drop X", "was this discussed before", "did we already decide this", or "what was the reasoning behind X". Especially useful when someone joins a project late, returns after time away, or wants to re-propose something that was previously turned down.
---

# why

Answers "why was this decided?" from the written record of a project that uses the
team-collab coordination files.

## Why this matters

In a group where several people each run their own Claude Code, the reasoning behind a
decision lives in whoever's chat window it happened in. The coordination files are the
attempt to make it shared — but people still ask "why did we say no to that?", usually
because they're about to propose it again.

Answering well does two jobs: it saves the group from re-running an old argument, and it
tells the person their idea was actually considered rather than ignored. Answering
*badly* — inventing a plausible reason — is worse than not answering, because a
fabricated rationale sounds exactly like a real one and will be repeated as fact.

## How to answer

Run the trace script from the repo root:

```bash
bash "$SKILL_DIR/scripts/trace.sh" "<the thing being asked about>"
```

It searches the current files and the git history — including text that was later edited
or deleted, which is often precisely the reasoning in question. Pass the topic, not the
whole question ("offline mode", not "why did we drop offline mode").

Then read what comes back and reconstruct the story. Look for:

- **The decision itself** — usually a Decisions entry in `CONTEXT.md`, or an entry under
  ideas the group said no to.
- **The discussion that led to it** — `JOURNAL.md`, which holds the alternatives weighed
  and who argued what. This is the part people actually want; the verdict alone rarely
  satisfies someone who disagrees with it.
- **When and by whom** — the commit log gives dates and authors even when the file itself
  doesn't say.
- **Whether it's still current** — a decision made before some other change may have been
  quietly overtaken. Say so if the reasoning rests on something that has since changed.

Answer in prose, briefly: what was decided, when, by whom, and the reasoning — then say
where you found it so they can read the original. If the reasoning came from a deleted
line, mention that it was removed later; that's usually meaningful.

## When the record is silent

Say so directly: "There's no record of why — `X` appears in IDEAS.md on 3 March but
nothing explains the decision." Then offer what the trace *does* show — who was active
around that time, what else was decided the same week — and suggest asking them.

The temptation is to fill the gap with something reasonable, because a confident answer
feels more helpful than a shrug. Resist it. A group that can't tell recorded reasoning
from reconstructed guesswork loses the ability to trust its own history, and this skill
exists precisely to be trustworthy on that point. Distinguish clearly between what is
written down and what you are inferring, and label inference as inference.

## After answering

If the person is pushing back on the decision, that's a live disagreement — offer to open
a thread in `JOURNAL.md` with their argument, or to add it to `IDEAS.md`. New information
is a legitimate reason to reverse a decision; the record exists to make reversals
deliberate rather than accidental.

If the reasoning turned out to be missing and someone then explains it from memory, offer
to write it into `CONTEXT.md` so the next person doesn't have to ask.
