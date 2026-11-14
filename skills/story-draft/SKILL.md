---
name: story-draft
compatibility: Needs Python 3 (standard library only) to run the bundled text checker. Install the whole skill set together; some skills read sibling skill folders.
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
4. **Read the voice file and its sample passage last**, just before you write, for how the story sounds and not only what the sheet says. Where the writer has chapters of their own, those pages are the voice. Never reuse a sentence or an image from the voice file or its sample: they show the register, and a reader would meet them twice.

## By who owns drafting

- **`ai`**: draft the chapter (below).
- **`alternate`**: write the next scene only, continuing from where the writer's last scene ends, in the writer's voice as their pages show it. Then hand the next scene back to them.
- **`writer`**: do not write the chapter. Offer a scene list for it (who wants what, what is in the way, how it turns out, the hook out), the questions under "Pass 1: imagine each scene", the questions the craft checks below raise, or a line or two of illustration if the writer asks how something could go. Then offer to check their draft when it is done.
  If they want the AI to draft after all, that is a settings change: offer `story-onboard`, which shows the change and asks first. Never change the settings yourself.
- **`none`** (design only): there is no prose stage. Say so, and offer to refine the design instead.

## When inputs are missing

- **No beats for this chapter, and the AI owns planning:** do not draft blind. First work out what this chapter is for, from the project itself: any timeline or phase plan in `kb/`, the spec, the promise ledger, the open questions, and the previous chapter's hook out. Write a working plan of a few lines to `work/brainstorm/draft-plan-NNN.md`: what the chapter changes, what it sets up or pays off, the main scenes, and the hook out. A chapter that changes nothing and sets nothing up is the failure to avoid. If the project does not say what comes next, or two directions are equally supported, ask one question with the two directions as choices, or offer `story-plan`, instead of picking one quietly. Then draft from the working plan. Show the plan and every assumption at the top of your hand-over, and offer to plan properly afterward. Do not refuse.
- **No beats, and the writer owns planning:** ask for the chapter's beats in a few bullets, offering a scene-list template. If the writer says "just write it", draft with listed assumptions as above.
- **Nothing exists at all:** ask one question about the story and offer `story-develop`.
- **No voice or style file, and no earlier chapters:** ask for a paragraph of the writer's own writing or the voice they want, or offer `story-voice`, and wait.

## Reading a long story

Once the story has five or more chapters, read it in tiers instead of loading every chapter:

1. The chapter in hand and its beats, in full.
2. The chapters just before and just after it, in full.
3. Every other chapter as its card in `work/cards/`. Open the prose only when a card is missing or stale, when the task needs the exact wording, or when a card disagrees with another source. The prose wins: correct the card from it.

Run `cards.py report <project folder>` from the `story-continue` skill folder (full path, no `cd`) to see missing and stale cards. A card that agrees with everything else is enough: do not open its chapter just to be thorough. A card points to its chapter; a fact that is only on a card is not settled.

Writing a card is housekeeping, not a fix. When you had to open a chapter because its card was missing or stale, rewrite the card from the chapter and stamp it (see Chapter cards in `story-continue`), and say so in one line. Never change a chapter to match its card.

## Drafting a chapter

- Follow the beats in order: the goal, each scene and how it turns out, the hook out. If a beat does not work on the page, say so and propose a change; do not skip it quietly.
- Stay inside `kb/`. Never contradict a settled fact. Where the beats need a detail that is not settled, write something plausible and list it as a new fact.
- Keep the project's chapter length, viewpoint, tense, and voice file for this part of the book.
- The craft checks at the end are for Pass 3 and for the files you write. Do not draft by checklist.
- Draft one chapter. Do not run ahead without the writer's go-ahead.

The beats decide what happens. How it reads is your judgment as a writer. The three passes below are not optional and not reorderable: do every step of each. Inside them the choices are yours, and where your taste and the project's voice file differ, the voice file wins.

## Pass 1: imagine each scene

Before writing a scene, settle these in your notes or your reasoning, never on the page:

