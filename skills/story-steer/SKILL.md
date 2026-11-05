---
name: story-steer
metadata:
  type: workflow
description: >
  Use for story changes such as "darker", "slower", or "make this character colder". Proposes numbered patches with their effects, applies approved changes, preserves old wording, and flags chapters needing revision.
---

# Story steer

The writer says what they want in their own words. You turn it into specific, numbered changes and keep the story consistent. You change the plan and the story facts, never the drafted chapters.

## Before you start

Read the settings in the project's Story project block for the craft language to use, the project's own rules for where things live, and the spec, the promise ledger, the beats, the `kb/` pages, and the voice files the request touches.

## Steps

1. **Restate the request as patches.** A numbered list. Each patch says what changes (the spec, a character, a world rule, the voice file, a chapter's beats), why, in the writer's words, what it touches (which beats and which drafted chapters), and the size of the job: small, medium, or large.
2. **Offer options for a vague request.** "Darker" could mean grimmer narration, higher stakes, or morally grayer characters. Offer the versions with what each does to the story and recommend one. Never guess silently.
3. **Check it against the craft checks below**, and say plainly when a change opens a gap: a promise that loses its payoff, a character who loses the scale that made them work, a climax that no longer resolves the kind of progress the story measures. Say it in the craft language the settings name.
4. **Ask for approval** by number ("Apply 1 and 3?"). The writer can accept all, some, or none.
5. **Apply only the approved patches**, changing only what each says. A change to a settled story fact is a canon change and needs that approval; it is never applied on your own judgment.
6. **List the fallout.** Name the drafted chapters that now need revising and mark each `<!-- status: needs revision: <the patch> -->` in place of its current status line (the only change you make to a chapter). Offer `story-revise` for them, one at a time. Do not rewrite drafts here.
7. **Log it** in `work/spec/patch-notes.md` (or the project's own change log): the date, the request, each patch applied, and the old wording, so any change can be undone.

## If it clashes with earlier choices

If a request contradicts something the writer already approved or a settled fact, say so plainly and offer the ways to reconcile it. Do not overrule an earlier choice silently, and do not refuse a change of mind.

## Rules

- Do not argue about taste.
- Be honest about the cost of a change: a late change to a central rule touches many chapters.
- Never delete the earlier version of anything.
- Never edit chapter prose here. The status line is the only change to a chapter.

<!-- generated:checks:start -->
## Craft checks (generated)

Apply each check that fits this story. In the files you write (beats, reports, notes), record its ID with a short note of what it found in this story, or `n/a` with a reason. Never show IDs or skill names to the writer: in conversation, ask or say the substance in the craft language the settings name. A deliberate break of a framework is a valid answer, not a defect: say it is deliberate and do not push the story back toward the formula. Load the skill listed for a check's family (after the list) only when you need its full reasoning.

- `plot.ppp.04` Has a promised thread been dropped for a more interesting subplot? If the progress is what you want to tell, revise the promise, not the middle.
- `plot.progress.01` Name the kind of progress the story measures (information, relationship, skill, distance, or another) and check that the climax resolves that kind.
- `character.scales.03` Which scale does the character's arc move along, and is the movement shown on the page?

Skill for each check family: `plot.ppp` plot-promise-progress-payoff; `plot.progress` plot-types-of-progress; `character.scales` character-proactive-relatable-capable.
<!-- generated:checks:end -->
