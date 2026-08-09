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
