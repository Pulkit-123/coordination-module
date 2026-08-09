# Ideas — coordination-module

Anyone can add an idea. Append to the bottom, never edit or delete someone else's entry —
appending is what keeps two people adding ideas at the same time from conflicting in git.

Rough or half-formed ideas are welcome. `team-collab triage` will ask you clarifying
questions rather than silently dropping them.

**Format:**

```
### <short title>
- **From:** <your name>
- **Date:** YYYY-MM-DD
- **What:** one or two sentences on the idea
- **Why:** the problem it solves (optional, but it's what decides priority)
```

---

### ~~SDLC toolkit — skills for the whole product development cycle~~ (BUILT)
- **From:** pulkit
- **Date:** 2026-08-09
- **What:** A modular set of skills covering planning, specs, architecture, task
  breakdown, implementation, testing and deployment, encoding good practice as defaults.
- **Why:** We're new to structured development and don't know what good steps look like.
  Wanting the tool to teach the process, not just track it.
- **Status:** built as the `shape` skill. spec-kit not adopted — see CONTEXT.md.

### Add collaborators and start using this on a real project
- **From:** pulkit
- **Date:** 2026-08-09
- **What:** Invite friends to this repo, then create the first private project repo and
  scaffold the workflow into it.
- **Why:** Everything so far is verified against simulated collaborators. Nothing is
  proven until real people with their own Claude Code use it at the same time.

### Onboarding checks in the journey
- **From:** pulkit, 2026-08-09
- **Why:** 84% of users who hit a blank state with no contextual help abandon in the first
  session, and 70–80% of users are lost within three days — most before any value lands.
  Forcing signup before value is "the single most expensive onboarding mistake"; over seven
  steps measurably drops conversion; over 30 minutes to value triples abandonment.
- **What:** `check_journey.py` flags flows that ask for an account before delivering
  anything, count steps to first value, and check every empty state actually helps.

### Rank the assumptions we already collect
- **From:** pulkit, 2026-08-09
- **Why:** journeys record assumptions and then treat them all alike. Assumption mapping
  ranks on two axes — how important (if wrong, does it kill us?) against how much evidence
  (do we know, or are we guessing?) — which points at the single thing worth checking.
- **What:** mark one assumption per journey as "check this before building".

### Attribute to convention, never to their omission
- **From:** pulkit, 2026-08-09
- **Why:** unsolicited help produces measurable self-threat — it challenges competence and
  autonomy, and reduces willingness to use the tool again. Same information, different
  framing, different outcome.
- **What:** "added the empty state, that's the one everyone forgets" — never "you forgot
  the empty state".

### A shipping moment
- **From:** pulkit, 2026-08-09
- **Why:** side projects have no external forcing function, so the improvement phase
  expands indefinitely and nothing ships. Perfectionism turns "onboarding emails" into "a
  full drip campaign with A/B testing".
- **What:** when the first slice is done, say so once — "that's what you called v1, ship it
  or keep going?" — and don't nag after that.

### Leave a resume point at the end of a session
- **From:** pulkit, 2026-08-09
- **Why:** coming back after a break costs "an hour or two" just rebuilding context, and
  that reload cost is a large part of why side projects die. Trained developers leave
  themselves a breadcrumb instinctively; beginners don't know to.
- **What:** at a natural stopping point, write where things are and the next concrete step.
  Not a summary — an entry point.

### Never leave it broken
- **From:** pulkit, 2026-08-09
- **Why:** ending a session mid-break means tomorrow starts with debugging rather than
  building, which is the most demoralising possible restart.
- **What:** at a stopping point, get back to something that runs and commit it — or say
  plainly that it's mid-surgery and what's half-done.

### Understand before writing code
- **From:** pulkit, 2026-08-09
- **Why:** "the best engineers write code as a last resort"; 15–30 minutes spent reading
  requirements, existing code and edge cases prevents hours of rework. Beginners start
  typing immediately, which is exactly the reflex that produces rebuilds.
