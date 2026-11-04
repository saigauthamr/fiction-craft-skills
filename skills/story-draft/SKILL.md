---
name: story-draft
metadata:
  type: workflow
description: >
  Use to draft a chapter or scene, take a turn, or act on "go" for a planned chapter. Follows drafting ownership and project voice; coaches when the writer drafts. Queues new facts for approval and supports bounded autopilot.
---

# Story draft

Write prose only when the settings say the AI drafts. The draft is working material: the writer accepts it, changes it, or throws it away.

## Before anything

1. **Read the settings** in the project's Story project block: who owns drafting, and how much craft language to use. No valid block: do not draft; offer a scene list and mention `story-onboard`.
2. **Read the project's own rules first.** They may name the voice and style files for each part of the book, chapter length, chapter naming and numbering, a header or dateline every chapter opens with, and where open questions go. Follow them over anything here. If they name the files to load for drafting, load those and no more.
3. **Read the chapter's beats**, the `kb/` pages its "facts to check" names, and the chapter before it. Do not load the whole knowledge base.

## By who owns drafting

- **`ai`**: draft the chapter (below).
- **`alternate`**: write the next scene only, continuing from where the writer's last scene ends, in the writer's voice as their pages show it. Then hand the next scene back to them.
- **`writer`**: do not write the chapter. Offer a scene list for it (who wants what, what is in the way, how it turns out, the hook out), the questions the craft checks below raise, or a line or two of illustration if the writer asks how something could go. Then offer to check their draft when it is done.
  If they want the AI to draft after all, that is a settings change: offer `story-onboard`, which shows the change and asks first. Never change the settings yourself.
- **`none`** (design only): there is no prose stage. Say so, and offer to refine the design instead.

## When inputs are missing

- **No beats for this chapter, and the AI owns planning:** do not draft blind. First work out what this chapter is for, from the project itself: any timeline or phase plan in `kb/`, the spec, the promise ledger, the open questions, and the previous chapter's hook out. Write a working plan of a few lines to `work/brainstorm/draft-plan-NNN.md`: what the chapter changes, what it sets up or pays off, the main scenes, and the hook out. A chapter that changes nothing and sets nothing up is the failure to avoid. If the project does not say what comes next, or two directions are equally supported, ask one question with the two directions as choices, or offer `story-plan`, instead of picking one quietly. Then draft from the working plan. Show the plan and every assumption at the top of your hand-over, and offer to plan properly afterward. Do not refuse.
- **No beats, and the writer owns planning:** ask for the chapter's beats in a few bullets, offering a scene-list template. If the writer says "just write it", draft with listed assumptions as above.
- **Nothing exists at all:** ask one question about the story and offer `story-develop`.
- **No voice or style file, and no earlier chapters:** ask for a paragraph of the writer's own writing or the voice they want, or offer `story-voice`, and wait.

## Drafting a chapter

- Follow the beats in order: the goal, each scene and how it turns out, the hook out. If a beat does not work on the page, say so and propose a change; do not skip it quietly.
- Stay inside `kb/`. Never contradict a settled fact. Where the beats need a detail that is not settled, write something plausible and list it as a new fact.
- Keep the project's chapter length, viewpoint, tense, and voice file for this part of the book.
- Apply the craft checks below while you write. Avoid the machine-prose patterns listed among them.
- Draft one chapter. Do not run ahead without the writer's go-ahead.

## How people talk

Drafted dialogue fails in one predictable way: everyone takes turns delivering clear, complete, reasonable lines. People do not talk like that, least of all in a conflict.

- **Cornered people deflect.** They ask who told you, appeal to family or rank, change the subject, offer food, go quiet, or attack. They do not explain their position in a tidy speech, unless lecturing is who they are.
- **Lines do not answer each other neatly.** People answer the question they wish they had been asked, or none. They do not pick up the last speaker's words and hand them back. Some questions get no answer at all.
- **People interrupt and leave things unsaid.** A line can break off. A pause can be the answer.
- **Each speaker sounds like themself.** Give them their own vocabulary, sentence length, and things they avoid saying. Cover the names: you should still know who is talking.
- **Facts come out contested and in fragments**, as accusations, half-denials, and slips, never as a briefing for the reader. If the reader must learn how something works, let it arrive in pieces that someone is fighting over.
- **Nobody states the subtext.** "I feel betrayed because you promised" becomes "You said you'd stay."
- **Tags:** "said", or none. Put an action between lines instead of an adverb.

## Leave the meaning to the reader

- Show what happens. Do not add a sentence that names the lesson, the significance, or the feeling just shown.
- The beats' turn is your aim, not your text. Never put it on the page, not even paraphrased.
- End a scene on an image or an action, not a summary of what it meant.

## Autopilot (the AI drafts and revises)

When the settings give the AI both drafting and revising, keep going chapter by chapter until the check-in the settings name (`check-in`: every chapter, every three chapters, or every part of the book). For each chapter:

1. **Draft** it as above.
2. **Check it silently** following `story-check`, including the dialogue and over-explanation pass. Keep the findings as a working note in `work/critique-reports/`; do not show the raw report.
3. **Revise** what must be fixed, following `story-revise`, and delete each finding from the working note once fixed, or mark it `[resolved] declined: <reason>` when you keep the text on purpose: keep the earlier version in `work/drafts/_previous/`, change as little as each finding needs, and re-check your own new text so one habit is not swapped for another. At most two passes.
4. **Continuity**: compare the chapter with `kb/` and the earlier chapters. If it contradicts a settled fact and you cannot fix it inside the chapter, stop and ask.
5. **Queue the new facts** as pending, major or minor, as described below.
6. Set the chapter's status line to `<!-- status: awaiting check-in -->`.

