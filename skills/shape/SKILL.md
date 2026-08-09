---
name: shape
description: Help someone work out what to build before any code is written, by walking them through the user's journey step by step and turning it into a spec and a task list. Produces a mermaid flowchart plus written requirements in journeys/<slug>.md. Use this whenever someone is at the start of a feature or product and hasn't pinned down what it should do - phrasings like "I want to build X", "help me plan a feature", "where do I even start", "what should this actually do", "I have an idea for an app", "let's design X", "how should this work", "can you help me spec this out", "turn this idea into tasks", or when they describe a thing they want to build in vague terms and no journey file exists for it yet. Also use for "shape", "shape it", "journey", "map the journey", "user journey", "walk through the flow", "write the spec", "break this into tasks", "slice it". Especially valuable for people new to software who don't know which questions to ask themselves before building.
---

# shape

Gets an idea out of someone's head and onto paper, in a form that can actually be built.

## Why this exists

The reason software comes out badly is rarely that someone couldn't write the code. It's
that nobody worked out what it should do — so the empty state was never designed, the
failure case was invented at 2am, and the thing that shipped solved a slightly different
problem than the one that mattered.

Asking a beginner to "write a spec" doesn't fix that; it produces a blank page and a stuck
person. But **everyone can answer "walk me through what the person does."** They already
have a picture in their head. Your job is to get it out, make it visible, and interrogate
it step by step. The spec is a byproduct of that conversation.

Patton's line is the thing to remember: *shared documents aren't shared understanding.* A
filled-in template that nobody thought hard about is worse than nothing, because it looks
finished. **The interrogation is the value.** Never just generate a journey file and hand
it over — you'll produce the artifact without the understanding.

## Never announce the process

Do not say "let's start Phase 1" or "now we'll map your user journey" or explain this
methodology. Most people arriving here just said *"I want to build X"* and want to get on
with it. Naming a process makes it feel like paperwork standing between them and the thing
they're excited about, and they'll either disengage or rush through it to get to the end.

Just start talking. *"Nice — who's going to use it, and what makes them open it in the
first place?"* is a friendly question. *"Let's begin the discovery phase to establish your
job story"* is a form. Same information, completely different response.

Same when someone shows up with a one-liner and clearly wants you to just build it. Don't
refuse and don't lecture. Ask the two or three questions that would actually change what
gets built, then get going. You can shape the rest as you go — a journey file that grows
during the work is far better than one nobody had the patience to finish up front.

Only mention the files when there's something worth showing: *"here's the flow as I
understand it"* with the diagram. The artifact should feel like a helpful side effect, not
the reason you were asking.

## Opening: match how they arrive

People turn up in two modes, and using the wrong approach loses them immediately.

**The ones who arrive full of it** will type three paragraphs about their idea. **Let them
finish.** Don't interrupt with structure, don't ask a clarifying question halfway through.
When they're done, reflect it back organised — the steps in order, what you understood the
goal to be — and *that* is where they see the gaps themselves. Someone reading their own
idea laid out in sequence will spontaneously say "oh, and it also needs to…". That moment
does more than any question you could ask.

**The ones who arrive with a sentence** — "I want to build a habit tracker" — need a way
in, not a questionnaire. Give them one concrete opening, and make it a question about a
person rather than about features:

> *"Nice. Picture someone opening it — what's happened in their day that made them reach
> for it?"*

That question is already doing the teaching. It frames the whole thing around user intent
instead of a feature list, which is the single most useful habit you can hand someone. But
you never said "always start from user intent" — they just did it.

If they stall, offer a guess to react to rather than another question. *"I'm imagining
they just finished a workout and want to tick it off — something like that?"* Reacting is
much easier than generating, and their correction will be more precise than anything a
blank prompt would have produced.

## Show the diagram as it grows

Talking about a flow is abstract. Seeing it drawn is not — and someone looking at their own
idea as a picture spots missing steps immediately, without being asked.

Show the journey file in the side panel and keep it updated:

```
SendUserFile(files=["journeys/<slug>.md"], display="render", status="normal")
```

Markdown renders there with the mermaid diagram drawn, so they see the actual shape rather
than source code.

**Draft first, ask second.** Don't start from an empty file. As soon as they've described
the thing even roughly, sketch a first-pass flow — your best guess at the steps — and show
it. *"Here's what I think you mean — what's wrong with it?"* Correcting a wrong diagram is
enormously easier than producing a right one from nothing, and it removes the blank-page
problem entirely. Being wrong is fine and often better: a wrong step gets an immediate,
specific correction.

**Mark what's still uncertain** so the picture shows its own gaps. Dashed borders and a
question mark read instantly:

```
flowchart TD
    A([Opens app]) --> B[Picks a habit]
    B -.-> C[?? What if they have none yet]
    class C unknown
    classDef unknown stroke-dasharray:4,stroke:#999,color:#999
```

Re-send at **meaningful moments** — after the happy path is complete, after a round of
failure states, when a phase finishes. Not after every single edit; a panel that flickers
constantly is worse than one that updates when something changed. Three or four times in a
session is about right.

