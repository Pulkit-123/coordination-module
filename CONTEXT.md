# Shared understanding — coordination-module

What the group has figured out. Every person's Claude Code reads this on opening the repo,
so knowledge one person gained becomes knowledge everyone has — that's the whole point.

`IDEAS.md` is what we might build. This is what we now know. Append here whenever
something is learned the hard way, decided with reasoning, or would make a newcomer say
"I wish someone had told me."

**Keep entries short and dated.** Delete or amend entries that turn out to be wrong —
stale context is worse than none, because people act on it confidently.

## Scope

**coordination-module is** a memory for a project, so Claude Code stops forgetting it
between sessions: decisions and their reasoning, dead ends already hit, and — if more than
one person is involved — who is doing what. Plus `shape`, which drafts a plan before
building so the thing doesn't get built twice. All in plain markdown that any Claude Code
opening the repo reads automatically.

**The user does nothing to maintain it.** That constraint outranks every feature idea: a
dashboard, a ranking command and a list of words to type were all built and then deleted
because each one required the person to do something extra.

**coordination-module is not** a dashboard, a project-management tool, a hosted service, a
chat tool, or a replacement for GitHub Issues. It covers only the front half of the
development cycle — testing, review and deployment are left to Claude Code. And it is not
worth installing for a one-afternoon script.

_Scope revised 2026-08-09 — it previously excluded spec work entirely. See the decision
below; the earlier wording is in git history._

The guiding constraint is footprint: plain files, plain git, no server, no API keys, no
build step. A friend should clone and be productive in a minute. Reject anything that
breaks that unless the payoff is very large.

## Decisions

Things settled, with the reasoning — so they don't get relitigated every month.

### ~~2026-08-09 — dashboard is a static snapshot, not a live page~~ (SUPERSEDED)
_The dashboard was deleted entirely later the same day — nobody opens one. Kept for
the reasoning about live pages, which still stands if it ever comes back._

- **Chose:** `dashboard.html` regenerated locally from the markdown files, with buttons
  that tell you which word to type into your own Claude Code
- **Over:** a live page whose buttons call an LLM API directly
- **Because:** live means a hosted API key, a backend, and per-call billing — a large jump
  in cost, complexity, and risk for a group who are all already running Claude Code
  locally. The static page gets the same outcome with none of that.
- **By:** pulkit

### 2026-08-09 — no GitHub Pages; private repo instead
- **Chose:** no Pages at all; view coordination files natively on github.com, and open
  `dashboard.html` locally after a pull
- **Over:** publishing the dashboard via GitHub Pages
- **Because:** Pages access control is GitHub Enterprise Cloud only. On Free and Pro
  *every* Pages site is world-readable, even when built from a private repo — there is no
  free way to restrict one. And it isn't needed: private repos with unlimited
  collaborators are free, and markdown renders natively in the GitHub web UI, which is
  already mobile-friendly and gated by the repo's own permissions.
- **By:** pulkit

### 2026-08-09 — GitHub Issues as the discussion layer (amended same day)
- **Chose:** ideas can start as an `idea`-labelled issue; they get folded into `IDEAS.md`
  automatically during the session-start pull
- **Over:** building comment/threading features into the dashboard; and over the original
  `sync` command, which was dropped — it needed the `gh` CLI, a remembered command, and
  manual labelling, which is the same friction that killed `triage`. The capability was
  worth keeping, the command was not.
- **Because:** markdown is a good backlog but a bad conversation — you can't reply to one
  line of a file, and simultaneous edits collide. Issues already give threading,
  👍-as-voting, notifications, and phone access, for free.
- **By:** pulkit

### 2026-08-09 — tooling repo public, project repos private
- **Chose:** this repo public; each actual app in its own private repo
- **Over:** keeping everything private, or everything public
- **Because:** the tooling is generic and useful to other teams, and contains no project
  data. Access control comes free: the skills run locally under each person's own git
  credentials, so a non-collaborator's push simply fails. No permission layer to build.
- **By:** pulkit

### 2026-08-09 — `merge=union` on append-only files
- **Chose:** `.gitattributes` sets `merge=union` for `IDEAS.md`, `CONTEXT.md`,
  `JOURNAL.md`, `TASKS.md`
