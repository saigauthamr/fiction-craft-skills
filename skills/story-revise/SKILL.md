---
name: story-revise
compatibility: Needs Python 3 (standard library only) to run a bundled script. Install the whole skill set together; some skills read sibling skill folders.
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
3. **If `work/drafts/_delivered/` holds a copy of the chapter that differs from it, the writer has edited the chapter.** Run `story-edits` first, so your revision never overwrites what they changed.
4. Otherwise read the check report, the chapter, its beats, and the `kb/` pages it leans on. With no check report, recommend `story-check` first.
5. List the open findings with your recommendation for each (fix, skip, or ask) and let the writer choose, unless the AI fully owns drafting and revising and this is the silent fix inside autopilot. Never fix what the writer did not agree to.

## Reading a long story

Once the story has five or more chapters, read it in tiers instead of loading every chapter:

1. The chapter in hand and its beats, in full.
2. The chapters just before and just after it, in full.
3. Every other chapter as its card in `work/cards/`. Open the prose only when a card is missing or stale, when the task needs the exact wording, or when a card disagrees with another source. The prose wins: correct the card from it.

Run `cards.py report <project folder>` from the `story-continue` skill folder (full path, no `cd`) to see missing and stale cards. A card that agrees with everything else is enough: do not open its chapter just to be thorough. A card points to its chapter; a fact that is only on a card is not settled.

Writing a card is housekeeping, not a fix. When you had to open a chapter because its card was missing or stale, rewrite the card from the chapter and stamp it (see Chapter cards in `story-continue`), and say so in one line. Never change a chapter to match its card.

## By who owns revising

- **`ai`**: revise the AI's own text (below). When drafting alternates, revise only the passages the AI wrote; the writer's passages get notes.
- **`writer`**: do not change the chapter. Give the writer each finding as a short note: where, what is wrong, and one way to fix it, in the craft language the settings name. For a flat passage, give the questions to answer about the moment (what the character wants, sees, and has wrong), not replacement prose. Offer to check again when they have revised.
- **`none`** (design only): there is no prose to revise.

## Revising

A revision that fixes structure and correctness can strip out the personality, and a chapter that is correct and lifeless is worse than the one you started with. So every revision does these steps, in order:

1. **Keep the earlier version.** Copy the chapter to `work/drafts/_previous/` with a version number before changing it. Never overwrite the only copy.
2. **List what is alive, before changing anything.** Read the chapter for what a reader would repeat to someone: jokes, lines with an edge, the exact odd detail, a character's particular way of talking, a passage with momentum. Write the list down, quoting each. This is the keep list. Also on it, unless a finding shows one failing at its own job: dialogue and its rhythm, inner thoughts, digressive texture, deliberate ambiguity or silence, repetition that carries rhythm.
3. **Fix in priority order, must-fix first, changing as little as each finding needs.** Keep the voice and the settled facts. A fix that needs a new fact queues it as pending; never write it into `kb/`. You may fix wording, punctuation, and paragraph breaks freely. Never compress concrete material into summary.
4. **A flat passage is written again whole.** When the finding is that a passage has no mind in it, a generic detail, a line that states nothing, or the same weight as everything around it, swapping words will not help, because the passage was never imagined. Go back into the moment (what the viewpoint character wants, sees, thinks it means, has wrong) and write that passage again, with the same events and facts, at about the same length. How it is written is your judgment. The rest of the chapter stays.
5. **A whole-chapter rewrite happens only when the writer asks for one.** Then the keep list matters most: build the new chapter around those lines, and add to them. The aim of a rewrite is everything the old chapter had, plus what it lacked. That is not a licence to add length: stay inside the chapter's length range, or within about a tenth of the old length if no range is set, and if what you added will not fit, say what you would cut and let the writer choose.
6. **Compare what was gained and what was lost.** Read the old and new versions side by side. For each line on the keep list: is it still there, or replaced by something at least as alive? Put back anything that was lost for nothing. Then ask the same of the chapter as a whole: is it as funny, as sharp, as strange, as much itself as before? If the new version is better built and duller, it is not finished. Then read the new version straight through once: a line carried over or put back has to fit what now surrounds it, and one that repeats a point already made comes out.
7. **Re-check your own new text** against the finding that prompted it and the craft checks below. Do not swap one habit for its cousin (a named emotion for a body report, a cut explanation for a comparison). Run `habits.py` from the `story-check` skill folder (full path, no `cd`) on both versions and compare.
8. **Housekeeping.** In the check report, delete each fixed finding; one you or the writer decline becomes `[resolved] declined: <reason>`; only a deferred one stays `[open]`, with why. Delete the report when it is empty. Set the status line to `<!-- status: draft -->` (or `awaiting check-in` inside autopilot) and never remove it yourself. Replace the chapter's copy in `work/drafts/_delivered/` with what you hand over. Rewrite its card (see Chapter cards in `story-continue`) if it has one or the story has five or more chapters.

