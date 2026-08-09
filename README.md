# Coordination Module

**Claude Code forgets your project between sessions. This fixes that.**

You spend an hour working out why Postgres and not SQLite, what that API does when the list
is empty, why the obvious approach failed. Next session Claude knows none of it — so you
explain it again, or you don't and it rebuilds the thing you already rejected.

This keeps those notes in the repo. Every Claude Code that opens the project reads them
automatically.

**You don't do anything to maintain it.** No commands, no dashboard, no process. You talk
and build normally; Claude writes things down and mentions it in a line.

## Install

One command, then a restart that genuinely matters — Claude Code only looks for new skills
at startup, and skipping it fails silently with no error.

```bash
git clone https://github.com/Pulkit-123/coordination-module.git ~/coordination-module && bash ~/coordination-module/install.sh
```

Quit Claude Code and reopen it. To confirm it took, ask any project *"what can you remember
about this project"* — if it has no idea, you didn't restart.

Once per machine. That's the whole setup.

## Use

Open a project and say *"remember things about this project"*. After that, just work.

What changes:

- Start a session and you get two lines on what's different, not a status report
- Decide something and the reasoning gets kept, so it isn't relitigated next month
- Hit a dead end and it's noted, so you don't lose the same hour twice
- Say *"I want to build X"* and you get a flow diagram and a plan before code gets written,
  which is usually cheaper than rebuilding twice

## Working with other people

Add them as collaborators on GitHub. They run the install once and clone the repo — the
notes travel with it, so their Claude Code starts with everything yours knows.

Their chat history is private to them, which is exactly the problem this solves. Two people
writing notes at the same moment both get kept, and if you both claim the same job you get
told, because git won't tell you.

## What's in the repo

| File | What's in it |
|---|---|
| `CONTEXT.md` | Decisions and why, dead ends, what the project is and isn't |
| `JOURNAL.md` | Reasoning, and arguments still open |
| `IDEAS.md` | Things someone wanted |
| `TASKS.md` | Who's on what |
| `journeys/*.md` | One per feature: the flow as a diagram, plus what it must do |

Plain markdown, plain git. No server, no API keys, no build step. It renders on GitHub if
you ever want to look, and you mostly won't need to.

## Is this for you?

Worth it if the project outlives a weekend, or someone else is working on it, or you've
already lost time re-explaining things.

Not worth it for a one-afternoon script. It's overhead, and you'd be right to skip it.

## Notes

`PLAN.md` has the design rationale and the failure modes found while stress-testing four
simulated collaborators. Two things to know before changing how merging works:

- **`merge=union` on the notes files is load-bearing.** Without it, two people writing at
  once collide and git silently keeps one.
- **That hides collisions in exchange**, so `check_collisions.py` exists to find them. It's
  lexical only — semantically-identical entries need the model's judgment.

An earlier version had a dashboard, a priority-ranking command, and a table of commands to
type. All removed: they required the user to do something extra, which is the one thing
that guarantees a tool goes unused.