- **Over:** letting git conflict normally
- **Because:** two people appending at the same moment collide at end-of-file and git's
  rebase silently keeps only one. Verified, not theoretical — see Gotchas. Losing
  someone's contribution is the fastest way to make them stop contributing.
- **By:** pulkit

### ~~2026-08-09 — generated files are rebuilt, never merged~~ (SUPERSEDED)
_No generated files remain. The rebase-conflict handling in `publish.sh` still exists
and the failure it fixed is real — see Gotchas — so don't reintroduce generated files
without it._

- **Chose:** `publish.sh` auto-resolves conflicts in `dashboard.html` and `PRIORITIES.md`
  by taking either side and regenerating
- **Over:** treating them like any other file
- **Because:** they differ on every machine, so they conflicted on every concurrent push
  and deadlocked everyone but the first pusher. Rebuilding always yields the correct
  result, so a human should never be asked to resolve one.
- **By:** pulkit

### 2026-08-09 — intent recognition over remembered commands
- **Chose:** read intent from ordinary conversation and act; the trigger-word list was
  dropped altogether when the command surface was deleted
- **Over:** requiring people to type `claim`, `done`, `idea:` etc.
- **Because:** anyone who has to remember a magic word won't, and the record rots — the
  exact failure the module exists to prevent. Crucially the rules live in `CLAUDE.md`,
  not just `SKILL.md`: skills only activate when their description matches, so "I'll take
  the CSV export" might never reach the skill at all, whereas `CLAUDE.md` is auto-loaded
  every session regardless of phrasing.
- **By:** pulkit

### 2026-08-09 — ask before anything other people see; act silently otherwise
- **Chose:** record ideas/gotchas/decisions immediately and mention it in one line; ask a
  short confirming question before claiming, marking done/blocked, or pushing
- **Over:** asking about everything, or asking about nothing
- **Because:** the split is blast radius. A wrong idea entry is trivially corrected, so
  asking is pure friction. A wrong claim makes someone else skip work that isn't
  happening, and a wrong "done" makes the group believe a feature exists — those cost
  other people's time. Paired with anti-nag rules (never ask twice, batch at natural
  pauses, stop if told to), because an assistant that prompts constantly gets ignored and
  the record rots anyway.
- **By:** pulkit

### 2026-08-09 — scope widened to cover shaping work, and spec-kit not adopted
- **Chose:** add a `shape` skill covering discovery → user journey → spec → first slice,
  in this repo, reversing "not a spec-driven development framework"
- **Over:** (a) leaving scope as it was, (b) depending on GitHub spec-kit, (c) covering the
  full cycle including test and deploy
- **Because:** the front half is where quality is actually lost — getting the idea out of
  someone's head is the hard part, and Claude Code already handles the back half well.
  spec-kit was not adopted because journey-first makes it unnecessary rather than something
  to bridge to: it starts from writing a spec, which is exactly the blank page that stops
  beginners. The full cycle was rejected as the BMAD failure mode — a ~2-month learning
  curve for a tool meant to save time.
- **By:** pulkit

### 2026-08-09 — user journey as the primary artifact, not the spec
- **Chose:** a mermaid `flowchart` per feature in `journeys/<slug>.md`, with the spec
  derived from it
- **Over:** a written spec as the starting point, and over mermaid's `journey` type
- **Because:** "walk me through what the person does" is answerable by anyone; "write a
  spec" is not. Mermaid's `journey` type was rejected on inspection — its grammar is only
  `title`, `section`, `Task: score: actor`, so it **cannot branch at all** and therefore
  can't express the error and empty states the whole exercise exists to surface. It also
  only adds an emotion score, which is the one dimension deliberately cut.
- **By:** pulkit

### 2026-08-09 — dashboard may load mermaid from a CDN
- **Chose:** pull the mermaid renderer from a CDN, only on pages that contain a diagram,
  with the diagram source left visible as the offline fallback
- **Over:** strict "no external requests", or vendoring ~2.5MB of JS into the repo
- **Because:** a render-only library with no keys, no backend and no cost is a different
  risk from the API-key-plus-billing case the original rule was written against. It
  degrades cleanly: offline you see readable source, not a broken page. Pages without a
  diagram still get no script at all.
