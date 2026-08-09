# Journal — coordination-module

The running conversation of the project, so that everyone's Claude Code starts from the
same understanding. Read this first in a new session — it's the "what happened while I
was away" file.

`CONTEXT.md` holds settled conclusions. This holds the **reasoning and the arguments**,
including the ones still in progress. Both matter: a conclusion without its reasoning
gets reversed by accident, and a debate nobody recorded gets restarted from zero.

## Open threads

Questions actively being argued. Keep the positions and who holds them — an unresolved
debate is the single most valuable thing to hand another person, because it's where they
can actually contribute. Move a thread to `CONTEXT.md` decisions once it settles, leaving
a one-line pointer here.

_None open._

Recently settled: **SDLC toolkit vs spec-kit** — resolved 2026-08-09 in favour of a
journey-first `shape` skill covering the front half only; spec-kit not adopted. Reasoning
and the research behind it are in `CONTEXT.md` decisions and the log entry below.

## Log

Newest at the bottom. One short entry per meaningful exchange — what was discussed, what
options were weighed, what was chosen or left open. Include the alternatives that were
rejected in passing; those are the ones people otherwise re-propose.

Don't transcribe everything. Write what someone joining tomorrow would need in order to
disagree intelligently.

### 2026-08-09 — how should a group of friends collaborate at all?  (pulkit)
Starting point: several people each with their own Claude Code, wanting to build apps
together and spread work across everyone's token budget. Considered GitHub Projects boards
and a formal PR review process; rejected the ceremony in favour of plain markdown files
plus short-lived branches, on the grounds that a friend should be able to take part without
learning a process first. Branches kept purely as a collision guard, not as a review gate.

### 2026-08-09 — where should the workflow rules live?  (pulkit)
Weighed a personal skill vs a per-repo `CLAUDE.md`. Landed on both, with different jobs:
`CLAUDE.md` is portable and auto-loads for anyone who clones, so the repo is self-teaching;
the skill is the scaffolding shortcut and lives in a meta-repo so it can be versioned and
shared. The deciding factor was that friends should need zero setup beyond cloning.

### 2026-08-09 — dashboard interactivity, and then hosting  (pulkit)
Wanted clickable actions on the dashboard. Traced through what "live" actually requires —
hosted API key, backend, billing — and chose static instead, with the page telling people
which word to type. Then asked whether Pages could be restricted to just the group; found
it cannot on a free plan, which redirected the whole approach to private repos + native
markdown rendering. Both outcomes recorded in `CONTEXT.md`.

### 2026-08-09 — what actually makes contexts converge  (pulkit)
The real goal named explicitly: it should feel like one agent that has worked continuously
and happens to talk to several people. Traced this session's own discussion through the
file set and found conclusions were captured but *reasoning* was not — so a decision could
be reversed by accident and rejected ideas would be re-proposed forever. That produced
`JOURNAL.md` (reasoning + open threads) and the rule that triage must write reject
reasoning into `CONTEXT.md`, since `PRIORITIES.md` is overwritten every run.

### 2026-08-09 — stress test with four simulated collaborators  (pulkit)
Simulated four clones with overlapping and offset work rather than assuming the design
held. Found three real bugs — two of which worked fine at two people and broke badly at
four — and one accepted tradeoff needing a detector. All four written up in the Gotchas
section of `CONTEXT.md`. Worth repeating this exercise after any change to merge or
publish logic.

### 2026-08-09 — published, and this repo became its own first user  (pulkit)
Rewrote git history to a GitHub noreply identity before publishing (the old author email
embedded a work-machine hostname), then published as a public repo. Verified the actual
friend path: fresh clone → `update_skill.sh` → both skills installed with executable bits
intact. Then ran the workflow on this repo itself, and seeded these files with the real
history above — which is both dogfooding and the first genuine test of whether the record
is usable by someone who wasn't in the conversation.

### 2026-08-09 — the trigger words were the interface, and that was a bug  (pulkit)
Noticed that the design leaned on people typing exact words. Real conversation doesn't
work that way: someone says "let's do the CSV export" and means a claim, or finishes work
and never says "done". Weighed three options — silent auto-capture (surprising, erodes
trust), keep requiring commands (friction, guarantees the record rots), or infer intent
and confirm. Chose the third, split by blast radius: additive record-only edits happen
silently with a one-line mention, anything other people will see gets a one-line
confirmation first. Added explicit anti-nag rules, since the obvious failure of this
feature is an assistant that asks about everything and gets tuned out. The structural
insight was that these rules belong in `CLAUDE.md` rather than `SKILL.md`, because
`CLAUDE.md` loads every session while a skill only fires when its description matches.

### 2026-08-09 — journeys, and the questions people can't answer  (pulkit)
Settled the SDLC thread by reframing it: the **user journey**, not the spec, is the primary
artifact. Rejected spec-kit as a dependency — it starts from writing a spec, which is the
blank page that stops beginners, so journey-first makes it unnecessary rather than
something to bridge to. Rejected the full cycle in favour of the front half, on the
grounds that Claude Code already covers testing and review and that equal-depth phases are
what made BMAD unusable.

Grounded the method in existing practice rather than inventing one: Patton's story mapping
for the backbone and walking skeleton, job stories instead of personas (personas don't
explain causality and invite invented demographics), Hurff's UI Stack plus three Nielsen
heuristics as the per-step checklist, happy → alternate → exception as the *order* of
questioning, and Example Mapping to turn the map into rules. Cut as enterprise overhead:
emotion rows, personas with photos, "thoughts" rows sourced from research nobody did.