- **What:** for anything non-trivial, look at what's already there and say what you found
  before changing anything.

### Commit hygiene, demonstrated not taught
- **From:** pulkit, 2026-08-09
- **Why:** the documented beginner pattern is vague messages ("update", "changes"),
  fear of committing at all, working directly on main, and committing untested work. All
  four make it impossible to go back to something that worked.
- **What:** commit in logical chunks with messages saying what and why; branch for anything
  risky. Do it visibly rather than explaining it.

### One project at a time
- **From:** pulkit, 2026-08-09
- **Why:** the multi-project trap — new projects feel exciting, so a backlog of half-built
  things accumulates and none ship. "90% done syndrome". Enforced monotasking increases the
  total number of things actually finished.
- **What:** when a new idea arrives mid-project, capture it to a someday list and keep
  going, rather than switching. Notice out loud when several things are open at once.

### Consistency over intensity
- **From:** pulkit, 2026-08-09
- **Why:** "consistency beats intensity almost every time" — a few hours regularly beats a
  twelve-hour marathon nobody returns from. The 10-minute re-engagement trick works because
  brief contact keeps the mental loop alive, so the next real session starts with context
  already loaded.
- **What:** make a short session productive rather than requiring a long one — always have
  an obvious small next step available.

---

## Semantic pass, 2026-08-09

The lexical checker finds nothing here, and says so while warning it can't see meaning.
Reading them properly:

- **"Leave a resume point"** and **"Never leave it broken"** are two halves of one moment —
  the stopping point. Build them together: get it running, commit, leave the next step
  written down. Separately they'd produce two nags at the same instant.