- **By:** pulkit

### 2026-08-09 — deleted the dashboard, triage and the command list
- **Chose:** remove `dashboard.html`, `PRIORITIES.md`, the `triage` command and the table
  of words to type; keep only what the agent maintains silently
- **Over:** keeping them and making them nicer
- **Because:** every one of them required the user to do something extra — open a page,
  run a command, remember a word. That is the one thing an impatient person will never do,
  so those features were never going to be used regardless of quality. Ranking five ideas
  for four friends is also something you do in your head in ten seconds. ~1,100 lines
  removed.
- **By:** pulkit

### 2026-08-09 — the pitch is memory, not coordination
- **Chose:** lead with "Claude Code forgets your project between sessions; this fixes it"
- **Over:** leading with team coordination
- **Because:** coordination needs friends, invitations and weeks before any payoff, and the
  old install was six steps before anything good happened. The repetition problem is felt
  daily by one person alone, on day one. Coordination is then a side effect of the notes
  living in a shared repo, rather than something to sell.
- **By:** pulkit

### 2026-08-09 — draft the plan instead of interviewing
- **Chose:** `shape` writes the whole journey from one sentence using conventional
  defaults, shows it, and asks "what's wrong?"
- **Over:** asking a sequence of questions per step
- **Because:** correcting a draft costs seconds; producing one from nothing costs real
  effort and stalls beginners. Assumptions must be written *specifically* — "anyone with
  the link can view, no account" gets corrected instantly, "standard permissions" gets
  rubber-stamped — since that is what keeps drafting honest without adding questions.
- **By:** pulkit

### 2026-08-09 — guard the things that can't be undone
- **Chose:** a narrow pre-ship check (real credentials, tracked `.env`, Supabase without
  RLS, unfiltered drop/truncate, always-true auth), offered as a reversible hook
- **Over:** a broad linter, or nothing
- **Because:** research on AI-built apps found 45–62% ship with vulnerabilities, and 63% of
  people building this way have no coding background — so they cannot review what they
  ship. Rescue engineers name the same seven patterns repeatedly, and by mid-2026 ~8,000 of
  ~10,000 AI-built startups needed a rebuild costing $50k–$500k. Narrow is deliberate: a
  checker that cries wolf gets ignored, and then the real warning is too. Reversible is
  deliberate too — people grow, and the training wheels must come off cleanly.
- **By:** pulkit

### 2026-08-09 — describe changes by what they let the software do
- **Chose:** surface who can get in, what leaves the machine, what's stored or deleted —
  then say it in one sentence a non-coder could disagree with
- **Over:** expecting them to read a diff
- **Because:** the documented failure is a verification gap, not laziness. "Anyone with the
  link can now read every entry" is a review someone non-technical can genuinely perform;
  "added a GET route without auth middleware" is not.
- **By:** pulkit

### 2026-08-09 — flag one-way doors, don't gate them
- **Chose:** name the decisions that are painful to reverse (data model, accounts or not,
  single vs shared, real-time, where data lives, public URLs) in one line when they arise
- **Over:** treating all decisions alike, or forcing a review step
- **Because:** early product decisions are path-dependent — some are branches you cannot
  climb back down. Knowing which is which is exactly the experience a beginner lacks, and
  it is cheap to hand over at the right moment.
- **By:** pulkit

## Ideas we said no to (and why)

`PRIORITIES.md` gets rewritten on every triage, so reject reasoning kept only there
vanishes. It belongs here instead — otherwise the same idea gets proposed, debated, and
rejected again every few weeks, which wears people down faster than almost anything else.

Not permanent: if circumstances change, reverse it deliberately and note what changed.

### Live/real-time coordination backend  (proposed by pulkit, decided 2026-08-09)
- **Verdict:** deferred until the file-based flow proves genuinely insufficient
- **Because:** needs hosting, auth, and ongoing cost. Explicitly not a priority; the
  static-snapshot flow covers the actual need today.

