---
name: story-check
compatibility: Needs Python 3 (standard library only) to run the bundled text checker. Install the whole skill set together; some skills read sibling skill folders.
metadata:
  type: workflow
description: >
  Use to check, review, or critique a chapter, test dialogue, or give a reader's report. Cites evidence against the plan, craft checks, and machine-prose patterns. Never edits the chapter.
---

# Story check

Find what is not working and say where, with evidence. Never fix anything here. A check that rewrites is a revision, and the writer should see the findings first. Checking is available in every setting, whoever wrote the chapter.

## Before you check

1. **Read the settings** in the project's Story project block, for the craft language to use. No valid block: use full terms.
2. **Read the project's own rules.** Any review checklist, voice rules, chapter format, or length range it names is part of the check. Where it names several voice files (for example one per part of the book), use the one that applies to this chapter.
3. **Read the chapter, its beats, the spec, and the `kb/` pages the beats name.** Without a spec or beats, check against the frameworks, the prose patterns, and the chapter's own internal consistency, and say what you could not check.
4. **Run the text checker first**, with its full path and the chapter file or the folder of chapters: `python3 check_text.py <chapter or folder>`. If the beats or the project's own rules state a length range for a chapter, add `--words MIN-MAX` (for example `--words 1800-2500`). It reports leaked assistant text, stray formatting, unbalanced quotes, duplicated paragraphs, encoding damage, whitespace problems, a last line that stops mid-sentence, a long phrase repeated three or more times, and a chapter outside the stated length, with line numbers. Treat each warning as something to look at, not a verdict: a real slip becomes a finding, a deliberate choice does not. A chapter that stops mid-sentence is probably cut off, so say that first. A repeated phrase may be a deliberate refrain, song, or repeated document header. A length warning is a mismatch with the plan, not a flaw in the prose: say which one the writer should change.
5. **Read the whole chapter before noting anything.**

## Reading a long story

Once the story has five or more chapters, read it in tiers instead of loading every chapter:

1. The chapter in hand and its beats, in full.
2. The chapters just before and just after it, in full.
3. Every other chapter as its card in `work/cards/`. Open the prose only when a card is missing or stale, when the task needs the exact wording, or when a card disagrees with another source. The prose wins: correct the card from it.

Run `cards.py report <project folder>` from the `story-continue` skill folder (full path, no `cd`) to see missing and stale cards. A card that agrees with everything else is enough: do not open its chapter just to be thorough. A card points to its chapter; a fact that is only on a card is not settled.

Writing a card is housekeeping, not a fix. When you had to open a chapter because its card was missing or stale, rewrite the card from the chapter and stamp it (see Chapter cards in `story-continue`), and say so in one line. Never change a chapter to match its card.

## Two kinds of report

**A check report** (the default, and what "check" or "review" means): run the craft checks below that apply. Skip any that do not, silently. Save the report to `work/critique-reports/` with the chapter's file name plus `-check` (or the project's own convention). One finding per list item:

```
- [open] <must fix | should fix | note>: <short title>. Check: <id>. Where: <chapter, scene or paragraph>. Evidence: "<short quote>". Fix: <what to do, in a sentence or two>.
```

Three kinds of finding have no framework check: a contradiction with `kb/` or an earlier chapter uses `Check: continuity`, a gap between the chapter and its beats or spec uses `Check: plan`, and a real warning from the text checker uses `Check: text`. Never borrow an unrelated ID to fill the field.

Rank findings by how much they hurt the chapter. End with the top three priorities and one thing the chapter does well that should be kept. A finding is removed from the report when it is fixed; one kept on purpose becomes `[resolved] declined: <reason>`, handled by `story-revise`.

**A reader's report** ("is it any good?", "be a reader"): read as a skeptical reader and report in five short parts: where I got bored, where I got confused, where I stopped believing it, what I saw coming too early, what worked. Give only the three biggest problems, each with a one-line example. Then the twist test: what you think the story's biggest secret is and how sure you are, and which clue gave it away if you guessed it early. Run the craft checks silently to find the problems; say them in the reader's words. Do not save a file unless the writer asks for one.

## Dialogue and over-explanation

Give these their own pass, because they are what makes drafted fiction read as machine-written.

- **Dialogue.** Do lines answer each other in tidy pairs, or echo each other's wording? Does a cornered character explain their position in a tidy speech? Does anyone dodge, interrupt, change the subject, or leave a question unanswered? Do the speakers sound different from each other? Does a line state its own subtext? Does the action between lines change the next beat, or is it a nod, sip, or look away that anyone could do, or a task step with no pressure in it? Do not flag untagged rapid dialogue that is clear, or a plain stated silence, as defects.
- **Over-explanation.** Does the narration say what a beat means after showing it, name an emotion right after showing it, announce that a moment matters, or close a scene by explaining it? Does a beat's planned turn appear in the prose as a sentence, when it should only shape the scene?

