---
name: shape
description: Turn a rough idea into a concrete plan before building it - draft the user's flow as a diagram, fill in the parts they didn't think about, and produce acceptance rules and a first slice in journeys/<slug>.md. Use whenever someone describes something they want built and the details aren't pinned down - "I want to build X", "let's add X", "can you make an app that…", "help me plan X", "where do I start", "I have an idea for…", "build me a X" where X is more than a small change. Also for "shape", "journey", "map the flow", "spec this out", "break this into tasks". Especially for people who don't know which questions to ask themselves before building, and for anyone who has had to rebuild something because the first attempt solved the wrong problem.
---

# shape

Turns "I want to build X" into a plan, mostly without asking them anything.

## What this is actually for

Not documentation. **Avoiding rebuilds.** The expensive failure is describing an app,
getting something that's wrong in a way nobody anticipated, and going round three times.
Most of that comes from a handful of things nobody thought about up front: what the screen
shows before there's any data, what happens when the request fails, who's allowed to do it.

So the value proposition is speed, not rigour. Two minutes now instead of three rounds
later. Anything that makes this feel like paperwork has destroyed the point.

## The core move: draft it, don't interview

**Never ask a series of questions.** From whatever they've said — even one sentence —
write the whole journey yourself: the steps, the empty state, the failure branches, the
permissions. Use conventional defaults for everything you don't know.

Then show it and ask one question:

> Here's how I'd build it — what's wrong?

Correcting a draft costs a person almost nothing. Producing one from a blank page costs
them a lot. That difference is the entire skill.

A wrong guess is fine and often better than a vague one — it gets an immediate, specific
correction. "No, people shouldn't need an account" is a better answer than anything a
question would have produced.

### The draft is a mirror, not a substitute

There's a line here worth being careful about. If they described the flow and you tidied it
into a diagram, that's their thinking made visible — useful. If they said one vague
sentence and you invented an entire product, that's **your** idea wearing their name, and
they'll nod along at something they never thought about.

So the draft only extends what they actually said, in the directions convention makes
obvious — a list screen implies an empty state, a form implies validation, a login implies
a wrong-password path. Fill those in freely; nobody has a special opinion about them.

Anything that's a genuine product decision — what it's for, who it's for, what's in and
out — stays **visibly blank or visibly guessed**, never quietly invented. Show it as a
question mark in the diagram, or a line in the chat:

> Two things I couldn't tell from what you said: whether other people can see someone's
> entries, and whether this needs to work on a phone. Guessed private and phone-first.

If they don't answer, that's fine — carry on with the guess and leave it marked in the
file. Someone who doesn't know yet genuinely doesn't know, and pressing them turns a
useful five minutes into an exam. They'll correct it the moment it matters, which is
usually the first time they see it working.

### Make assumptions specific, so wrong ones are obvious

The risk with drafting is that they skim, say "looks good", and now there's a plan nobody
actually thought about. The fix is not more questions — it's writing assumptions sharply
enough that a wrong one jumps out.

- Bad: "assumes standard permissions" — nobody reacts to this
- Good: "assumes anyone with the link can view, no account needed" — gets corrected instantly

List them in the file under **Assumptions**, and put the two or three riskiest in the chat
message. Everything else stays in the file for later.

### Ask for what only they know — and nothing else

There's a real hazard in doing all of this for someone. Research on AI and learning
distinguishes **dependent offloading** — handing over the actual thinking, which correlates
with worse outcomes — from **autonomous offloading**, where the tool does the legwork and
the person keeps the judgment, which correlates with better ones. The named failure is
*metacognitive laziness*: people stop setting goals, monitoring errors and reflecting,
because the output reads so fluently that it produces an illusion of competence.

A tool that silently decides everything produces exactly that. So the line isn't "ask less",
it's **ask for precisely the things you cannot possibly infer, and infer everything else.**

You can infer, so don't ask: what an empty screen should say, that failures need a message,
that a form needs validation, what the conventional flow looks like, what to call things.

You cannot infer, so do ask — briefly, once:

- **Who is the first real person who'd use this?** Not "users" — a person they can name.
- **What would make this a failure?** If nobody touches it in a fortnight, what would that
  tell them?
- **What matters more here, and what doesn't?** Their priorities aren't derivable from the
  feature description.

That's two or three questions in total, and they're the only parts genuinely theirs. It
also happens to be the highest-value information in the whole exercise — everything else is
convention you can supply.

If they won't answer, drop it and carry on. Asking twice turns a useful question into an
exam.

### A note on the first user

Most of discovery can't be automated and pretending otherwise would be dishonest. Talking
to someone who might actually use the thing is real work, and no tool removes it.

What you can do is make its absence visible exactly once, without turning it into a gate:

> Who's the first person who'd actually use this — anyone you could show it to this week?

If the honest answer is "just us", that's fine and worth saying plainly: it's a project for
themselves, which is a perfectly good reason to build something. It's only worth flagging
when they believe other people want it and haven't checked — **42% of startups fail for
exactly that reason**, and asking friends "would you use this?" is the weakest signal there
is. Someone actually turning up to use it is the strong one.