This is also what makes progress visible. *"That's the main flow done — three failure
cases left"* alongside a diagram that visibly filled in is what stops it feeling like an
endless interview.

## Teach by asking, not by explaining

The point is that people come out of this better at thinking about what they build — but
nobody wants a lecture on requirements engineering while they're excited about an idea.

**Ask the question instead of naming the principle.** Not *"you should always define your
empty state"* — instead *"what do they see the very first time, before they've added
anything?"* They learn the question by being asked it, and after two or three features
they start asking it themselves. That's the whole mechanism.

A few things that make this work:

- **Name the principle only after they've felt it, and only once.** When someone says "oh
  — I hadn't thought about that", a single short line is worth a lot: *"that one catches
  almost everyone — the empty screen is the first thing a new user ever sees."* Then move
  on. Repeating it turns it into nagging.
- **Reflect their words back with better structure**, using their vocabulary rather than
  yours. If they say "the thingy where you pick a date", write "pick a date" in the
  diagram — not "date-range selection component". Their idea should stay recognisably
  theirs; that's what keeps them engaged with it.
- **When they get something right unprompted, say so briefly.** If they volunteer "and if
  the upload fails we should keep what they typed" — *"yes, exactly that"* — takes a
  second and reinforces the habit far better than praise-free silence.
- **Never imply they should have known something.** No "as you'd expect" or "obviously".
  The people who most need this tool are the ones who'd quietly conclude they're not cut
  out for it.

## When they don't know the answer

This is the thing that makes tools like this fail. You ask a good question, they don't
know, you ask another, they don't know either — and now they feel tested on their own idea.
People disengage quickly from that, and once they do, everything after it is shallow.

**A question someone can't answer is worse than a question you answer for them.** The goal
is a well-shaped feature, not a completed interview.

So when an answer isn't there, escalate down this ladder instead of pressing:

1. **Ask once, plainly.** *"What should they see if there's nothing there yet?"*
2. **Offer concrete options.** Reacting is much easier than generating. *"Could be an empty
   box with a 'create your first one' button, or some sample data to play with — any
   preference?"*
3. **Propose a default and move on.** *"I'll assume a simple empty state with a create
   button — that's what most apps do. Easy to change later."* Then **mark it as an
   assumption in the file, not a decision**, so it's visibly unresolved rather than
   silently baked in.
4. **Drop it entirely** if it's genuinely not important yet. Not every step needs all nine
   answers.

Read the signals and stop pressing when you see them: *"I don't know"*, *"you decide"*,
*"whatever you think"*, one-word answers where they were previously expansive, or answering
a different question than the one you asked. That last one usually means the question
didn't make sense to them — rephrase in their language rather than repeating it.

Be especially quick to fall back when the question is outside what they'd reasonably know.
Asking someone building their first app how they want to handle token refresh or database
migrations isn't rigour, it's just making them feel stupid. Make the call, tell them what
you assumed and why in one line, and keep moving.

**Watch the overall budget too.** Roughly three or four questions per step is plenty, and
if the whole conversation is dragging, offer the exit: *"want to sketch the rest roughly
and tighten it up once you've seen it working?"* Half a journey someone believes in beats a
complete one they resented filling in.

## The four phases

Names are for you, not for them — don't use these words out loud.

Work through them in order. They're resumable: read the existing `journeys/<slug>.md`
first, see how far it got, and carry on rather than restarting. Say which phase you're in
and roughly how much is left, so it doesn't feel endless.

Skip ahead when the person clearly already knows something. A one-screen feature does not
need ceremony — the point is to prevent missed requirements, not to perform process.

### Phase 1 — `discover`: what is this, and for whom

Short. Three or four exchanges, not an interview.

Get to a **job story**, which replaces the usual persona format:

> **When** [situation], **I want to** [motivation], **so I can** [outcome].

Use this rather than "As a [type of user], I want…" deliberately. Personas don't explain
causality — knowing someone is a 34-year-old designer tells you nothing about why they act.
The *situation* does. It also stops people inventing demographics they have no evidence for.

Also establish the boundary: what is explicitly **not** part of this. If the project has a
Scope section in `CONTEXT.md`, check the idea against it and say something if it drifts.

### Phase 2 — `journey`: the interrogation

The core of the skill, and where the value is.

**Walk the happy path first, uninterrupted.** Get the whole sequence of steps end to end
before asking a single "but what if". This ordering matters — if you let someone start
enumerating failure cases at step two, they rathole there and never map the rest.

Then go back over each step with the checklist below. **Ask one or two questions at a
time, conversationally.** Never dump the whole list as a form; that's how you get shallow
answers to all nine questions instead of real answers to the three that mattered.

Per step, as relevant:

- **What makes them arrive here?** (the trigger — often reveals a missing prior step)
- **What do they do, and what does the system do back?**
- **What does it look like with zero, one, and lots?** (the empty and partial states — the
  most commonly forgotten thing in software)
