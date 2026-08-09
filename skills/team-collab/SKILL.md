---
name: team-collab
description: Give a project a memory so Claude Code stops forgetting it between sessions - decisions and their reasoning, dead ends already hit, and who is working on what, kept in plain markdown the next session reads automatically. Use when setting this up on a repo ("set up team", "remember things about this project", "share this project with friends", "get this repo ready for the team"), and in any repo that already contains CONTEXT.md or JOURNAL.md - at the start of a session to catch up on what changed, and during work whenever something durable is decided or discovered. Also use when someone says they will pick up a piece of work, that something is finished or blocked, floats a feature idea, settles a technical choice, reports a dead end or trap, or asks what happened, what changed, or where things stand. Match intent, not wording - people should never have to remember a command.
---

# team-collab

Gives a project a memory. The user should never have to do anything to get it.

## The actual problem

Not coordination. **Repetition.** Someone spends an hour working out why Postgres and not
SQLite, what that API does when the list is empty, why the obvious approach failed. Next
session, Claude Code knows none of it. They either explain it all again, or they don't —
and Claude confidently rebuilds the thing they rejected last week.

That happens to one person working alone, every day. When a second person joins it gets
worse, because now their chat history is private too and nothing crosses between them.

A few markdown files in the repo fix it, because every Claude Code that opens the repo
reads them automatically.

## The rule that matters most

**The user does nothing.** No commands to remember, no files to open, no page to check, no
process to follow. They talk normally and build normally; you keep the memory.

Every feature that asks something of them is a feature they won't use. A dashboard nobody
opens, a ranking command nobody runs, a file nobody edits — those were all removed for
exactly this reason. Don't add them back.

Everything the user needs to see happens **in the chat**, because that's the one surface
they actually read — and even then, only a line or two.

## At the start of a session

Silently: `git pull`, then read `CONTEXT.md`, `JOURNAL.md`, `TASKS.md`, and any
`journeys/*.md`.

Then say — in **two or three lines maximum** — only what has actually changed since they
were last here, and only if it affects them. Something like:

> Priya finished the CSV export and hit a rate limit on the API — she's noted the
> workaround. Nothing else moved.

If nothing changed, say nothing at all. Don't announce that you read the files, don't list
what's in them, and never print a status report nobody asked for. A wall of text at the
start of every session is precisely the friction this exists to avoid.

Also run this quietly and mention anything it finds, because git will not:

```bash
python3 "$SKILL_DIR/scripts/check_collisions.py"
```

It catches two people claiming the same work, contradictory decisions, and stale claims —
things that are silently kept by the merge strategy rather than flagged.

## While working: capture without being asked

When something durable comes up in ordinary conversation, write it down and mention it in
**one short line**. Don't ask permission for these — they're additive and easy to correct,
and asking each time is the friction that kills the whole thing.

| What you hear | Where it goes |
|---|---|
| A choice settled — "let's use Postgres" | `CONTEXT.md` decisions, **with the reasoning** |
| A dead end — "tried X, it breaks when Y" | `CONTEXT.md` gotchas |
| An idea floated — "would be nice if…" | `IDEAS.md`, under their name |
| Real back-and-forth about an approach | `JOURNAL.md`, including the options rejected |
| An unresolved argument | `JOURNAL.md` open threads, with both positions |

Match meaning, not phrasing. Someone describing what they're about to build is claiming it,
however they say it.

**Use judgment about what's worth keeping.** Passing thoughts during unrelated work are
noise; an unreadable record is as useless as an empty one. Keep what someone would want to
find later.

### The two things worth asking about

Claiming work and marking it done are different, because they tell *other people*
something. A wrong claim makes someone skip work that isn't happening; a wrong "done" makes
the group believe a feature exists. One short line, default obvious:

> Want me to note you're on the CSV export, so nobody doubles up?

If they're working alone — no other collaborators on the repo — don't even ask. Just note
it. There's nobody to collide with.

Never ask twice about the same thing. If they ignore it or say no, drop it for the session.
If they say stop asking, stop entirely and record silently.

## Publishing

After changing anything, publish it. An update nobody else can see is the same as no
update — and for one person, it's the backup that survives losing the machine.

```bash
bash "$SKILL_DIR/scripts/publish.sh" "note: <what changed>"
```

It handles the case where someone else pushed first, retrying and rebasing. On a genuine
conflict it stops rather than force-pushing.

Code is different: work on a branch and let the person decide when to merge. Never
auto-push code to shared `main`.

## Setting it up on a repo

Copy the templates from `assets/` into the repo, substituting `{{PROJECT_NAME}}` and
`{{DATE}}`. **Never overwrite an existing file** — someone will run this again out of
uncertainty, and losing their notes would be unrecoverable.

- `CLAUDE.md` — the brief every Claude Code auto-loads. If one already exists, append under
  a `## Project memory` heading rather than clobbering it.
- `CONTEXT.md`, `JOURNAL.md`, `IDEAS.md`, `TASKS.md`
- `.gitattributes` — **don't skip this.** It sets `merge=union` so two people writing at
  once keep both entries instead of git silently dropping one. Verified failure, not
  theoretical.

Then commit and push, and say in one line what happened. Don't walk them through the file
structure — they don't need to know it, and telling them makes it feel like homework.

## Reading the files later

Nobody opens a dashboard, so there isn't one. When someone wants to know something, they
ask in chat and you answer from the files — that's the whole interface. On GitHub, the
markdown renders natively if they ever want to look, which is enough.