Use the matching prose-pattern checks for each finding. Quote the line.

## Talking to the writer

- In the file, every finding carries its check ID. In conversation, never show IDs or skill names: say the problem in the craft language the settings name (with `none`, plain words only).
- A framework the story breaks on purpose (for example, soft magic that is never meant to solve the plot) is not a defect. Do not report it, unless the break fails at what the story is trying to do instead.

## Rules

- Evidence for every finding. No evidence, no finding.
- Quote briefly. Do not paste paragraphs.
- Separate a problem in the chapter from a disagreement with the beats or spec; say which it is.
- Never edit the chapter, the plan, or `kb/`. The only file you write is the report.
- Do not propose cutting style-bearing material (dialogue and its rhythm, inner thoughts, observational detail, deliberate ambiguity or silence, rhythm-bearing repetition) unless you can say what it fails to do. Slack is not a finding just because it is not plot.
- No scores and no flattery. Say plainly what you could not check.

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
- `scene.access.04` Is each consequential choice made by the character who owns that decision, and does it follow from what they perceived or misread?
- `scene.access.05` When a character states a fact, is it clear whether it is an observation, a report, a judgment, an intention, or a mistake?
- `plot.bridges.01` For each major turn, can you name the pressure, the actor who interprets it, their goal, and their method?
- `plot.bridges.02` Why this person, why now, and why this method?
- `plot.bridges.03` If this event were removed, would the next decision change? If not, it is off the spine or a bridge is missing.
- `plot.bridges.04` Does any turn rest on a summary jump (A happened, so B) with no one choosing?
- `plot.bridges.05` Is every place, group, or person established before it carries an event?
- `plot.reveals.01` For each secret, is the true fact written down apart from what the reader is told?
- `plot.reveals.02` For each secret, can you name who knows it, who is wrong about it, where the reader gets the first clue, and where they learn it?
- `plot.reveals.03` Does any reveal come before its setup, or any setup go unrewarded?
- `plot.reveals.04` Does narration leak author truth the viewpoint character could not know?
- `plot.reveals.05` Does the outline tell the causal story before explaining the hidden system?
- `scene.dialogue.01` For each action beat in a sustained exchange, does the reaction change the next line, tactic, or situation? If not, it is decorative or procedural.
- `scene.dialogue.02` Are beats placed where something changes (information lands, a lie, a shift in power, a decision) and not spread evenly or attached to every line?
- `scene.dialogue.03` Is any procedural action (opening, reading, moving things) connected to human pressure, or is the scene static with props?
- `scene.dialogue.04` Was a flat exchange "fixed" by adding emotion labels or a gesture to every line? Untagged rapid dialogue and plain stated silence are fine when voices and pressure are clear.
- `scene.dialogue.05` Does the viewpoint character notice only what they would under this pressure, instead of the scene cutting to every participant's reaction?
- `plot.ppp.01` Name what the story has promised by this point: its tone, its central conflict, and what the main character wants.
- `plot.ppp.02` For this stretch, name what tells the reader the story is moving toward one of those promises. A stretch with no signpost reads as a stall.
- `plot.ppp.03` Does the payoff deliver what was promised, in a way that feels surprising yet inevitable, or something the reader was never led to want?
- `plot.ppp.04` Has a promised thread been dropped for a more interesting subplot? If the progress is what you want to tell, revise the promise, not the middle.
- `plot.promises.01` Which kinds of promise does the opening make (tone, plot, character, series), and which does it skip? Not every kind is required; mark each skip as deliberate or accidental.
- `plot.promises.02` From the first pages, could a reader say what feel to expect and what the main character wants?
- `plot.promises.03` Does the character promise show what the character wants, what they need, and why they cannot have it yet?
- `plot.promises.04` If the tone will switch (for example from thriller to travelogue), is the second tone promised at the start?
- `plot.promises.05` Does each new character, sequence, or chapter make its own small promise, and does the chapter signal it was delivered?
- `plot.bigp.02` For each chapter, name its little p plot and whether it advances a Big P promise or makes a promise of its own that the book keeps.
- `plot.bigp.03` Where does the story's emotional core actually live, in the headline plot or in a little p thread, and do the signposts follow it?
- `plot.progress.03` For this sequence, what does the reader think it is moving toward, and what signals tell them so?
- `plot.coldopen.01` Can the opening be described as a small version of the book's central conflict? If not, are a tone promise and a likable character with a hard problem doing that work instead?
- `plot.threeact.01` Write the major dramatic question in one sentence. Is it posed by the end of Act I, and does the climax answer it?
- `plot.threeact.02` Name the point after which the character cannot go back.
- `plot.threeact.03` Does the midpoint change what the reader believes the story is about, escalate it, or make it personal?
- `plot.threeact.04` Does each attempt in the second act make things worse, or do the attempts merely repeat?
- `plot.threeact.05` Is there a low point that the last realization climbs out of?
- `plot.tryfail.01` For each major success, what failed before it, and did the failure cost something or teach something?
- `plot.tryfail.02` Is any big problem solved on the first clever attempt?
- `plot.tryfail.03` Is it visible whether each failure comes from the character, the opposition, or both?
- `plot.tryfail.04` Do the failures differ in kind, not only in number?
- `plot.tryfail.05` If successes run in a long streak, are the stakes, the danger, and the competence strong enough to carry it?
- `plot.yesbut.01` Does each "but" or "and" grow out of the specific event before it?
- `plot.yesbut.02` Do the complications escalate in cost, or only change in kind?
- `plot.yesbut.03` Does each answer tell the reader something new about the character?
- `plot.yesbut.04` Are several plain wins in a row creating a lull?
- `plot.cheer.01` Name the promise this cheer moment pays off, and where it was made.
- `plot.cheer.02` What internal decision comes before the external win? The reverse order is fine when it reads better.
- `plot.cheer.03` If several plotlines resolve in one scene, does each get its own distinct beat?
- `plot.cheer.04` Is each payoff in a cascade larger than or different from the last, and not only louder?
- `plot.climax.01` Name each climax and what it pays off. Is an early one a plot payoff and the late one an emotional payoff?
- `plot.climax.02` If one viewpoint or plotline is far stronger than another, is strengthening the weaker one the fix?
- `plot.climax.03` Did early readers feel the real ending where you intended it?
- `plot.climax.04` Does the aftermath fit the format and deliver the last small promises?
- `plot.foreshadow.01` For each reveal that must feel earned, where does the reader get the first clue, and how many clues are there?
- `plot.foreshadow.02` Is the likely guess point a page or a paragraph before the reveal, and not "never" or "the first act"?
- `plot.foreshadow.03` If readers guess too early, would turning the twist into suspense serve better than hiding it harder?
- `plot.foreshadow.04` Does a shocking event serve theme, character, and plot, or only shock?
- `plot.layering.01` For each important scene, name the outer goal and the inner struggle. Does the outer obstacle press on the inner flaw?
- `plot.layering.02` Where was the change promised, and where is the first serious failure caused by the flaw?
- `plot.layering.03` How many chapters pass between inner-conflict beats? Look for long gaps.
- `plot.layering.04` Does the climax return to the early problem in a larger form?
- `plot.layering.05` Would a reader understand why the character behaves this way, in terms they recognize from real people?
- `plot.payoff.01` Which promise is being paid off, and where was it planted?
- `plot.payoff.02` At the moment of payoff, what does the reader currently believe will happen? If the answer is "exactly this", add deniability or let the promise fade first.
- `plot.payoff.03` If the promise is meant to be forgotten, is it planted clearly enough that it still reads as inevitable?
- `plot.payoff.04` Are the obstacles that create doubt honest, and not tricks that make the outcome impossible or the hero foolish?
- `plot.twist.01` What exactly did the story promise, and in which scene?
- `plot.twist.02` Where does the reader start to prefer the alternative? If nowhere, the twist is a surprise and not a swap.
- `plot.twist.03` Can you name two earlier moments that point to the real outcome?
- `plot.twist.04` Does the new outcome serve the theme and the character, or only startle?
- `character.scales.02` Which scale is lowest? A passive character needs a want and a first action, a cold one a reason to be liked, an unimpressive one something they are visibly good at.
- `character.proactive.01` What does the character want in their first scene, and does an action follow from it?
- `character.proactive.02` If the character reads as wooden, has the reader been shown what they want before the dialogue is blamed?
- `character.proactive.03` For a reluctant hero, where does the push land, and what small act of initiative comes before it?
- `character.proactive.04` Is the villain driving events while the hero only reacts?
- `character.proactive.05` When a motivation changes, is the new one established on the page?
- `character.relatable.01` Within the first chapters, what does the reader learn that makes them like or pity this character?
- `character.relatable.02` Does a trait carry the reader's sympathy, or is the narration telling them to feel it?
- `character.relatable.03` Is the likeable trait shown by action?
- `character.villain.01` Where does the villain sit on each scale? If low on proactive, why would they threaten anyone?
- `character.villain.02` Does the reader understand any of the villain's want?
- `character.villain.03` For an antihero, who is worse than them, and does the story show it?
- `character.dialogue.01` Can you say in one sentence what each speaker wants from the other?
- `character.dialogue.02` Does the refusal, or the compromise, come from the character's own nature, so a different character would have answered differently?
- `character.dialogue.03` Does each reveal about a character come through what they say and how they push, not through the narrator explaining?
- `character.dialogue.04` Is there something here for a side character to do beyond listening?
- `character.presenting.01` Can you name the character's motivation, how their personality goes after it, and what they will give up for it?
- `character.presenting.02` Does any character state their own motive to someone who already knows it?
- `character.presenting.03` With dialogue tags and setting removed, could a reader tell who is speaking from the lines alone?
- `character.presenting.04` Does each quirk reinforce a core trait, instead of sitting on top of it?
- `character.trait.01` List the traits the reader has seen for each recurring character. How many scenes in a row has one trait been the driver?
- `character.trait.02` What else does this character want, and has it ever competed with the trait?
- `character.trait.03` Could the trait be absent from a scene without breaking the character? If not, the trait is carrying too much.
- `character.arc.01` Does the reader see the flaw hurting the character before the lesson arrives?
- `character.arc.02` Is the decisive choice explained by who the character has become, not by how many times they have tried?
- `character.arc.03` In a downward arc, does the character know the flaw at the key moment? Constant arrogance that simply causes failure is a different, weaker shape.
- `character.capability.03` If the character fails nothing, where would a reader worry?
- `character.weakness.02` Is a limitation ever treated as a flaw the character should simply get over?
- `character.weakness.03` Does an unaddressed flaw block progress so long that readers lose patience?
- `character.background.01` Does the character have a goal and personality apart from the background?
- `character.background.02` Could any trait be swapped for a cliche from media? If so, replace it.
- `character.background.03` Are other members of the group shown with variety, if they appear?
- `character.background.04` Is the thing that makes the character different treated as a source of skill and difficulty, not just a label?
- `magic.first.01` Name the emotion the resolution should give, and ask whether the reader's understanding of the magic can support it.
- `magic.first.02` At the climax, could a reader have predicted the move from what they were shown? If they learn the rule only as it is used, expect a cheat reaction.
- `magic.first.03` If the magic is soft, does the resolution rest on what the characters do and want, not on the magic saving the day?
- `magic.first.04` If the magic is hard, were its pieces seeded earlier as tools that the characters now combine?
- `magic.second.02` If the first list is long and the others short, does the magic solve problems too easily?
- `magic.logic.04` Does the reader know something from real-world science that the characters cannot, making them look foolish?
- `worldbuilding.gorilla.01` List the most exciting elements in the book (a creature, a magic, a faction). Where does each first appear?
- `worldbuilding.gorilla.02` At that point, what thread is the reader following, and is the new element stronger than that thread? If so, raise the main thread, move the element, or cut it.
- `worldbuilding.gorilla.03` Does the new element serve the promise the reader is already holding, or create a rival one?
- `worldbuilding.gorilla.04` In the last quarter, does anything arrive that nobody has mentioned? A long-foreshadowed threat is fine; an unforeshadowed new problem is not.
- `worldbuilding.curve.01` Count the new proper names and terms in the first chapter. Which could wait?
- `worldbuilding.curve.02` For each paragraph of explanation, who is thinking it, and why now?
- `worldbuilding.curve.03` Is the learning curve steep on purpose, and does the opening promise that?
- `worldbuilding.filtered.01` Cover the name tags. Can you tell from the description who is looking and how they feel?
- `worldbuilding.filtered.02` Is each description a catalog of what exists, or a record of what this person notices?
- `worldbuilding.filtered.03` Across chapters in one location, does each opening notice something new?
- `worldbuilding.filtered.04` Do recurring features get a full description each time, where a line would do?
- `worldbuilding.pyramid.01` Find the most abstract paragraph (an explanation, a reflection, a cosmology). What concrete detail sits in the paragraphs just before and after it?
- `worldbuilding.pyramid.02` Does the scene use only sight? Add one or two other senses.
- `worldbuilding.pyramid.03` Is any concrete detail doing no work? When the image is irrelevant, a plain noun is enough.
- `worldbuilding.pyramid.04` Is a figure of speech colliding with the world, such as "he flew across the room" where people really fly?
- `worldbuilding.pyramid.05` Does a prologue about gods or cosmology give the reader no character and no scene?
- `scene.pov.01` Does the viewpoint mode fit the cast size and the information the story needs to withhold?
- `scene.pov.02` Within a scene, does the narration stay in one head, and is any switch deliberate and clear to the reader?
- `scene.pov.03` In true omniscient, is information withheld in a way that will feel like a cheat? Lean on suspense instead.
- `scene.pov.04` Does any change of tense or mode mid-book have a reason the reader can see?
- `scene.sequel.01` After each scene that ends with a change, is there a sequel where the characters take in the result, sized to the pace you want?
- `scene.sequel.02` Is a dragging stretch a run of sequels with no scene between them?
- `scene.sequel.03` Is a numbing stretch a run of scenes with no sequel to feel the consequences?
- `scene.sequel.04` Does each sequel carry something (a revelation, a joke, a relationship beat), and does its decision launch the next scene?
- `scene.show.01` For each stated trait or emotion, does it matter enough to the story to be shown? If yes, find one specific action or detail; if no, leave the plain statement.
- `scene.show.02` Is a minor point being proved at length, such as a passing trait or a one-time character given a dramatized scene?
- `scene.show.03` Is the first appearance of anything the reader must remember shown, not only stated?
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
- `prose.tells.16` Stock body reactions (weak alone).
- `prose.tells.17` Stock atmosphere lines (weak alone).
- `prose.tells.18` Tag and gesture filler between lines of dialogue (weak alone).
- `prose.tells.19` Stacked similes (weak alone).
- `prose.tells.20` One register for every speaker (weak alone; whole-chapter pass only).
- `prose.tells.21` Lines that answer each other in tidy pairs, often echoing the last line's wording.
- `prose.tells.22` A cornered character explains their position in a tidy speech that briefs the reader.
- `foundations.feedback.01` Is each note descriptive (what the reader felt, and where) instead of prescriptive (how to fix it)?
- `foundations.feedback.02` Does each note point to a specific place in the text?
- `foundations.feedback.03` Does any suggestion come from the reviewer's taste instead of the book's own promises?
- `foundations.readers.01` Across readers, which reactions form a pattern (several readers stalling or lost in the same place), and which are single data points?
- `foundations.readers.02` For each pattern, what is the cause in the story, as opposed to the fix a reader suggested?