- **What if it's slow?** (loading feedback)
- **What can they get wrong here — and can we stop it happening?** (prevention beats a
  good error message)
- **What can the system get wrong, and what do we say when it does?** (an error message
  that doesn't say what to do next is a dead end)
- **Who's allowed to do this?** (permissions)
- **Is this the first time they've ever seen this screen?** (first-run is not the same as
  empty)
- **What do we not know?** → record it as an open question rather than guessing

Not every question applies to every step. Judgment beats completeness — asking "what if
it's slow?" about a purely local UI toggle wastes their attention and trains them to skim.

Write each answer into the journey file as you go, and keep the flowchart updated so they
can see it taking shape. Seeing their own idea drawn back at them is what makes people
spot the gaps themselves.

### Phase 3 — `spec`: turn the journey into rules

Use **Example Mapping**, which is deliberately lightweight:

- **Rules** — the acceptance criteria. Plain checklist bullets.
- **Examples** — one concrete line each, with real values, showing a rule in action.
  Concrete beats abstract: "uploading a 12MB file shows 'Files must be under 10MB'" is
  worth more than "validates file size".
- **Questions** — anything nobody can answer yet. Keep these visible rather than resolving
  them by guessing.

Two diagnostics come free with this, and both are genuinely useful signals:

- **Lots of questions → it isn't understood yet.** Don't proceed to slicing. Say so.
- **Lots of rules → it's too big.** Propose splitting into separate journeys.

Default to checklists. Only use Given/When/Then for the two or three rules that genuinely
span multiple steps — full Gherkin without a test runner is syntax tax with no payoff, and
beginners reliably write click-by-click UI steps that rot immediately.

### Phase 4 — `slice`: what gets built first

Find the **walking skeleton**: the thinnest path that goes end to end and still delivers a
complete outcome. Not "the first third of the steps" — a thin version of *all* of them.

Then, with the person's agreement:

- Walking-skeleton work → rows in `TASKS.md`
- Everything else → entries in `IDEAS.md`, so it's kept but not blocking
- Open questions → an open thread in `JOURNAL.md`
- Decisions made along the way → `CONTEXT.md` with the reasoning

Claiming and pushing tell other people something, so ask before doing them — the existing
rule in `CLAUDE.md` applies here too.

## Offering research — the part that teaches

Showing how existing products solve a step is where someone new actually learns. *"Linear
shows a skeleton row rather than a spinner here, because the layout doesn't jump when it
loads."*

But doing this at every step is slow, expensive, and after the third time people skim past
it. **Offer it, and go deep on the two or three steps that carry real risk** — the payment
step, the permissions model, the thing they've never built before. Ask before running web
searches; they cost time the person may not want to spend right now.

## The diagram

Use `flowchart TD`. **Never use mermaid's `journey` type** — its grammar is only
`title`, `section`, and `Task: <score>: <actor>`, so it cannot express branching at all.
It's a diagram of how the user *feels*, not of what happens, and the branches are exactly
what this skill exists to surface.

Structure: happy path down the trunk, each error/empty/permission state as a labelled
branch off it. This makes coverage visible — **a trunk with no branches is an unfinished
journey**, and the person can see that at a glance.

```
flowchart TD
    Start([User opens the export page]) --> Check{Any data to export?}
    Check -->|No| Empty[Show: nothing to export yet]
    Check -->|Yes| Pick[Choose date range and format]
    Pick --> Submit[Click Export]
    Submit --> Gen[Generating… progress shown]
    Gen -->|Success| Done([File downloads])
    Gen -->|Too large| Split[Offer to split into monthly files]
    Gen -->|Server error| Err[Show retry, keep their selections]
```

Hard constraints when generating mermaid:

- **Never emit `click`** — GitHub blocks the entire diagram and shows "This content is
  blocked" instead.
- **Keep under about 40 nodes.** Mermaid fails on edge count and layout well before its
  50,000-character limit, and that limit can't be raised from inside a diagram. Past ~40
  nodes the journey is too big anyway — split it.
- Avoid HTML in labels; GitHub sanitizes it.
- Quote labels containing brackets, quotes, or colons.

Check the result before showing it:

```bash
python3 "$SKILL_DIR/scripts/check_journey.py" journeys/<slug>.md
```

It flags steps with no failure branch, unanswered questions, oversized diagrams, and
`click` directives.

## Writing the file

One file per feature: `journeys/<slug>.md`, from `assets/journey.md.template`. Slug is
kebab-case from the feature name.

**Journey files are edited in place, so they must not be union-merged.** The append-only
coordination files use `merge=union` to keep both sides of a simultaneous edit; doing that
to a flowchart produces a corrupt diagram with duplicated nodes. Two people rewriting the
same journey *should* get a conflict and talk to each other.

## Working with a group

A journey is a shared object people can argue about concretely — "step 4 is wrong" is a
far better conversation than "the spec feels off". When someone else's journey file already
exists, read it before proposing changes, and put disagreements in `JOURNAL.md` as an open
thread rather than silently rewriting their steps.
