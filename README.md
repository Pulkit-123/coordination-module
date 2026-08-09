# Coordination Module

> **New here? Read [GETTING-STARTED.md](GETTING-STARTED.md) instead.** It's a plain-language
> walkthrough — install, first project, and daily use — with no jargon. This page is the
> technical overview.

Two Claude Code skills for a small group building a project together, where **each person
runs their own Claude Code**.

The problem it solves isn't writing code — it's that each person's chat history is
private. Reasoning that happened in one person's conversation is invisible to everyone
else, so the group slowly diverges: the same idea gets proposed twice, a decision made on
Monday gets contradicted on Tuesday, and two people build the same feature without
noticing.

The fix is plain markdown files in the project repo. Every Claude Code that opens the repo
reads them automatically, so what one person works out becomes what everyone knows.

No server, no API keys, no build step, no accounts. Plain files and plain git.

## What you get

**`team-collab`** — sets up and runs the workflow:

| File | What it holds |
|---|---|
| `CLAUDE.md` | The workflow brief, auto-loaded by anyone's Claude Code |
| `JOURNAL.md` | The running conversation — reasoning, and arguments still open |
| `CONTEXT.md` | Scope, decisions with reasoning, gotchas, why ideas were declined |
| `IDEAS.md` | Append-only backlog, attributed |
| `TASKS.md` | Who is building what, right now |
| `PRIORITIES.md` | Ranked build order (generated) |
| `journeys/*.md` | One per feature: the flow, the spec, open questions |
| `dashboard.html` | Static single-page view (generated) |

**`shape`** — works out *what* to build, before any code. Walks through the user's flow
step by step, turning it into a mermaid diagram, acceptance rules and a first slice in
`journeys/<slug>.md`. Built on established practice (Patton's story mapping, job stories,
Hurff's UI Stack, Example Mapping) rather than an invented methodology.

**`why`** — answers "why was this rejected / decided / dropped?" by tracing those files
*and their git history*, including reasoning that was later edited out or deleted.

## Install

```bash
git clone https://github.com/Pulkit-123/coordination-module.git
cd coordination-module && bash skills/team-collab/scripts/update_skill.sh
```

That copies both skills into `~/.claude/skills/`. Re-run it any time to update.

## Use

Open your project in Claude Code and type `setup team`. After that, people just type
what they want — no commands to memorize:

| Type this | What happens |
|---|---|
| `idea: dark mode for settings` | Added to the backlog under your name |
| `triage` | Re-ranks everything, flags clashes, asks what's unclear |
| `claim csv export` | Marks you as working on it, creates the branch |
| `done` | Moves your task to finished |
| `status` / `catch me up` | What changed, who's on what, what needs your view |
| `why was offline mode dropped?` | Traces the decision and its reasoning |
| `help me plan the export feature` | Shapes it into a journey, spec and tasks |

## How access works

This tooling repo is public — anyone can use it. Your **project** repo is separate and can
be private. The skills run locally under your own git credentials, so whether you can read
or push is decided entirely by that project repo's own collaborator settings. There's no
account, no service, and nothing here ever sees your project's contents.

Private repos with unlimited collaborators are free on GitHub, and markdown renders
natively in the web UI — so a private repo already gives you a mobile-friendly, access-
controlled view of the coordination files with no hosting at all.

## Notes from building it

`PLAN.md` has the design rationale and the failure modes found while stress-testing four
simulated collaborators — including three real bugs, two of which broke the workflow
entirely at four people while working fine at two. Worth reading before changing how
merging or publishing works.

Two things to know if you extend it:

- **`merge=union` on the append-only files is load-bearing.** Without it, two people
  adding an idea at the same moment collide at end-of-file and git silently keeps one.
- **Union-merge hides collisions in exchange.** Git reports success to everyone and never
  flags the clash, so `check_collisions.py` exists to find them. It's lexical only —
  semantically-identical ideas and scope drift need the model's judgment, and the skill
  instructs it accordingly.