Skill for each check family: `character.entry` character-first-entry; `scene.access` scene-access-limits; `plot.bridges` plot-causal-bridges; `plot.reveals` plot-reveal-boundaries; `scene.dialogue` scene-dialogue-behavior; `plot.ppp` plot-promise-progress-payoff; `plot.promises` plot-kinds-of-promises; `plot.bigp` plot-big-p-little-p; `plot.progress` plot-types-of-progress; `plot.coldopen` plot-cold-open-microcosm; `plot.threeact` plot-three-act-structure; `plot.tryfail` plot-try-fail-cycle; `plot.yesbut` plot-yes-but-no-and; `plot.cheer` plot-cheer-moment-sanderlanche; `plot.climax` plot-climax-placement-aftermath; `plot.foreshadow` plot-foreshadowing-twists; `plot.layering` plot-layering-conflict; `plot.payoff` plot-payoff-deniability-forgotten-promise; `plot.twist` plot-twists-promise-and-wish; `character.scales` character-proactive-relatable-capable; `character.proactive` character-proactivity-toolkit; `character.relatable` character-relatability-toolkit; `character.villain` character-villain-and-antihero-patterns; `character.dialogue` character-floating-outline-for-dialogue; `character.presenting` character-presenting-a-character; `character.trait` character-overused-trait-trap; `character.arc` character-arc-types; `character.capability` character-capability-design; `character.weakness` character-flaws-restrictions-limitations; `character.background` character-writing-unfamiliar-backgrounds; `magic.first` magic-first-law; `magic.second` magic-second-law; `magic.logic` magic-internal-and-external-logic; `worldbuilding.gorilla` worldbuilding-gorilla-in-the-phone-booth; `worldbuilding.curve` worldbuilding-learning-curve-and-exposition; `worldbuilding.filtered` worldbuilding-viewpoint-filtered-description; `worldbuilding.pyramid` worldbuilding-pyramid-of-abstraction; `scene.pov` viewpoint-and-tense; `scene.sequel` scene-and-sequel; `scene.show` show-dont-tell; `prose.tells` prose-ai-tells; `foundations.feedback` foundations-writing-group-rules; `foundations.readers` foundations-alpha-beta-readers.
<!-- generated:checks:end -->