- **"One project at a time"** and **"Consistency over intensity"** and **"A shipping
  moment"** all attack the same failure — things not getting finished — from different
  angles (don't start more, keep the loop alive, notice when v1 is done). Worth designing
  as one behaviour rather than three, or they'll compete for the same pause in the
  conversation.
- **"Understand before writing code"** and **"Commit hygiene"** are the only two that are
  purely about the agent working visibly rather than saying anything. Cheapest to add and
  least likely to annoy.

Nothing contradicts anything else. The real risk across the whole list is **volume**: ten
new behaviours, each individually justified, together adding up to an assistant that
comments constantly. Whatever gets built needs one shared budget for how often it speaks,
not ten independent ones.


### Notice the prompting rabbit hole and break it
- **From:** pulkit, 2026-08-09
- **Why:** the signature failure of a beginner's first session. They prompt, it's wrong,
  they rephrase, it's wrong differently, they rephrase again — "the feature that should
  have taken minutes eats most of your afternoon." It's sticky because "you always feel the
  end is within reach, and stopping feels dangerous." Novices are documented as iterating
  on prompts without converging; experts decompose instead.
- **What:** after two or three failed rounds on the same thing, stop and say so. Go back to
  the last working state, break the problem smaller, and attack one piece. The signal is
  repetition without new information — "still not working", "that's not what I meant".

### Keep save points so there's always a way back
- **From:** pulkit, 2026-08-09
- **Why:** the top practitioner advice for exactly this failure is "save each point where
  it got things right, so if something goes wrong you can go back to the last working
  version." Beginners have one enormous uncommitted blob instead, so the only way back is
  starting over.
- **What:** commit automatically whenever something demonstrably works, with a real
  message. Then "put it back how it was an hour ago" is always available, which is what
  makes experimenting safe.

### Get the actual error, don't guess from "it's not working"
- **From:** pulkit, 2026-08-09
- **Why:** a beginner's entire bug report is "it's not working" — they don't know that the
  red text matters, or which part of it. Guessing from that is what starts the rabbit hole,
  and guessing changes several files at once, which is what adds the second bug.
- **What:** ask for what's actually on screen before changing anything. One question, and
  it teaches the habit by needing it.

### Decompose out loud, build one piece
- **From:** pulkit, 2026-08-09
- **Why:** novices "have difficulty identifying boundaries for components of their plans
  and underspecify their plans" — the documented skill gap is decomposition, not syntax. A
  senior turns "an app for tracking workouts with friends" into "first: record one workout
  and still see it tomorrow." A beginner asks for all of it at once and gets 800 lines that
  can't be judged.
- **What:** say the breakdown in one line before starting, build the first piece, show it
  working, then continue. The beginner absorbs the decomposition by watching it happen.

### Name the stage, so effort goes to the right thing
- **From:** pulkit, 2026-08-09
- **Why:** experienced people make stage-dependent trade-offs — speed over polish before
  product-market fit, quality over speed once there's traction. Beginners don't know which
  stage they're in, so they polish a thing nobody has used, or ship something fragile to
  people who depend on it.
- **What:** one line when it's relevant — "nobody's used this yet, so rough is fine; worry
  about that when someone complains."

### Say the downside of each choice
- **From:** pulkit, 2026-08-09
- **Why:** the clearest tell of an experienced product person is that they name the cost of
  the path they chose. Juniors present a decision as if it were free. Hearing "and the
  downside is…" repeatedly is how someone learns that every choice has one.
- **What:** whenever a real choice is made, one clause on what it costs. Not a paragraph.

### Write the words in the interface properly, silently
- **From:** pulkit, 2026-08-09
- **Why:** the highest-value free win available. "Submit" versus a button that says what it
  does can double or triple conversion; "Invalid input" versus "Please enter your email as
  name@example.com" is the difference between a user fixing their mistake and abandoning
  the form. The pervasive beginner mistake is generic template copy — every button
  "Submit", every error "An error occurred" — plus leaked internal jargon.
- **What:** the agent writes this text anyway, so write it well by default. Users scan
  rather than read, so front-load the meaningful words; if it can't be understood in three
  seconds it's too complex. Never mention doing it.

### Don't collect data you don't need, and say so
- **From:** pulkit, 2026-08-09
- **Why:** GDPR has **no revenue or size threshold** for its core obligations, and a single
  developer paid $50,000 under COPPA for collecting children's email addresses. Beginners
  have no idea any of this applies to them. The common failure is collecting "just in
  case" — full location, phone, birthday — when only an email is needed.
- **What:** the agent designs the schema anyway, so default to collecting the minimum. If a
  feature starts storing personal data, say once what's being collected and that anything
  public-facing will need a privacy notice. Not legal advice — just don't let them walk
  into it unaware.

### Derive a smoke test from the journey's happy path
- **From:** pulkit, 2026-08-09
- **Why:** the standard pre-release check is five to ten manual steps — open it, do the one
  main thing, confirm nothing crashed — and it's exactly right for a solo builder with no
  test suite. Beginners either test nothing or think they need a full testing setup.
- **What:** the journey's happy path already is that list. Generate it and walk it before
  anyone else sees the thing.

### Close the loop when someone reports something
- **From:** pulkit, 2026-08-09
- **Why:** "when you act on feedback but don't update the user, they feel ignored and bail
  — one-way feedback erodes trust." Beginners fix the bug and never reply, losing the
  person anyway. Early on, response speed matters more than the fix.
- **What:** when a reported problem gets fixed, note who reported it so they can be told.
  One line, and it's the difference between an early user who stays and one who doesn't.

### The record is also evidence they're getting somewhere
- **From:** pulkit, 2026-08-09
- **Why:** the recommended counter to the imposter feeling that kills side projects is a
  "brag document" — a running log of what was actually accomplished, so there's concrete
  evidence when self-doubt arrives. `JOURNAL.md` is already that, by accident.
- **What:** when someone sounds discouraged, that's the moment the history is worth
  surfacing — "three weeks ago none of this existed". Only then; never as a progress
  report.