Mermaid's `journey` type was investigated and rejected on a hard fact: its grammar has no
branching, so it structurally cannot express the failure states the exercise exists to
find. `flowchart TD` instead — happy path as trunk, failures as labelled branches, which
makes a trunk-with-no-branches visibly unfinished.

Three refinements came from thinking about how this fails in practice rather than how it
works on paper:

- **Never announce the process.** Naming phases turns an exciting idea into paperwork.
  Ask "who opens this, and what just happened to them?" rather than "let's begin the
  discovery phase" — same information, completely different response.
- **A question someone can't answer is worse than one you answer for them.** Added an
  escalation ladder — ask, then offer options to react to, then propose a default and mark
  it as an *assumption* rather than a decision. Frustrating someone in a domain they don't
  know makes everything after it shallow.
- **Show the diagram as it grows**, in the side panel, drafting a wrong first version
  deliberately: correcting a sketch is far easier than producing one from nothing. Also
  generalised to `team-collab` — files changing silently on disk is invisible work, so
  anything worth reading gets opened rather than just mentioned.

### 2026-08-09 — cut roughly half of it  (pulkit)
pulkit pushed hard on a question the build had been dodging: why would an impatient
beginner install this at all? Explicitly ruled out "it improves quality" and "it boosts
productivity" as answers nobody acts on. The honest conclusion was that he wouldn't — he'd
never open a dashboard, never type `triage`, never learn a command.

So the dashboard (728 lines), `PRIORITIES.md`, the triage flow and the whole command table
were deleted — about 1,100 lines. Every one of them required the user to do something
extra, which is the single reliable way to guarantee a tool goes unused. Ranking five ideas
for four friends is also a ten-second job done in your head.

The pitch inverted: **memory, not coordination.** "Claude Code forgets your project between
sessions" is a pain felt daily, alone, on day one — whereas coordination needs friends,
invites and weeks before it pays off, and the old install was six steps before anything
good happened. Coordination is now a side effect of the notes living in a shared repo.

`shape` changed from interviewing to drafting: write the whole flow from one sentence, show
it, ask "what's wrong?". Correcting a draft costs seconds. The refinement pulkit added is
that the draft must be a *mirror, not a substitute* — extend only where convention makes it
obvious (a list implies an empty state), and leave genuine product decisions visibly
guessed rather than quietly invented, or the person nods along at something they never
thought about. If they don't know, they won't answer, and that's fine.

Also added cross-project preferences in `~/.claude/CLAUDE.md`, so recurring habits stop
being relearned per project — asked once before first use, since it changes behaviour
everywhere.

Two real bugs found while doing this. The dashboard's mermaid never actually rendered:
`startOnLoad` hooks `DOMContentLoaded`, which has already fired by the time an `await
import()` resolves, so nothing drew — an earlier claim that it was "verified" had only
checked the HTML contained a script tag, not that a diagram appeared. And emptying
`GENERATED_FILES` broke `publish.sh` outright, because `set -u` errors on expanding an
empty array in macOS bash 3.2; the fix was deleting the mechanism rather than patching it.

### 2026-08-09 — researched what actually goes wrong, then built against it  (pulkit)
Stopped guessing at features and looked for evidence. The numbers reframed the priorities:
**63% of people vibe coding have no coding background**, **45–62% of AI-generated code
ships with vulnerabilities**, privilege-escalation paths are up 322%, and by mid-2026 about
**8,000 of ~10,000 AI-built startups had needed a rebuild costing $50k–$500k**. Rescue
engineers report the same seven patterns: exposed keys, fake auth, zero error handling,
race conditions, broken payments, unvalidated inputs, unmaintainable code.

The mechanism named in the research is a **verification gap** — novices can't detect errors
in what they accept, so the checks an experienced developer makes by reflex never happen.
That shifted the emphasis: we'd been optimising for "did we build the right thing" when the
larger risk for this user is "did we ship something dangerous", with no way to know.

Built three things against that. A **narrow pre-ship check** — real credentials, tracked
`.env`, Supabase tables without row-level security (the exact mistake that leaked 1.5M
tokens in Feb 2026), unfiltered drop/truncate, always-true auth — and nothing else, because
a checker that cries wolf gets ignored and then the real warning is too. Verified: catches
all five, zero false positives on correct code, and stays quiet on placeholders.

**Plain-English change summaries**, aimed squarely at the verification gap. A non-coder
can't review a diff, but they can review "anyone with the link can now read every entry."
The script surfaces signals; the sentence is the review.

**One-way-door flagging.** Early product decisions are path-dependent, and knowing which
choices are permanent — data model, accounts or not, single vs shared — is precisely the
experience a beginner lacks. Flag in one line, never gate.

Also discovered that Claude Code **hooks** are the mechanism pulkit had been describing all
along: deterministic, run unasked, cannot be talked around by reasoning the way `CLAUDE.md`
can. The guard installs as a hook, backs up existing settings, touches only its own entry,
and uninstalls cleanly — pulkit's constraint was that people grow, so the training wheels
must come off without hunting through config.

Separately: the rewrite had **silently dropped the GitHub Issues layer** while leaving the
decision standing in `CONTEXT.md` — exactly the stale-memory failure this tool exists to
prevent, caused by me. Restored, but without the `sync` command: ideas fold in during the
pull that already happens. The capability was worth keeping; the command was not.

