# Getting started

Two minutes. Assumes you know nothing about this.

---

## What problem this solves

You're building something with Claude Code. You explain your project, make decisions, hit
problems and work around them.

Next session, Claude has forgotten all of it. You explain it again. Or you don't, and it
happily rebuilds something you already decided against.

This keeps notes in your project folder so that stops happening.

**You don't have to write the notes.** Claude does it while you talk, and tells you in one
line when it does.

---

## Install (once per computer)

Paste this:

```bash
git clone https://github.com/Pulkit-123/coordination-module.git ~/coordination-module
```

Then this:

```bash
bash ~/coordination-module/skills/team-collab/scripts/update_skill.sh
```

**Now quit Claude Code and open it again.** It only looks for new skills when it starts. If
you skip this, nothing will work and there'll be no error to tell you why.

Done. You never do this again.

---

## Turn it on for a project (once per project)

Open the project and say:

> remember things about this project

Claude adds a few notes files. Then say **commit and push** so they're saved.

That's it. Now just work.

---

## What you'll notice

Nothing to learn. You talk normally and Claude keeps up:

| You say | What happens |
|---|---|
| "let's use Postgres, we need joins" | The decision *and the reason* get kept |
| "careful, that API breaks on empty lists" | Noted, so nobody hits it again |
| "it'd be nice if it had dark mode" | Added to the ideas list |
| "I'll take the login page" | Asks if you want it noted, so nobody doubles up |

Say it however you say it — there are no magic words.

And when you come back tomorrow, you get two lines on what changed rather than a blank
slate.

---

## Planning something bigger

Say *"I want to build a habit tracker"*, or whatever it is.

Instead of asking you twenty questions, Claude **drafts the whole thing** — the steps, what
the screen shows when there's nothing there yet, what happens when it breaks — draws it as
a diagram in the side panel, and asks one thing:

> Here's how I'd build it. What's wrong?

Fixing a wrong guess takes you ten seconds. Answering twenty questions doesn't. It'll tell
you the assumptions it made, so if one's wrong you'll spot it.

Then it builds. The plan stays in `journeys/` and you never need to open it.

---

## Building with friends

Add them on GitHub: your project → **Settings** → **Collaborators** → **Add people**.

They run the same one command above (and restart), then `git clone` your project. Their Claude
starts out knowing everything yours knows.

If you both write notes at the same moment, both are kept. If you both claim the same job,
Claude tells you — GitHub won't.

---

## When something's wrong

**"Claude has no idea about any of this"** — you didn't restart after installing. That's
almost always it.

**"Push was rejected"** — someone pushed first. Say `push again`. If you're not a
collaborator yet, ask whoever owns the repo.

**"Claude keeps asking me things"** — say *stop asking, just note things quietly*. It'll
remember for the session.

**"I want the latest version of this tool"** — rerun the install command, then restart.

**"I installed it but nothing happens and there's no error"** — that's the restart. It's
always the restart.

---

## The only thing to remember

Say things out loud as you work. Decisions, problems, half-thoughts.

Anything you only think and never say stays invisible — to Claude tomorrow, and to anyone
else on the project.
