# coordination-module

## Project memory

This repo keeps notes so Claude Code doesn't forget things between sessions. **The person
working here should never have to do anything to maintain them.** No commands, no files to
open, no process. They talk and build normally; you keep the notes.

| File | What's in it |
|---|---|
| `CONTEXT.md` | Decisions and why, dead ends already hit, what the project is and isn't |
| `JOURNAL.md` | How things were reasoned through, and arguments still unresolved |
| `IDEAS.md` | Things someone wanted, not yet built |
| `TASKS.md` | Who's working on what right now |
| `journeys/*.md` | One per feature: the flow as a diagram, plus what it must do |

### Start of a session

Pull, read those files, then say **only what changed** since they were last here, in two or
three lines. If nothing changed, say nothing. Don't announce that you read anything, and
never print an unrequested status report — that's the friction this is meant to remove.

### While working

When something durable comes up, write it down and mention it in **one line**. Don't ask
first — these are additive and easy to correct.

- A choice settled → `CONTEXT.md`, **with the reasoning**, or it gets relitigated
- A dead end or trap → `CONTEXT.md` gotchas, so the next person doesn't lose the same hour
- An idea floated → `IDEAS.md`
- A real back-and-forth about approach → `JOURNAL.md`, including what was rejected
- An unresolved disagreement → `JOURNAL.md`, with both positions

Match meaning, not wording. Someone saying "I'll take the export" is claiming it; "that
works now" is finishing it; "tried X, it broke" is a gotcha. Nobody should need to know a
command exists.

Use judgment — keep what someone would want to find later, not every passing remark.

### The only two things worth asking about

Claiming work and marking it done, because those tell *other people* something and a wrong
one wastes their time. One short line: *"want me to note you're on this so nobody doubles
up?"*

If nobody else has access to this repo, don't even ask — just note it.

Never ask twice about the same thing. If they say stop, record silently from then on.

### Let the memory prove itself

When a note actually saves them something, say so in one line — *"you chose Postgres in
week one because of the joins, so sticking with that."* That's the only visible payoff
this has, and it costs nothing.

### Before it ships

Run the safety check before any commit or push:
`python3 ~/.claude/skills/team-collab/scripts/safety_check.py`

It only fires on things that can't be undone — a real credential about to be committed, a
tracked `.env`, Supabase tables without row level security, a migration that drops or
truncates without a filter, an auth check that always returns true. Exit 2 means stop: a
pushed key is public permanently, and only rotating it helps.

Then say in one sentence what the change lets the software *do* —
`python3 ~/.claude/skills/team-collab/scripts/what_changed.py` surfaces the signals.
"Anyone with the link can now read every entry" is a review someone non-technical can
actually push back on; "added a GET route without auth middleware" isn't. Stay quiet on
refactors.

### Decisions that are hard to undo

A beginner can't tell a cheap choice from a permanent one. Hard to reverse once there's
real data: the data model, whether accounts exist, single-user vs shared, real-time or
not, where data lives, any public URL others depend on. Easy: framework, styling, wording,
hosting, most libraries.

Flag the first kind in one line — *"worth thirty seconds, this one's painful to change
later"* — record the reasoning, and move on. Never make it a gate.

### When something breaks

Before debugging an error, check whether it's been solved before — in this project or any
other. Beginners repeat mistakes across projects, not within them, because each repo's
notes are stuck in that repo:

```
python3 ~/.claude/skills/team-collab/scripts/recall.py "<the error text>"
```

If a gotcha you record is about a tool rather than this project — a build quirk, a library
trap — also append it to `~/.claude/known-issues.md` so it's there next time, in whatever
project that turns out to be.

### Before agreeing something is finished

If a journey exists for it, the rules in it were agreed for this exact moment — the empty
state, the failure case, the things that get skipped because the happy path works. Check
them, mention only what genuinely isn't met, and don't recite the whole list.

### If several people work here

Friend groups fail in a specific way: nobody says the difficult thing, because criticising
a friend's work feels like risking the friendship. It starts as silence, not argument.

Be the neutral party — *"this contradicts what Priya recorded on Tuesday"* is a fact, not
one friend criticising another, and that removes the social cost of raising it.

Surface **stalls**, never scorekeeping. "Nothing's moved on the export in three weeks" is
useful. "Alice has 40 commits, Bob has 5" is corrosive — never generate contribution
comparisons, even if asked casually. And note who owns what when it comes up naturally;
unclear roles are the largest single cause of these teams breaking up.

### Preferences that follow the person, not the project

If the same choice keeps recurring across their projects — always Postgres, always CLI
first, never wants to be asked about small things — that belongs in `~/.claude/CLAUDE.md`
under a `## Learned preferences` heading, so it applies everywhere instead of being
relearned each time.

Ask once before writing there the first time; it changes Claude's behaviour in all their
projects. Only record things seen two or three times, never one-offs, and keep it short —
it loads into every session. Nothing project-specific or sensitive.

### Before building something non-trivial

Check `journeys/` for an existing flow, and read `CONTEXT.md` for decisions that constrain
it. If it's a real feature and no journey exists, draft one first — the flow, what happens
when it's empty, and what happens when it fails. That's what stops a rebuild.

### Publishing

Push notes as they're made; an update nobody can see is no update. Expect rejections when
several people are active — pull with `--rebase` and retry rather than force-pushing.

Code is different: work on a branch and let the person decide when to merge.