Say it once. Never again.

### Ask only when you genuinely can't guess

One or two questions maximum, and only when the answer changes the whole shape — is this
for one person or a team, does it need to work offline, is there money involved. Never ask
about something they'd have no way to know; make the call and say what you assumed.

Read the room: "I don't know", "you decide", "whatever's normal", or one-word replies mean
stop asking and start assuming.

## Show it building, then get out of the way

Write the file as you go and open it in the side panel so they watch the flow appear:

```
SendUserFile(files=["journeys/<slug>.md"], display="render", status="normal")
```

Show it **once** when the draft is ready, and again only if they change something
substantial. Then stop mentioning it. The file stays in the repo and you read it before
building — they never have to open it again.

## What goes in the file

Use `assets/journey.md.template` → `journeys/<slug>.md`.

The diagram is a mermaid `flowchart TD`: happy path down the trunk, each failure or empty
state as a labelled branch. **Never mermaid's `journey` type** — it cannot branch at all,
so it can't show the failure states that are the whole point.

Cover these when drafting, because they're what people forget:

- What's on screen when there's nothing yet (first run is not the same as empty)
- One item vs hundreds
- What the user can get wrong, and whether it can be prevented
- What the system can get wrong, and what it says when it does
- Who's allowed to do it

Then acceptance rules as a plain checklist, and a **first slice** — the thinnest version
that works end to end, not the first third of the steps.

Check it before showing:

```bash
python3 "$SKILL_DIR/scripts/check_journey.py" journeys/<slug>.md
```

It flags a flow where nothing ever fails, `click` directives (GitHub refuses to render the
whole diagram), and diagrams over ~40 nodes.

## Scale to the size of the thing

A small change doesn't need any of this — just build it. A screen or two needs a short
flow and three rules. Only something genuinely large needs the full treatment.

If they came in saying "just build it", don't refuse and don't lecture. Draft the plan in
the background, state the two riskiest assumptions in one line, and start building. They
can correct you mid-flight.

## Never name the process

Don't say "phase", "discovery", "user journey mapping", or explain any methodology. Say
what you're doing in plain words — *"here's how I'd build it"* — or say nothing and just
show the diagram.

Same for principles. Don't tell someone to define their empty state; just put the empty
state in the draft. If they notice and say "oh, good catch", one short line is worth it —
*"that one catches most people"* — and then move on.

## When they say it's done

The rules in the journey exist for exactly this moment. Someone builds a feature, tries it,
it works, and they call it finished — then it breaks the first time a list is empty or a
request fails, because those cases were written down and never implemented.

So when someone says a feature is done and a journey exists for it:

```bash
python3 "$SKILL_DIR/scripts/check_done.py" journeys/<slug>.md
```

It lists the rules nobody ticked off, marks the ones with no trace in the code, and
resurfaces assumptions and questions that were never resolved.

**It cannot tell you whether a rule is actually met** — that needs reading the code, which
is your job. Use its output as a shortlist, check each one properly, then say plainly which
hold and which don't:

> Mostly there. The empty list still renders a blank page though — the plan said it should
> say "nothing to export yet". Want me to add that before we call it done?

Keep it to the ones that genuinely aren't met. Reciting a checklist at someone who just
finished something is the fastest way to make them stop writing plans at all. If everything
holds, say so in a line and move on.

## Check what already exists — once, at the start

Before drafting, one search on what's already out there. This is the cheapest piece of
discovery there is and it costs the person nothing:

> Three apps do roughly this. The recurring complaint about all of them is that setting up
> takes twenty minutes before you see anything. Worth being the one that doesn't.

Two useful outcomes and no bad one. Either nothing quite does it — encouraging, and now you
know the gap — or several do, and the interesting question becomes what they get wrong.
"This already exists" is almost never a reason to stop; it's a reason to aim at the part
everyone complains about.

Keep it to one search and two sentences. Don't produce a competitive analysis.

## Tracking, added while building rather than never

Analytics gets skipped for a concrete reason: wiring it up takes a week when the build took
a day, so it gets cut, and the thing ships with no data and a vague sense that nobody's
using it.

The journey is already the funnel — the steps are the events. So derive them:

```bash
python3 "$SKILL_DIR/scripts/journey_events.py" journeys/<slug>.md
```

Add those lines **during the build that's happening anyway**, which makes the cost to the
person zero. Use whatever the project already has — PostHog, Plausible, a row in their own
database. The tool matters far less than being able to answer "did anyone get through this"
in a fortnight.

Track the failure branches too. Knowing eleven people started and two finished is mildly
interesting; knowing nine of them hit the empty state is the thing that tells you what to
fix.

Don't exceed the handful the script suggests, and don't build anything to view it. A long
event list becomes a dashboard nobody opens — the same failure as no data, with more work.

## Handing off to the build

When the plan is agreed, put the first slice into `TASKS.md` and the rest into `IDEAS.md`,
and note any real decisions in `CONTEXT.md` with the reasoning. That's what stops the same
questions coming back in a fortnight.

If someone else already wrote a journey for this, read it first and don't quietly rewrite
their steps — put a disagreement in `JOURNAL.md` instead.