### Restricting who can view a GitHub Pages dashboard  (proposed by pulkit, decided 2026-08-09)
- **Verdict:** rejected — not possible on a free plan
- **Because:** Pages access control is Enterprise Cloud only. Superseded by using a private
  repo, which achieves the same goal for free.

### Auto-updating the skill on every invocation  (proposed by pulkit, decided 2026-08-09)
- **Verdict:** rejected in favour of an explicit `update` command
- **Because:** a tool that silently rewrites itself mid-task is impossible to reason about.
  Predictability beats freshness here.

### Four small skills for the dashboard actions  (proposed by pulkit, decided 2026-08-09)
- **Verdict:** rejected; one skill answering to several bare trigger words instead
- **Because:** several tiny skills with near-identical descriptions mis-trigger against
  each other. Keep skill count low and trigger surface wide.

## Gotchas and dead ends

Things tried that didn't work, and traps in the codebase or its dependencies. This section
saves the most time — it stops the second and third person rediscovering the same wall.

**Read this section before changing anything in `publish.sh` or `.gitattributes`.** All
three entries below were found by stress-testing four simulated collaborators, and all
three pass silently at two people while breaking badly at four.

### Generated files deadlocked everyone but the first pusher  (pulkit, 2026-08-09)
`dashboard.html` was marked `-merge`. Because it's generated, it differs on every machine,
so it conflicted on *every* concurrent push and aborted the rebase — three of four people
were permanently blocked and their ideas never reached the repo. Fix: `publish.sh` treats
`GENERATED_FILES` as auto-resolvable and rebuilds them after rebasing. Never hand a
generated-file conflict to a person.

### `git rebase --skip` silently deleted a whole commit  (pulkit, 2026-08-09)
The first attempt at the fix above called `git rebase --skip` whenever the rebase got
stuck. That discards the **entire commit**, not just the conflicting file — an entire
recorded decision vanished. Fix: only skip after confirming the commit is genuinely empty
(`git diff --cached --quiet HEAD`).

### Two people appending at once lost one entry  (pulkit, 2026-08-09)
"Append-only means low conflict" is wrong for end-of-file appends: both sides touch the
same spot and rebase keeps one. Fix: `merge=union`. Without `.gitattributes` committed and
present in the clone, this protection silently does not apply.

### Union-merge hides the collisions it prevents  (pulkit, 2026-08-09)
The cost of never losing data is that git reports success to everyone and never mentions
the clash — two people can claim the same task, or record contradictory decisions, with no
warning at all. That's why `scripts/check_collisions.py` exists. It is **lexical only**:
it cannot tell that "push notifications when a plan changes" and "alert members if the plan
is updated" are one feature. Semantic duplicates and scope drift need the model's
judgment, and `SKILL.md` instructs it accordingly.

### `CLAUDE.md` and `.gitattributes` must be committed by `publish.sh`  (pulkit, 2026-08-09)
An early version committed only the data files. A fresh clone then arrived with no workflow
brief and no merge protection — the entire mechanism missing for everyone but the author.
Both are now in `SOURCE_FILES`.

## How things work

**Three layers of memory, deliberately separated.** `IDEAS.md`/`TASKS.md` hold *state*
(what exists, who's on it). `CONTEXT.md` holds *conclusions* (what's settled and why).
`JOURNAL.md` holds *reasoning and live arguments*. The third is the one that normally
evaporates, and it's what someone needs in order to disagree intelligently rather than
re-tread settled ground.

**Why capture is the mechanism, not bookkeeping.** Each person's chat history is private,
so reasoning that happened in one conversation is invisible to everyone else. The files are
the only shared memory. That's why sessions start with a catch-up read and why the skill
records as it goes rather than waiting to be asked.

**Two skills, not many.** `team-collab` does the workflow; `why` explains history. Skill
count is kept deliberately low because similar descriptions mis-trigger against each other.
Prefer adding a trigger word or subcommand to an existing skill over creating a new one.

**The skill is installed from this repo.** `~/.claude/skills/` holds working copies;
`skills/` here is canonical. `scripts/update_skill.sh` syncs canonical → installed. Edit
here, not in `~/.claude/skills/`, or your change gets overwritten on the next update.