- **The pleasure.** What a reader will enjoy here: a voice, a joke, an argument, somebody being good at something, dread. Name it, so the draft delivers it and no later fix sands it off.
- **Want and dread.** What the viewpoint character is trying to get or avoid, and what they fear will happen instead.
- **In and out.** The state they arrive in and how they leave it changed.
- **What they have wrong:** a belief, a misreading, a thing they are not looking at.
- **What only they would notice,** from their trade, history, and want. If the first detail to arrive would fit any story, take the next.
- **Where the words go.** The moment the scene turns gets the room; routine is summarized or skipped.
- **One thing the beats did not predict** that is right for these people.

If an earlier chapter exists, note how it opened and closed, and do both differently.

## Pass 2: write it

Write the chapter as a novelist with this voice would: with appetite, making your own decisions about where to be funny, where to tell something outright, where to be blunt, and when to break a habit of good taste. A draft that takes risks and misses in places is worth more than one that offends nobody; the next pass catches the misses. Aim for a chapter where somebody is plainly telling this (a mind, an attitude, a sense of humor), where people sound like themselves and want things from each other, and where what is on the page could only be in this story.

`prose-craft` and `scene-dialogue-behavior` hold the reasoning and worked examples. Load them when a scene will not come alive, not as rules to write by.

## Pass 3: read it back

Read the finished chapter once as its reader would, start to finish. Then do each step:

1. **Mark what is alive.** The lines a reader would repeat to someone: the joke, the exact odd detail, the thing only this person would say. A chapter needs several, spread through it. A scene with none was written dutifully: write it again for the pleasure you named in Pass 1.
2. **The turn and the skim.** If the moment the chapter turns is not among its most alive passages, write it again from inside the character. Do the same for the passage a reader would skim, or cut it. Write a passage again whole; polishing words does not fix what was never imagined.
3. **Look for the known failures.** Drafted fiction fails in predictable ways. Find each one that is here and fix it by imagining the moment again, not by applying a rule:
   - narration filmed from outside, with no thought, judgment, or mistake from the viewpoint character
   - the narrator explaining what a scene meant
   - dialogue in tidy turns: lines that answer each other neatly, a cornered person briefing the reader, a line that states its own subtext, gestures between lines that change nothing
   - one register for everyone, including everyone dodging with the same dry wit
   - feeling carried only by labels or by reports from the body, unless the voice file asks for named feelings
   - description by denial ("it did not rush") or by reflex comparison
   - a line that sounds deep and states nothing, or shows a picture that cannot be pictured
   - every scene at one temperature, or every scene ending the same way
4. **Check that it adds up.** Follow the hours, positions, and objects through the chapter: what time it is, who stands where and in what order, who holds what, what each person can see. Fix each slip.
5. **Count your habits.** Run `habits.py` from the `story-check` skill folder (full path, no `cd`) on the chapter. It lists comparisons, negated narration, body reports, hedges, and one-line paragraphs in the narration with line numbers. Where one habit is carrying the page, keep the instances doing real work and rewrite the rest. There is no passing number.
6. **Check the borrowings.** Run `habits.py <chapter> --borrowed-from <voice file> <sample passage>`: it lists every run of five or more words the chapter shares with them. Each one comes out, along with any image taken from them. Then reread the beats' turn note and look for it in the chapter said in other words; that comes out too. The opening and ending differ in kind from the previous chapter's.
7. **Check nothing was lost.** Go back to what you marked in step 1. Every one of those lines should have survived steps 2 to 6, or been replaced by something at least as alive. Trading a living line for a correct one is a bad trade: put it back.

Leave this pass out of the hand-over. The hand-over says what the chapter does, not that it was improved.

## Autopilot (the AI drafts and revises)

When the settings give the AI both drafting and revising, keep going chapter by chapter until the check-in the settings name (`check-in`: every chapter, every three chapters, or every part of the book). For each chapter:

