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

### Ideas raised on GitHub

Markdown is a fine list but a poor conversation — you can't reply to one line of a file,
there are no notifications, and nobody can join in from a phone. GitHub Issues gives all
three for free, so ideas legitimately arrive there too.

While you're already pulling, fold them in — **no command, nobody has to remember this**:

```bash
gh issue list --label idea --state all --limit 100 \
  --json number,title,body,author,state,reactionGroups 2>/dev/null
```

Add anything not already in `IDEAS.md`, matching on issue number so re-running is safe, and
keep `- **Issue:** #<n>` on the entry so the discussion stays one click away. If `gh` isn't
installed or there's no GitHub remote, skip it silently — never make this a setup step.

Closed issues are already-decided; treat them as such rather than resurfacing them.

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

## Before anything ships: the things that can't be undone

Most mistakes are fixable. A few are not, and those are the ones that end up in the news.
Research on AI-built apps is blunt about this: **45–62% ship with vulnerabilities**, and
**63% of the people building this way have no coding background** — so they cannot review
what they're shipping, and the checks an experienced developer does by reflex never happen.

Run this before a commit or push:

```bash
python3 "$SKILL_DIR/scripts/safety_check.py"
```

It is deliberately narrow — a real credential about to be committed, a `.env` tracked by
git, Supabase tables with row-level security never enabled, a migration that drops or
truncates without a filter, an auth check that returns true unconditionally. Nothing else.
A checker that cries wolf gets ignored, and then the real warning is ignored too.

**Exit 2 means stop.** A pushed credential is public permanently — deleting the commit does
not help, only rotating the key does. Say that plainly rather than softening it.

### Making it automatic

The check only helps if it always runs, which means not depending on anyone remembering:

```bash
bash "$SKILL_DIR/scripts/install_guard.sh"
```

That adds a hook so every commit and push is checked. Offer it once, when setting a project
up, and explain both halves honestly: it changes Claude Code's behaviour in **every**
project on the machine, and it comes off cleanly with `--uninstall` — settings are backed
up first and nothing else in them is touched. People get better at this over time and
should be able to remove the training wheels without hunting through config.

If they'd rather not, don't push it. Run the check manually before pushing instead.

## Saying what the code can now do

Someone who can't read code can't review a diff — so the review never happens. The fix
isn't teaching them to read diffs; it's describing the change in terms they can judge.

```bash
python3 "$SKILL_DIR/scripts/what_changed.py"
```

It surfaces the parts that change *what the software can do*: who can get in, what leaves
the machine, what gets stored or deleted, money, who can be contacted, what runs on its own.

Then turn that into one sentence they could disagree with:

> This now lets anyone with the link read every entry, including other people's.

not:

> Added a GET /entries route with no auth middleware.

The test is whether someone with no coding background could push back on your sentence. If
they couldn't, it's the wrong sentence. Skip it entirely for refactors and internal
changes — the script stays quiet on those, and so should you.

## Decisions that are hard to undo

Some choices are cheap to change later and some are near-permanent — and a beginner has no
way to tell them apart. That's not a knowledge gap you can close by explaining; it's one
you close by flagging it at the moment it matters.

Hard to undo once there's real data or real users: the data model, whether accounts exist
at all, single-user vs shared, whether anything is real-time, where data is hosted, and any
public URL or API other people start depending on.

Easy to change: framework, styling, layout, wording, hosting provider, most library
choices.

When one of the first kind comes up, say so in one line and then let them decide:

> Worth thirty seconds on this one — whether entries belong to a person or a group is
> painful to change once people have data. Everything else here we can swap later.

Never turn this into a gate. Flag it, record the reasoning in `CONTEXT.md`, move on.

## When something breaks: check whether they've solved it before

This is the moment the tool is worth the most, because it's the moment they're stuck and
will actually read what you say. **Whenever an error or a confusing failure comes up**, run
this before you start debugging:

```bash
python3 "$SKILL_DIR/scripts/recall.py" "<the error text or symptom>"
```

