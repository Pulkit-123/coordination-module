# Getting started (the simple version)

This guide assumes you know nothing about this tool. It takes about 5 minutes.

---

## What is this, in one paragraph

You and your friends are each building things with Claude Code. The problem: your chat
with Claude is private. Your friend's chat is private. So Claude on your laptop has no
idea what Claude on their laptop already figured out, decided, or is halfway through
building. You end up building the same thing twice, or undoing each other's decisions.

This tool fixes that by writing everything important into a few text files inside your
project. Those files go on GitHub. Everyone's Claude reads them automatically. Now
everyone's Claude knows the same things.

**You don't have to write those files yourself.** You just talk normally, and Claude
writes them for you.

---

## Part 1 — Install it (once per computer)

Open your terminal and paste this:

```bash
git clone https://github.com/Pulkit-123/coordination-module.git ~/coordination-module
```

Then paste this:

```bash
bash ~/coordination-module/skills/team-collab/scripts/update_skill.sh
```

You should see `team-collab: installing (new)` and `why: installing (new)`.

**Now close Claude Code completely and open it again.** This matters — Claude only
looks for new skills when it starts up. If you skip this, it won't find them.

That's the whole installation. You never need to do it again on this computer.

---

## Part 2 — Turn it on for a project (once per project)

Open your project folder in Claude Code and type:

```
setup team
```

Claude creates 6 files in your project. You don't need to memorise them, but here's what
they're for:

| File | In plain words |
|---|---|
| `IDEAS.md` | The wish list. Anything anyone thinks of. |
| `journeys/` | One file per feature: how it works, drawn as a diagram. |
| `TASKS.md` | Who is doing what right now. |
| `PRIORITIES.md` | What to build next, in order. |
| `CONTEXT.md` | What you've decided, and mistakes you already made. |
| `JOURNAL.md` | The story of your discussions and open arguments. |
| `CLAUDE.md` | Instructions for Claude. Don't edit this one. |

Then tell Claude:

```
commit and push
```

Now your friends can see it.

---

## Part 3 — Add your friends (once per project)

On GitHub, open your project → **Settings** → **Collaborators** → **Add people** → type
their GitHub username.

They accept the invite by email, then run **one** command:

```bash
git clone <your-project-url>
```

That's it for them. They don't install anything extra for the project — the instructions
travel inside it. (They do need Part 1 done once on their own computer.)

---

## Part 4 — Using it day to day

**This is the important part: there are no commands to learn.** Just talk to Claude
normally while you work. It listens for certain things and offers to write them down.

Here's what happens:

| You say something like | Claude does this |
|---|---|
| "I'll take the login page" | Asks: *want me to claim that so nobody doubles up?* |
| "the login page works now" | Asks: *mark it done and push?* |
| "it'd be nice if we had dark mode" | Writes it into the wish list, tells you it did |
| "let's use Postgres instead of SQLite" | Writes down the decision **and why** |
| "careful, that API breaks if you send an empty list" | Writes it down so nobody hits it again |
| "I'm stuck waiting on the API key" | Marks you as blocked |

You don't need those exact words. Say it however you say it.

**Why does it ask sometimes but not others?** If it only affects the notes, it just does
it and tells you. If it tells your *friends* something — like "I'm working on this" or
"this is finished" — it asks first, because getting that wrong wastes their time.

### Planning something new

If you're about to build a feature and aren't sure what it should do, just say so —
*"help me plan the export screen"*, or even *"I want to build a habit tracker"*.

Claude walks you through it by asking about the person using it: what they do first, what
they see when there's nothing there yet, what happens when it breaks. It draws the flow as
a diagram in the side panel as you talk, so you can see it taking shape and spot what's
missing.

**You don't have to know all the answers.** Say "I don't know" or "you decide" and it'll
suggest something sensible, note it as an assumption, and move on. The point is to catch
the things people usually forget — not to test you.

It saves everything to `journeys/<name>.md`, and turns the first chunk into tasks when
you're ready.

### Four things worth typing on purpose

| Type this | What you get |
|---|---|
| `catch me up` | What changed since you were last here |
| `what's next` | Claude ranks the wish list and tells you what to build first |
| `status` | Who's doing what right now |
| `why did we drop X?` | Claude finds the decision and explains the reasoning |

---

## Part 5 — Seeing what's going on

**Three ways, pick whichever you like:**

1. **Just ask Claude.** Type `status` or `catch me up`. Easiest.

2. **On GitHub in your browser.** Click on `IDEAS.md` or `TASKS.md`. GitHub displays them
   nicely, and it works on your phone.

3. **The dashboard.** Everything on one page. Type `refresh` in Claude, then open the
   `dashboard.html` file in your project by double-clicking it. It opens in your browser.

⚠️ The dashboard is a **snapshot**, not a live page. It shows what things looked like when
someone last refreshed it. Type `refresh` to bring it up to date.

---

## Part 6 — Working at the same time as your friends

**Start of the day.** Say `catch me up`. Claude downloads everyone's changes and tells you
what happened.

**Before you build something.** Say what you're about to do. Claude checks nobody else has
claimed it, and claims it for you.

**When you finish.** Say so. Claude marks it done and shares it.

**Things are designed so nothing gets lost.** If you and a friend write notes at the exact
same second, both are kept — the tool never throws one away.

But there's a catch worth knowing: because nothing is ever thrown away, you can both claim
the *same job* and neither of you gets a warning from GitHub. So Claude runs a check for
that and tells you. If you see *"DUPLICATE WORK: you're on X and Priya is on X"* — message
each other and decide who keeps it.

---

## If something seems wrong

**"Claude doesn't know about any of this"**
Did you restart Claude Code after installing? That's almost always it.

**"I can't push, it says rejected"**
Someone pushed just before you. Say `push again` — Claude handles it. If you're not a
collaborator on the project yet, ask the owner to add you.

**"The dashboard looks out of date"**
It is. Type `refresh`, then reopen the file.

**"Claude keeps asking me things"**
Say `stop asking, just record things quietly`. It'll remember for the rest of the session.

**"I want to update the tool itself"**
```bash
bash ~/coordination-module/skills/team-collab/scripts/update_skill.sh
```
Then restart Claude Code.

---

## The one rule

**If it matters, say it out loud to Claude.** Decisions, problems, half-formed ideas.
Claude writes it down, your friends' Claude reads it, and everyone stays on the same page.

Anything you only think about and never say is invisible to everyone else. That's the
entire problem this tool exists to solve.