1. **Draft** it as above.
2. **Check it silently** following `story-check`, including the dialogue and over-explanation pass and the text checker (`check_text.py` in the `story-check` skill folder, run with its full path on your chapter, adding `--words MIN-MAX` when the beats or the project's rules state a length range; fix real slips such as leaked wrapper text, an unclosed quote, a duplicated paragraph, a last line that stops mid-sentence, or a loop of repeated text, and bring a chapter that misses the stated length back into range). Keep the findings as a working note in `work/critique-reports/`; do not show the raw report.
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
- If `work/drafts/_delivered/` holds a copy of that chapter, compare it with the accepted chapter using `diff_chapter.py` in the `story-edits` skill folder (full path, no `cd`). Unchanged: delete the copy now. Edited: keep it, because `story-edits` learns from the writer's changes and then deletes it.

## Saving and handing over

Save the chapter to `work/drafts/` with the project's naming, or the beats file's `NNN-slug.md`. Its first line is `<!-- status: draft -->`. Never remove that line yourself; only the writer's approval does, and a chapter with no status line is trusted.

Also save an exact copy of the chapter, as handed over, to `work/drafts/_delivered/` under the same file name, replacing any earlier copy. It is how the writer's later edits can be told from your text. Keep it only until those edits have been learned from or the chapter is accepted unchanged.

Then write or refresh the chapter's card (see Chapter cards in `story-continue`) when the story has five or more chapters or the chapter already has a card.

If the project keeps a promise ledger, update it: mark each promise the chapter moved `advanced` or `paid`, and add a line for each new promise the chapter made (the line format is in `story-plan`). Change nothing else in it.

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

Apply each check that fits this story. In the files you write (beats, reports, notes), record its ID with a short note of what it found in this story, or `n/a` with a reason. Never show IDs or skill names to the writer: in conversation, ask or say the substance in the craft language the settings name. A deliberate break of a framework is a valid answer, not a defect: say it is deliberate and do not push the story back toward the formula. Load the skill listed for a check's family (after the list) only when you need its full reasoning.

- `character.entry.01` At first entry, has the prose shown the character's role or identity, or has only the author known it?
- `character.entry.02` Is the character's link to the current event or to the viewpoint character clear?
- `character.entry.03` Does the reader get a first impression the viewpoint character would actually form?
- `character.entry.04` For a villain, love interest, rival, or core ally: is there at least one recognizable trait (appearance, clothing, posture, voice, a habitual gesture, or how others react)?
- `character.entry.05` Is anything about this character, their place, or their relationships assumed because the author knows it, and not shown?
- `scene.access.01` For each thing a character acts on, which of seeing, hearing, reaching, or inferring gave it to them in this scene?
- `scene.access.02` Does any character understand something they only saw, or inspect something they only passed once?
- `scene.access.03` Are shared, specialized, and private knowledge kept apart (an expert's judgment does not leak to a layperson, and a private motive is not known to others)?
- `scene.access.05` When a character states a fact, is it clear whether it is an observation, a report, a judgment, an intention, or a mistake?
- `scene.dialogue.01` For each action beat in a sustained exchange, does the reaction change the next line, tactic, or situation? If not, it is decorative or procedural.
- `scene.dialogue.02` Are beats placed where something changes (information lands, a lie, a shift in power, a decision) and not spread evenly or attached to every line?
- `scene.dialogue.04` Was a flat exchange "fixed" by adding emotion labels or a gesture to every line? Untagged rapid dialogue and plain stated silence are fine when voices and pressure are clear.
- `scene.dialogue.05` Does the viewpoint character notice only what they would under this pressure, instead of the scene cutting to every participant's reaction?
- `plot.ppp.02` For this stretch, name what tells the reader the story is moving toward one of those promises. A stretch with no signpost reads as a stall.
- `plot.promises.05` Does each new character, sequence, or chapter make its own small promise, and does the chapter signal it was delivered?
- `plot.layering.01` For each important scene, name the outer goal and the inner struggle. Does the outer obstacle press on the inner flaw?
- `character.dialogue.02` Does the refusal, or the compromise, come from the character's own nature, so a different character would have answered differently?
- `character.dialogue.03` Does each reveal about a character come through what they say and how they push, not through the narrator explaining?
- `character.presenting.02` Does any character state their own motive to someone who already knows it?
- `character.presenting.03` With dialogue tags and setting removed, could a reader tell who is speaking from the lines alone?
- `character.relatable.02` Does a trait carry the reader's sympathy, or is the narration telling them to feel it?
- `worldbuilding.filtered.02` Is each description a catalog of what exists, or a record of what this person notices?
- `worldbuilding.pyramid.01` Find the most abstract paragraph (an explanation, a reflection, a cosmology). What concrete detail sits in the paragraphs just before and after it?
- `worldbuilding.pyramid.04` Is a figure of speech colliding with the world, such as "he flew across the room" where people really fly?
- `worldbuilding.curve.02` For each paragraph of explanation, who is thinking it, and why now?
- `scene.show.01` For each stated trait or emotion, does it matter enough to the story to be shown? If yes, find one specific action or detail; if no, leave the plain statement.
- `scene.pov.02` Within a scene, does the narration stay in one head, and is any switch deliberate and clear to the reader?
- `prose.craft.01` For each scene, where on the page does the viewpoint character want, judge, or think something through? A scene of only actions, objects, and speech reads as filmed.
- `prose.craft.02` For each reflection, is it the character's (partial, possibly wrong, leading to what they do next), or the author's caption on the scene?
- `prose.craft.03` How is each strong feeling carried? If mostly by labels or body reports (chest, breath, pulse, stomach), find what the feeling makes this character notice, avoid, or do.
- `prose.craft.04` Take the most prominent details. Could each sit unchanged in another story, and does each do a job (show who is looking, change an action, carry history, set something up)?
- `prose.craft.05` Does any sentence or image sound meaningful without stating anything exact? Say what it literally claims or what a reader would picture.
- `prose.craft.06` Where does the chapter spend its words? Does the moment that turns each scene get the most room, with routine summarized or skipped?
- `prose.craft.09` Against the earlier chapters, does this one open and close in a different way, and avoid leaning on the same devices?
- `prose.craft.11` What would a reader repeat to someone (a joke, an edged line, an exact odd detail)? Quote them. Against an earlier version, is anything of that kind gone with nothing as alive in its place?
- `prose.tells.01` Not X but Y: a contrast that denies something nobody claimed.
- `prose.tells.02` A closer that explains the beat the scene already showed.
- `prose.tells.03` An aphorism in the narration in place of the character's actual state.
- `prose.tells.09` Narrated significance: the narration announces that a moment matters instead of showing its consequence.
- `prose.tells.10` Reaction riders: an appended clause that tells the reader what to feel about a simple action.
- `prose.tells.13` An emotion named right after it is shown.
- `prose.tells.15` Dialogue that states its own subtext.
- `prose.tells.21` Lines that answer each other in tidy pairs, often echoing the last line's wording.
- `prose.tells.22` A cornered character explains their position in a tidy speech that briefs the reader.
- `prose.tells.23` Description by denial: narration that says what did not happen or what a thing was not (weak alone).
- `prose.tells.24` Hollow depth: a line or image that sounds meaningful and states nothing exact.

Skill for each check family: `character.entry` character-first-entry; `scene.access` scene-access-limits; `scene.dialogue` scene-dialogue-behavior; `plot.ppp` plot-promise-progress-payoff; `plot.promises` plot-kinds-of-promises; `plot.layering` plot-layering-conflict; `character.dialogue` character-floating-outline-for-dialogue; `character.presenting` character-presenting-a-character; `character.relatable` character-relatability-toolkit; `worldbuilding.filtered` worldbuilding-viewpoint-filtered-description; `worldbuilding.pyramid` worldbuilding-pyramid-of-abstraction; `worldbuilding.curve` worldbuilding-learning-curve-and-exposition; `scene.show` show-dont-tell; `scene.pov` viewpoint-and-tense; `prose.craft` prose-craft; `prose.tells` prose-ai-tells.
<!-- generated:checks:end -->