You may draft later chapters on top of pending **minor** facts; list those dependencies on the cards. A pending **major** fact stops autopilot until the writer decides. Stop earlier, too, when you need a decision, the plan needs to change, two revision passes did not clear a must-fix, or a chapter would cross a line the writer set.

**At the check-in**, show one card per chapter, five to eight plain lines: where it is saved; what happens; what changed; which promises moved; the new facts needing a yes or no, each with your recommended answer; what you fixed in your own check, in one line; any decision you need. Use the craft language the settings name.

**When the writer answers:**
- An approved fact goes into its `kb/` page, and its queue line is removed.
- A rejected fact: change its queue line to start with `[rejected]` (it is never proposed again), and set every chapter that used it to `<!-- status: needs revision: <the rejected fact> -->`. Revising those comes first, through `story-revise`.
- An accepted chapter is trusted, and trust is the default, so accepting it means deleting its status line and deleting its open findings from the check report (or marking a kept one `[resolved] declined: accepted as is`), and deleting the report file when nothing is left in it. Do this only on the writer's word, and record nothing else: no date, no "accepted by".

## Saving and handing over

Save the chapter to `work/drafts/` with the project's naming, or the beats file's `NNN-slug.md`. Its first line is `<!-- status: draft -->`. Never remove that line yourself; only the writer's approval does, and a chapter with no status line is trusted.

Then tell the writer, in the craft language the settings name:

1. Where the chapter is saved.
2. **New facts the draft invented**, one line each. Add each as `- [pending major] <fact> (chapter N)` or `- [pending minor] <fact> (chapter N)`. Major means plot, rules, motive, relationships, or timeline; minor means texture and background. Never write them into `kb/`. Never re-propose a fact marked `[rejected]`. If the project's instructions name one register for open or review items (for example a single open-questions file), use it for these too: pending facts are open items, and a second register is never created. Only when the project names none, use `work/brainstorm/pending-facts.md`.
3. Anywhere you departed from the beats, and why.
4. Any settled fact that was strained.
5. The assumptions list, if inputs were missing.
6. The next step: a check, then revision.

Never describe the chapter as finished or good. Describe what you did.

<!-- generated:checks:start -->
## Craft checks (generated)

Apply each check that fits this story. In the files you write (beats, reports, notes), record its ID with a short note of what it found in this story, or `n/a` with a reason. Never show IDs or skill names to the writer: in conversation, ask or say the substance in the craft language the settings name. A deliberate break of a framework is a valid answer, not a defect: say it is deliberate and do not push the story back toward the formula. Load the named skill only when you need its full reasoning.

- `plot.ppp.02` For this stretch, name what tells the reader the story is moving toward one of those promises. A stretch with no signpost reads as a stall. (`plot-promise-progress-payoff`)
- `plot.promises.05` Does each new character, sequence, or chapter make its own small promise, and does the chapter signal it was delivered? (`plot-kinds-of-promises`)
- `plot.layering.01` For each important scene, name the outer goal and the inner struggle. Does the outer obstacle press on the inner flaw? (`plot-layering-conflict`)
- `character.dialogue.02` Does the refusal, or the compromise, come from the character's own nature, so a different character would have answered differently? (`character-floating-outline-for-dialogue`)
- `character.dialogue.03` Does each reveal about a character come through what they say and how they push, not through the narrator explaining? (`character-floating-outline-for-dialogue`)
- `character.presenting.02` Does any character state their own motive to someone who already knows it? (`character-presenting-a-character`)
- `character.presenting.03` With dialogue tags and setting removed, could a reader tell who is speaking from the lines alone? (`character-presenting-a-character`)
- `character.relatable.02` Does a trait carry the reader's sympathy, or is the narration telling them to feel it? (`character-relatability-toolkit`)
- `worldbuilding.filtered.02` Is each description a catalog of what exists, or a record of what this person notices? (`worldbuilding-viewpoint-filtered-description`)
- `worldbuilding.pyramid.01` Find the most abstract paragraph (an explanation, a reflection, a cosmology). What concrete detail sits in the paragraphs just before and after it? (`worldbuilding-pyramid-of-abstraction`)
- `worldbuilding.pyramid.04` Is a figure of speech colliding with the world, such as "he flew across the room" where people really fly? (`worldbuilding-pyramid-of-abstraction`)
- `worldbuilding.curve.02` For each paragraph of explanation, who is thinking it, and why now? (`worldbuilding-learning-curve-and-exposition`)
- `scene.show.01` For each stated trait or emotion, does it matter enough to the story to be shown? If yes, find one specific action or detail; if no, leave the plain statement. (`show-dont-tell`)
- `scene.pov.02` Within a scene, does the narration stay in one head, and is any switch deliberate and clear to the reader? (`viewpoint-and-tense`)
- `prose.tells.01` Not X but Y: a contrast that denies something nobody claimed. (`prose-ai-tells`)
- `prose.tells.02` A closer that explains the beat the scene already showed. (`prose-ai-tells`)
- `prose.tells.03` An aphorism in the narration in place of the character's actual state. (`prose-ai-tells`)
- `prose.tells.09` Narrated significance: the narration announces that a moment matters instead of showing its consequence. (`prose-ai-tells`)
- `prose.tells.10` Reaction riders: an appended clause that tells the reader what to feel about a simple action. (`prose-ai-tells`)
- `prose.tells.13` An emotion named right after it is shown. (`prose-ai-tells`)
- `prose.tells.15` Dialogue that states its own subtext. (`prose-ai-tells`)
- `prose.tells.21` Lines that answer each other in tidy pairs, often echoing the last line's wording. (`prose-ai-tells`)
- `prose.tells.22` A cornered character explains their position in a tidy speech that briefs the reader. (`prose-ai-tells`)
<!-- generated:checks:end -->
