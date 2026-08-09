# Coordination Module — Plan

## Problem
Building multiple apps in parallel, want friends (each running their own Claude Code)
to collaborate: propose/prioritize ideas, pick up tasks, and build parts of the same
project — without hitting one person's token limits, and without re-explaining the
workflow every time a new project starts.

## Architecture — 3 layers

1. **This repo (`Coordination Module`) = the meta-repo.**
   Source of truth for the *tooling*, not any single app. Holds the `team-collab`
   skill and the templates it scaffolds. Versioned and updated over time as the
   workflow needs change (new fields, new commands, etc.).

2. **Each app = its own separate GitHub repo.**
   Friends added as direct collaborators (push access) — trusted group, no fork
   workflow needed. Short-lived branches recommended per feature purely as a
   collision guard (so two people's Claude Code don't overwrite the same file),
   not a formal review gate.

3. **The `team-collab` skill** (installed locally via skill-creator, pulls templates
   from this meta-repo) scaffolds and maintains the per-project files below.

## The real goal: one shared mind, several people

The target is that it *feels like a single agent* that has worked on the project
continuously and happens to talk to several people — not N agents each holding a
fraction. The thing preventing that is that each person's chat history is private, so
reasoning that happened in one conversation is invisible to everyone else.

Capture is therefore the mechanism, not bookkeeping. Note the split:

- **State** — what exists and who's on it (`IDEAS.md`, `TASKS.md`)
- **Conclusions** — what's settled and why, incl. why things were rejected (`CONTEXT.md`)
- **Reasoning** — the discussion itself and arguments still in flight (`JOURNAL.md`)

The third is the one that normally evaporates, and it's what someone needs in order to
disagree intelligently rather than re-tread settled ground. Every session starts with a
catch-up read of those files so nobody arrives cold.

## Per-project files (scaffolded by `team-collab init`)

- **`JOURNAL.md`** — running conversation: reasoning, options weighed, and open threads
  with each person's position. Read at session start to catch up.
- **`CONTEXT.md`** — settled understanding: decisions with reasoning, gotchas and dead
  ends, and *why ideas were rejected or deprioritized* (that last one must live here
  because `PRIORITIES.md` is overwritten on every triage).
- **`.gitattributes`** — sets `merge=union` on the append-only files. Verified necessary:
  without it, two people adding an idea simultaneously collide at end-of-file and git's
  rebase silently keeps only one.
- **`CLAUDE.md`** — portable, travels with the repo. Any Claude Code instance that
  opens the project (yours or a friend's) auto-loads it and already knows the
  workflow — no re-explaining needed. This is the actual source of truth for how
  to collaborate on *that* project.
- **`IDEAS.md`** — append-only backlog. Anyone adds an idea with name + date.
  Append-only keeps direct-commit conflict risk low.
- **`TASKS.md`** — who's actively building what, so work doesn't collide.
- **`PRIORITIES.md`** — output of the triage pass: ranked build order, flagged
  duplicate/contradicting ideas, rejects with reasoning, clarifying questions for
  ideas that need more detail.
- **`dashboard.html`** — static, generated snapshot of the three files above
  (ideas / tasks / priorities). Not live. Optionally published via free GitHub
  Pages so anyone has a read-only shareable link without cloning.

## Skill commands (`team-collab`)

- `init` — scaffold the four files + dashboard into the current repo. Skips files
  that already exist (safe to rerun).
- `triage` — read `IDEAS.md`, write a ranked build order + conflict flags + reject
  reasoning + clarifying questions into `PRIORITIES.md`.
- `dashboard` — regenerate `dashboard.html` from the current state of the three
  markdown files.
- `update` — explicit, manual pull of the latest templates/skill logic from this
  meta-repo. Not automatic on every invocation (predictability > silent drift).

## Key decision: GitHub Issues as the discussion layer

Markdown is a fine backlog but a bad conversation — you can't reply to one line of a
file, and simultaneous edits conflict. GitHub Issues gives threading, 👍-as-voting,
notifications, and phone access for free, so:

- An idea can start as an issue (labelled `idea`) **or** as an `IDEAS.md` entry.
- `team-collab sync` folds issues into `IDEAS.md`, matching on issue number so reruns
  are safe. Triage then weighs reaction counts and comment threads, and treats closed
  issues as already-decided rejects.
- The dashboard links to a prefilled "post an idea" issue form.

## Key decision: hosting and access control

**No GitHub Pages.** Pages access control is Enterprise Cloud only — on Free/Pro any
published Pages site is world-readable, even when built from a private repo. There is no
free way to publish a restricted dashboard.

Not needed anyway: **private repo + collaborators is free and unlimited**, and the
markdown files render natively on github.com — formatted, mobile-friendly, and gated by
the repo's own access rules. That *is* the private shareable dashboard, at zero cost.
`dashboard.html` is the single-page local view after a `git pull`.

## Key decision: dashboard interactivity

The "click a button and Claude reads/clarifies ideas" button on `dashboard.html`
is **not a live API call**. A real live version would need a hosted API key,
backend, and billing — too much footprint for what this needs to be. Instead the
button is a static instruction: *"run `team-collab triage` in your Claude Code."*
Whoever runs it updates the markdown + regenerates the dashboard + pushes; viewers
see the update on next pull/page load. This satisfies "not live, refreshes
manually or periodically" without any hosted infrastructure.

## Open / future (not priority now)

- True live/real-time coordination (would need a hosted backend — explicitly
  deferred by the user as "not a priority").
- Auto-update of the skill on every invocation (deferred in favor of explicit
  `update` command).

## One-word chat commands

People shouldn't need to remember file names or markdown format to take part — that
friction is what stops friends contributing. The dashboard lists these; the skill
triggers on the bare words: `idea: <x>`, `triage`, `claim <x>`, `done`, `status`,
`refresh`, `sync`.

## Status
- [x] Architecture agreed
- [x] `team-collab` skill built — init / triage / dashboard / sync / update + quick commands
- [x] Dashboard generator tested (escaping, tables, remote/no-remote link cases)
- [x] Verified: concurrent two-clone publish keeps both contributions
- [x] Verified: fresh clone receives CLAUDE.md + .gitattributes (friends get the brief
      and the merge protection)
- [ ] First real project scaffolded with it
- [ ] GitHub repo(s) created, friends added as collaborators — **nothing created yet**
