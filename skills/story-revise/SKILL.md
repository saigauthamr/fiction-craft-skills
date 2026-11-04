---
name: story-revise
metadata:
  type: workflow
description: >
  Use to revise a chapter, apply review notes, or resolve rejected facts. The AI revises its own drafts with previous versions preserved and changes re-checked; when the writer owns revision, it gives notes and leaves prose unchanged.
---

# Story revise

Act on a check report, or on chapters flagged for revision. Whoever owns revising does the changing; you never change prose the settings say is the writer's.

## Before you revise

1. **Read the settings** (who owns revising and drafting, the craft language) and the project's own revision conventions.
2. **Chapters marked `needs revision` come first.** Their status line says why (usually a rejected fact, or a change made by `story-steer`). Remove the rejected fact or apply the change, and nothing else.
3. Otherwise read the check report, the chapter, its beats, and the `kb/` pages it leans on. With no check report, recommend `story-check` first.
4. List the open findings with your recommendation for each (fix, skip, or ask) and let the writer choose, unless the AI fully owns drafting and revising and this is the silent fix inside autopilot. Never fix what the writer did not agree to.

## By who owns revising

- **`ai`**: revise the AI's own text (below). When drafting alternates, revise only the passages the AI wrote; the writer's passages get notes.
- **`writer`**: do not change the chapter. Give the writer each finding as a short note: where, what is wrong, and one way to fix it, in the craft language the settings name. Offer to check again when they have revised.
- **`none`** (design only): there is no prose to revise.

## Revising

1. **Keep the earlier version.** Copy the chapter to `work/drafts/_previous/` with a version number before changing it. Never overwrite the only copy.
2. Work in priority order, must-fix first.
3. Change as little as the finding needs. Keep the voice and the settled facts. If a fix needs a new fact, queue it as pending; never write it into `kb/`.
4. In the check report, delete each finding once it is fixed. A finding you or the writer decide not to fix becomes `[resolved] declined: <reason>`. Only a finding deferred to later stays `[open]`, with "deferred" and why. Delete the report file when no findings are left.
5. **Re-check your own new text** against the finding that prompted it and with the craft checks below. Do not swap one habit for a close cousin of it, such as replacing a named emotion with a stock gesture.
6. Set the chapter's status line to `<!-- status: draft -->` (or `awaiting check-in` inside autopilot). Never remove a chapter's status line yourself; only the writer's word does that.

## Handing over

Say what changed and what did not, and offer another check. Repeat check and revise until the writer says the chapter is done; never decide that yourself.

## Rules

- Never delete the earlier version.
- Never delete a finding you did not fix.
- Report what the revision does, not that it is better.

<!-- generated:checks:start -->
## Craft checks (generated)

Apply each check that fits this story. In the files you write (beats, reports, notes), record its ID with a short note of what it found in this story, or `n/a` with a reason. Never show IDs or skill names to the writer: in conversation, ask or say the substance in the craft language the settings name. A deliberate break of a framework is a valid answer, not a defect: say it is deliberate and do not push the story back toward the formula. Load the named skill only when you need its full reasoning.

- `foundations.revision.01` Are the problems ranked, with core problems (a character that does not work, a broken promise) ahead of line-level ones? (`foundations-revision-guide`)
- `foundations.revision.02` Does the top item have a specific plan: where to plant setup, which scenes to add or cut, which chapters change? (`foundations-revision-guide`)
- `foundations.revision.03` Is this pass limited to one or two goals? (`foundations-revision-guide`)
- `foundations.revision.04` Is any note being applied as a fix without agreement that it points at a real problem? (`foundations-revision-guide`)
- `foundations.readers.02` For each pattern, what is the cause in the story, as opposed to the fix a reader suggested? (`foundations-alpha-beta-readers`)
- `prose.tells.01` Not X but Y: a contrast that denies something nobody claimed. (`prose-ai-tells`)
- `prose.tells.02` A closer that explains the beat the scene already showed. (`prose-ai-tells`)
- `prose.tells.03` An aphorism in the narration in place of the character's actual state. (`prose-ai-tells`)
- `prose.tells.04` Arguing with no one: the narration rejects a reading nobody offered. (`prose-ai-tells`)
- `prose.tells.05` Forced triads: lists of three by reflex. (`prose-ai-tells`)
- `prose.tells.06` Repeated sentence openings in a run. (`prose-ai-tells`)
- `prose.tells.07` Dashes as the universal connector (weak alone). (`prose-ai-tells`)
- `prose.tells.08` Stacked hedges on one perception (weak alone). (`prose-ai-tells`)
- `prose.tells.09` Narrated significance: the narration announces that a moment matters instead of showing its consequence. (`prose-ai-tells`)
- `prose.tells.10` Reaction riders: an appended clause that tells the reader what to feel about a simple action. (`prose-ai-tells`)
- `prose.tells.11` Stock AI words (weak alone, strong in groups). (`prose-ai-tells`)
- `prose.tells.12` Chatbot wrapper text around the prose. (`prose-ai-tells`)
- `prose.tells.13` An emotion named right after it is shown. (`prose-ai-tells`)
- `prose.tells.14` "A flicker of" and "a mix of" emotions. (`prose-ai-tells`)
- `prose.tells.15` Dialogue that states its own subtext. (`prose-ai-tells`)
- `prose.tells.16` Stock body reactions (weak alone). (`prose-ai-tells`)
- `prose.tells.17` Stock atmosphere lines (weak alone). (`prose-ai-tells`)
- `prose.tells.18` Tag and gesture filler between lines of dialogue (weak alone). (`prose-ai-tells`)
- `prose.tells.19` Stacked similes (weak alone). (`prose-ai-tells`)
- `prose.tells.20` One register for every speaker (weak alone; whole-chapter pass only). (`prose-ai-tells`)
- `prose.tells.21` Lines that answer each other in tidy pairs, often echoing the last line's wording. (`prose-ai-tells`)
- `prose.tells.22` A cornered character explains their position in a tidy speech that briefs the reader. (`prose-ai-tells`)
<!-- generated:checks:end -->
