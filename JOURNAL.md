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

### Should we build a full SDLC toolkit, or bridge to GitHub spec-kit?  (opened by pulkit, 2026-08-09)

The idea: extend beyond coordination into a complete toolkit for the whole product
development cycle — planning, specs, architecture, task breakdown, implementation,
testing, deployment — aimed at people new to software who don't yet know what good process
looks like.

**Research done before deciding (so nobody has to redo it):**

- **[GitHub spec-kit](https://github.com/github/spec-kit) — 126k stars, GitHub-official,
  works with 30+ agents including Claude Code.** Provides exactly this lifecycle:
  `constitution → specify → clarify → plan → tasks → implement → analyze → converge`.
  Learning curve reported as 1–2 days.
- **[BMAD-METHOD v4](https://bmadcodes.com/bmad-method/)** — agent personas (Analyst, PM,
  Architect, Dev, QA) with structured handoffs. Criticized for a ~2-month learning curve
  and heavy token cost; one benchmark clocked a CRM dashboard at 5.5 hours with BMAD vs
  12 minutes with a lightweight alternative. Called overkill for small tasks.
- **OpenSpec** — lightweight, but its dominant community complaint is spec drift: specs
  "keep drifting until you have duplication and contradictions."
- **Agent OS, Kiro** — similar space, multi-agent orchestration.
- **Anthropic's official marketplace** has no SDLC plugin — only a document suite, example
  skills, and an API-docs skill. Claude Code's built-in plan mode covers some of this.

**Two observations that shape the argument:**

1. The documented top failure of the spec-driven tools — drift into duplication and
   contradictions — is precisely what this module already detects
   (`check_collisions.py`, `CONTEXT.md`, `JOURNAL.md`).
2. Every one of these frameworks assumes **one** developer orchestrating agents. None
   handle several people each running their own agent. That's this module's actual
   differentiator, and rebuilding a spec pipeline would trade a unique asset for a worse
   copy of a 126k-star tool.

- **pulkit:** wants the full cycle covered so beginners have good defaults, and expects it
  to be "a lot of small small things."
- **Counter-position:** don't rebuild. Bridge to spec-kit for the per-feature lifecycle and
  build only the thin layer connecting it to the coordination files, plus 2–3 skills
  filling genuine gaps. Also: "a lot of small skills" is a known hazard — several tiny
  skills with similar descriptions mis-trigger against each other, which already came up
  over the dashboard buttons.
- **Leaning (not decided):** thin bridge, teaching-oriented so it explains *why* each step
  matters, first cut 3–4 skills covering the biggest gaps.
- **Still unresolved:** whether to take a dependency on spec-kit at all, and which gaps
  are genuinely worth a skill. Deferred deliberately — ship and actually use the
  coordination tool first, then decide from real experience rather than speculation.

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

