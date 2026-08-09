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

## Per-project files (scaffolded by `team-collab init`)

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

## Status
- [x] Architecture agreed
- [ ] `team-collab` skill built (via skill-creator)
- [ ] First real project scaffolded with it
- [ ] GitHub repo(s) created, friends added as collaborators