When a fix would cost something on the keep list, say which line and what the fix gains, and let the writer decide.

## Handing over

Say what changed, what did not, and **what was lost**: any line from the keep list that did not survive, and why. Offer another check. Repeat check and revise until the writer says the chapter is done; never decide that yourself.

## Rules

- Never delete the earlier version.
- Never flatten concrete detail into summary.
- Never hand over a revision without the keep list checked against it.
- Never delete a finding you did not fix.
- Report what the revision does, not that it is better.

<!-- generated:checks:start -->
## Craft checks (generated)

Apply each check that fits this story. In the files you write (beats, reports, notes), record its ID with a short note of what it found in this story, or `n/a` with a reason. Never show IDs or skill names to the writer: in conversation, ask or say the substance in the craft language the settings name. A deliberate break of a framework is a valid answer, not a defect: say it is deliberate and do not push the story back toward the formula. Load the skill listed for a check's family (after the list) only when you need its full reasoning.

- `scene.dialogue.04` Was a flat exchange "fixed" by adding emotion labels or a gesture to every line? Untagged rapid dialogue and plain stated silence are fine when voices and pressure are clear.
- `foundations.revision.01` Are the problems ranked, with core problems (a character that does not work, a broken promise) ahead of line-level ones?
- `foundations.revision.02` Does the top item have a specific plan: where to plant setup, which scenes to add or cut, which chapters change?
- `foundations.revision.03` Is this pass limited to one or two goals?
- `foundations.revision.04` Is any note being applied as a fix without agreement that it points at a real problem?
- `foundations.readers.02` For each pattern, what is the cause in the story, as opposed to the fix a reader suggested?
- `prose.craft.01` For each scene, where on the page does the viewpoint character want, judge, or think something through? A scene of only actions, objects, and speech reads as filmed.
- `prose.craft.02` For each reflection, is it the character's (partial, possibly wrong, leading to what they do next), or the author's caption on the scene?
- `prose.craft.03` How is each strong feeling carried? If mostly by labels or body reports (chest, breath, pulse, stomach), find what the feeling makes this character notice, avoid, or do.
- `prose.craft.05` Does any sentence or image sound meaningful without stating anything exact? Say what it literally claims or what a reader would picture.
- `prose.craft.07` Is description built from what is present and what happens, or from denials and reflex comparisons?
- `prose.craft.11` What would a reader repeat to someone (a joke, an edged line, an exact odd detail)? Quote them. Against an earlier version, is anything of that kind gone with nothing as alive in its place?
- `prose.tells.01` Not X but Y: a contrast that denies something nobody claimed.
- `prose.tells.02` A closer that explains the beat the scene already showed.
- `prose.tells.03` An aphorism in the narration in place of the character's actual state.
- `prose.tells.04` Arguing with no one: the narration rejects a reading nobody offered.
- `prose.tells.05` Forced triads: lists of three by reflex.
- `prose.tells.06` Repeated sentence openings in a run.
- `prose.tells.07` Dashes as the universal connector (weak alone).
- `prose.tells.08` Stacked hedges on one perception (weak alone).
- `prose.tells.09` Narrated significance: the narration announces that a moment matters instead of showing its consequence.
- `prose.tells.10` Reaction riders: an appended clause that tells the reader what to feel about a simple action.
- `prose.tells.11` Stock AI words (weak alone, strong in groups).
- `prose.tells.12` Chatbot wrapper text around the prose.
- `prose.tells.13` An emotion named right after it is shown.
- `prose.tells.14` "A flicker of" and "a mix of" emotions.
- `prose.tells.15` Dialogue that states its own subtext.
- `prose.tells.16` Stock body reactions, and feeling always reported from the body (weak alone).
- `prose.tells.17` Stock atmosphere lines, and an offstage sound dropped into a pause (weak alone).
- `prose.tells.18` Tag and gesture filler between lines of dialogue (weak alone).
- `prose.tells.19` Reflex comparisons: stacked similes, or one in most paragraphs (weak alone).
- `prose.tells.20` One register for every speaker (weak alone; whole-chapter pass only).
- `prose.tells.21` Lines that answer each other in tidy pairs, often echoing the last line's wording.
- `prose.tells.22` A cornered character explains their position in a tidy speech that briefs the reader.
- `prose.tells.23` Description by denial: narration that says what did not happen or what a thing was not (weak alone).
- `prose.tells.24` Hollow depth: a line or image that sounds meaningful and states nothing exact.
- `prose.tells.25` One temperature: every scene quiet, every speaker oblique, every ending a held image (whole-chapter pass only).

Skill for each check family: `scene.dialogue` scene-dialogue-behavior; `foundations.revision` foundations-revision-guide; `foundations.readers` foundations-alpha-beta-readers; `prose.craft` prose-craft; `prose.tells` prose-ai-tells.
<!-- generated:checks:end -->