It searches a global list of problems they've already hit — including ones from completely
different projects, which is where this pays off. Beginners don't repeat mistakes within a
project so much as across every project they build, because each repo's notes are trapped
in that repo.

If it matches, say so in a line and check whether it really is the same cause before
applying the old fix — a similar message often has a different reason.

### Adding to it

When you record a gotcha in `CONTEXT.md`, ask one question: **is this about the project, or
about the tool?**

- *"our sync endpoint returns 200 on failure"* → project-specific, stays in `CONTEXT.md`
- *"Vercel builds break on case-mismatched imports because Linux is case-sensitive"* →
  happens anywhere, so also append it to `~/.claude/known-issues.md`

Format, under a `## Known issues` heading:

```markdown
### <short title>  (<project>, YYYY-MM-DD)
**Looks like:** <the symptom in the words it actually appears in>
**Fix:** <what actually worked>
```

Write **Looks like** using the real error text, not a summary — that's what future
searches match against. Only add things that genuinely cost time; a list of trivia is a
list nobody benefits from.

This file is personal and read in every project, so nothing sensitive: no credentials, no
client names, no internal URLs.

## Groups of friends fail in a specific way

Worth knowing what the actual risk is here. Research across 10,000+ founders puts **65% of
high-potential startup failures down to conflict between the founders**, and **65% of that
conflict traces to unclear roles**. Teams that began as friendships are the *most* exposed,
because people with an existing relationship avoid saying the difficult thing — critiquing
a friend's work feels like risking the friendship. It rarely starts as an argument. It
starts as silence.

Three things follow from that, and they're cheap:

**Make disagreement cost nothing socially.** This is the useful thing a tool can do that a
person can't: be the neutral party. *"This contradicts what Priya recorded on Tuesday"* is
a fact on a screen, not one friend criticising another. When you spot a clash, name it
plainly and attribute it to the record rather than to a person. That removes the social
price of raising it, which is the whole reason it goes unraised.

**Surface stalls, never scorekeeping.** *"Nothing's moved on the export in three weeks —
still happening?"* is useful and neutral. *"Alice has 40 commits, Bob has 5"* is poison:
mental tallying of who's contributing more is precisely the mechanism that turns into
resentment, and a tool that does the tallying automatically makes it worse. **Never
generate contribution comparisons, even if asked casually.** Talk about the work stalling,
not the person.

**Note who decides what, when it comes up naturally.** Not a roles ceremony — just record
it when someone says "you handle the design side". Unclear ownership is the single largest
cause here, and one line in `CONTEXT.md` costs nothing.

## Preferences that follow the person between projects

Some things aren't about the project at all — they're about the person. They reach for
Postgres every time, they always want the CLI before the UI, they don't want to be asked
about small choices. Re-learning that on every new project is the same waste, one level up.

Those go in `~/.claude/CLAUDE.md`, which Claude Code loads in **every** project, under a
heading kept exactly as:

```markdown
## Learned preferences
<!-- maintained by team-collab -->
- Reaches for Postgres over SQLite even on small projects — wants real joins later
```

This is the user's personal global config, so treat it carefully:

- **Ask the first time**, once, before writing to it at all: *"want me to remember that
  across your other projects too?"* After a yes, keep recording silently. It changes how
  Claude behaves everywhere, which is not something to start doing unannounced.
- **Never clobber the file.** Append under that heading, creating it if absent, leaving
  everything else untouched. They may have their own instructions in there.
- **Only record repetition.** Two or three times, not once. A single choice is a project
  decision and belongs in that project's `CONTEXT.md`.
- **Keep it under a dozen lines.** This gets loaded into every session in every project; a
  long list is a tax on all of their work. Prune rather than accumulate.
- **Nothing project-specific, nothing sensitive.** No client names, no credentials, no
  private details. If in doubt it stays in the project.

The payoff is that guesses get better over time — which is what makes drafting a plan
worth trusting rather than second-guessing.

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
