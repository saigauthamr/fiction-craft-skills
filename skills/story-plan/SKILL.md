---
name: story-plan
metadata:
  type: workflow
description: >
  Use for a story spec, chapter beats, an outline, or a promise ledger. Drafts plans when the AI owns planning and coaches when the writer does; records craft-check evidence and saves only after approval.
---

# Story plan

Two documents: the **spec**, which records what is settled about the whole story, and the **beats**, one file per chapter saying what each chapter does. Both are saved only after the writer approves them. Planning records decisions; it does not make them for the writer.

## Before you start

1. **Read the settings** in the project's Story project block: who owns planning, and how much craft language to use. No valid block: plan as if the writer owns it, and mention `story-onboard`.
2. **Read the project's own rules** in its instructions file. A spec format, a folder, chapter numbering, a naming pattern, or several voice files per part of the book all take priority over the defaults here.
3. **Read what exists**: `work/brainstorm/develop-summary.md` and the decisions list if there is one, `kb/vocab.md`, the `kb/` pages the plan needs (in a large knowledge base, read its index first), and any existing spec and beats.
4. If almost nothing is settled, say so and recommend `story-develop` first. A plan built on guesses is worse than none.

## Who does the planning

- **The AI owns planning.** Draft the document, show it, take corrections, and save it only after the writer approves.
- **The writer owns planning.** Do not write the plan for them. Offer the template below, ask the questions the checks raise, and when they have written it (or dictated it, which you record in their words, adding nothing), check it and report what you found. Save their words, not yours.

## The spec

Sections: premise (the book in one or two sentences, then what happens chapter to chapter if the writer has said), promises, characters (want, need, what stops them, where they sit on the three scales; link their `kb/` pages), rules of the world (costs and limits included), progress (the kind the story measures, and its soul), arcs, ending (what it must pay off and how it should feel), and open questions. Leave out a section the story does not need.

Every line is one of three kinds:

- **Settled**: the writer said it or it is in `kb/`. Unmarked.
- **Proposed**: you inferred or suggested it. Start the line with "Proposed:".
- **Open**: nobody has decided. List it under open questions.

Never present a proposal as settled, and never fill a gap to make a section look complete.

**The promise ledger.** With the spec, keep `work/spec/promise-ledger.md`: one entry per promise the story makes, with where it is made, where it advances, and where it pays off. If the project already tracks promises its own way, follow that and skip the format below. Otherwise write one line per promise: `- P03 | planted ch2 | open | the promise in a few words`. The status is `open` (made, not yet moved), `advanced` (moved on the page, not paid), `paid`, or `dropped` (given up on purpose, with the reason in the text). `planted` is the chapter that makes it, or for a promise not yet written the chapter the beats plan it for. A promise with no payoff is either a gap to list or a deliberate choice to note as `dropped`, with why.

## The beats

Ask how far to plan: the whole book, one part, or the next few chapters (the default for a writer who discovers the story is a few chapters). One file per chapter in `work/beats/`, named `NNN-slug.md` unless the project names a pattern:

- **Dateline or header**, if the project's chapters open with one.
- **Chapter goal**: what this chapter changes, in one sentence.
- **Viewpoint and tense**, and which voice file applies, if it varies.
- **Promises carried**: which promises from the ledger it makes, advances, or pays off.
- **Scenes**, in order: who wants what, what stands in the way, how it turns out.
- **Turn (a note for the writer, not a line for the page)**: what each scene means for the story. Whoever drafts uses it to aim the scene and never states it in the prose.
- **Hook out**.
- **Facts to check**: the `kb/` pages the draft will lean on.
- **Checks applied**: one line per applicable check from the beats list below, `<id>: <what it found in this chapter>`, or `<id>: n/a, <reason>`, or `<id>: deliberate, <what the story is doing instead>`.

In saved files, spell out each complete check ID on its own line; do not use ranges or family-only labels.

Keep a chapter's beats to about a page. Update the promise ledger as beats are planned.

## Before showing a plan

Run the checks for the document (below). Every applicable check gets a specific note about this story or `n/a` with a reason; a note that would fit any story is not a check. Then show the writer what you found: coverage gaps in the ledger, scenes that carry no promise, a middle that repeats itself, a length that does not fit, and anything contradicting `kb/`. Say what you fixed and what needs their decision.

## Confirming and changing

Show the document (section by section if it is long), point out every proposal, gap, and open question, and take corrections. Save only after the writer approves. A saved plan can change later: show the change as a diff, add a line to a "Changes" list at the bottom saying what changed and why, and name the beats and drafts it touches.

Say what comes next (beats after a spec, drafting after beats) and stop.

<!-- generated:checks:start spec -->
## Craft checks: spec (generated)

Apply each check that fits this story. In the files you write (beats, reports, notes), record its ID with a short note of what it found in this story, or `n/a` with a reason. Never show IDs or skill names to the writer: in conversation, ask or say the substance in the craft language the settings name. A deliberate break of a framework is a valid answer, not a defect: say it is deliberate and do not push the story back toward the formula. Load the skill listed for a check's family (after the list) only when you need its full reasoning.

- `plot.bridges.01` For each major turn, can you name the pressure, the actor who interprets it, their goal, and their method?
- `plot.bridges.02` Why this person, why now, and why this method?
- `plot.bridges.05` Is every place, group, or person established before it carries an event?
- `plot.reveals.01` For each secret, is the true fact written down apart from what the reader is told?
- `plot.reveals.02` For each secret, can you name who knows it, who is wrong about it, where the reader gets the first clue, and where they learn it?
- `plot.reveals.03` Does any reveal come before its setup, or any setup go unrewarded?
- `plot.reveals.04` Does narration leak author truth the viewpoint character could not know?
- `plot.reveals.05` Does the outline tell the causal story before explaining the hidden system?
- `plot.bigp.01` State the Big P Plot in one or two sentences. If you cannot, the book is not focused yet.
- `plot.bigp.03` Where does the story's emotional core actually live, in the headline plot or in a little p thread, and do the signposts follow it?
- `plot.promises.01` Which kinds of promise does the opening make (tone, plot, character, series), and which does it skip? Not every kind is required; mark each skip as deliberate or accidental.
- `plot.promises.02` From the first pages, could a reader say what feel to expect and what the main character wants?
- `plot.promises.03` Does the character promise show what the character wants, what they need, and why they cannot have it yet?
- `plot.promises.04` If the tone will switch (for example from thriller to travelogue), is the second tone promised at the start?
- `plot.promises.05` Does each new character, sequence, or chapter make its own small promise, and does the chapter signal it was delivered?
- `plot.progress.01` Name the kind of progress the story measures (information, relationship, skill, distance, or another) and check that the climax resolves that kind.
- `plot.progress.02` With several threads, name the soul of the story, the thread that drives the ending, and check that the climax turns on it and not on the trappings.
- `plot.archetypes.01` Name the archetypes the story layers, and which one carries the Big P Plot.
- `plot.archetypes.02` For each arc, has the story decided whether it heads for success or failure, and promised accordingly?
- `plot.archetypes.03` If the dominant archetype shifts midway, is the shift foreshadowed, and does it reuse the earlier archetype's setup?
- `plot.archetypes.04` For a betrayal, list the three or four moments where the betrayer's goal visibly diverges. Each should read as innocent on a first pass and damning on a second.
- `plot.scale.01` Does the central conflict fit the word count for the format and genre?
- `plot.scale.02` If the book is long, where does the scope widen, and is the widening signposted?
- `plot.cheer.01` Name the promise this cheer moment pays off, and where it was made.
- `plot.layering.02` Where was the change promised, and where is the first serious failure caused by the flaw?
- `plot.cycles.01` Does every cycle have a payoff, with visible progress between its promise and its payoff?
- `plot.cycles.04` Is every promised thread present in the merged outline?
- `plot.payoff.01` Which promise is being paid off, and where was it planted?
- `plot.twist.01` What exactly did the story promise, and in which scene?
- `plot.circle.01` Mark which steps of the circle are present. For each missing step, decide whether it is missing on purpose.
- `plot.circle.02` Name the character's growth circle separately from the external goal, and check that the signposts track the growth.
- `plot.circle.03` If a step stopped fitting the story, was it dropped instead of forced?
- `plot.circle.04` If the story ends tragically, which step does the character refuse, and what flaw drives the refusal?
- `character.scales.01` Place the character low, middle, or high on proactive, relatable, and capable, per domain where it matters.
- `character.scales.02` Which scale is lowest? A passive character needs a want and a first action, a cold one a reason to be liked, an unimpressive one something they are visibly good at.
- `character.scales.03` Which scale does the character's arc move along, and is the movement shown on the page?
- `character.scales.04` Is any character high on all three scales with nowhere left to go?
- `character.motivation.01` Can you name what the character wants, why they cannot have it, what they need, and what they must sacrifice?
- `character.motivation.02` Does each choice on the page follow the pattern of those answers, and where it breaks, does the text show why?
- `character.motivation.03` Do at least two of the character's answers conflict, giving scenes something to turn on?
- `character.arc.04` Can you name which of the four shapes each major character is on, or say that they have none?
- `character.villain.01` Where does the villain sit on each scale? If low on proactive, why would they threaten anyone?
- `character.villain.02` Does the reader understand any of the villain's want?
- `character.villain.03` For an antihero, who is worse than them, and does the story show it?
- `character.weakness.01` For each weakness, is it a flaw, a restriction, or a limitation, and is it handled that way: an arc for a flaw, pressure scenes for a restriction, ingenuity for a limitation?
- `character.weakness.02` Is a limitation ever treated as a flaw the character should simply get over?
- `character.weakness.03` Does an unaddressed flaw block progress so long that readers lose patience?
- `character.weakness.04` For a very strong character, which restriction or limitation bears on what the plot demands?
- `character.capability.01` Name the one or two things this character does better than anyone else in the story. Where does the plot use them?
- `character.capability.02` Name two things they do badly. Where does the plot punish that?
- `character.iconic.01` Can a new reader start with this installment and follow the character? If yes, the traits are stable and clear enough.
- `character.iconic.02` Is the tension coming from a capable opponent or a real cost? If neither, the story has no engine, since the arc was removed.
- `character.iconic.03` Is any small arc inside this one story kept from becoming central to who the character is?
- `character.iconic.04` Is the lead memorable through a clear trait, voice, or signature skill?
- `magic.first.01` Name the emotion the resolution should give, and ask whether the reader's understanding of the magic can support it.
- `magic.second.01` List what the magic can do, what it costs the user, and what stops it, including who or what is stronger.
- `magic.second.02` If the first list is long and the others short, does the magic solve problems too easily?
- `magic.second.03` Do the most interesting scenes come from the costs and the limits?
- `magic.second.04` Is each power described with rules specific enough to make a tactical puzzle, not a generic effect?
- `magic.hardsoft.01` For each magical element, could a reader predict what it will do and what it cannot do? Place each element separately.
- `magic.hardsoft.02` Does each element's place on the spectrum fit its job: problem-solving and training for hard magic, wonder and lack of control for soft?
- `magic.hardsoft.03` Across a series, are earlier inventions' consequences remembered, or is the drift toward softness chosen on purpose?
- `worldbuilding.curve.03` Is the learning curve steep on purpose, and does the opening promise that?
- `scene.pov.01` Does the viewpoint mode fit the cast size and the information the story needs to withhold?
- `scene.pov.03` In true omniscient, is information withheld in a way that will feel like a cheat? Lean on suspense instead.

Skill for each check family: `plot.bridges` plot-causal-bridges; `plot.reveals` plot-reveal-boundaries; `plot.bigp` plot-big-p-little-p; `plot.promises` plot-kinds-of-promises; `plot.progress` plot-types-of-progress; `plot.archetypes` plot-archetypes; `plot.scale` plot-scale-of-plot; `plot.cheer` plot-cheer-moment-sanderlanche; `plot.layering` plot-layering-conflict; `plot.cycles` plot-outline-interwoven-cycles; `plot.payoff` plot-payoff-deniability-forgotten-promise; `plot.twist` plot-twists-promise-and-wish; `plot.circle` plot-story-circle; `character.scales` character-proactive-relatable-capable; `character.motivation` character-motivation-discovery-questions; `character.arc` character-arc-types; `character.villain` character-villain-and-antihero-patterns; `character.weakness` character-flaws-restrictions-limitations; `character.capability` character-capability-design; `character.iconic` character-iconic-characters; `magic.first` magic-first-law; `magic.second` magic-second-law; `magic.hardsoft` magic-hard-and-soft; `worldbuilding.curve` worldbuilding-learning-curve-and-exposition; `scene.pov` viewpoint-and-tense.
<!-- generated:checks:end spec -->

<!-- generated:checks:start beats -->
## Craft checks: beats (generated)

Apply each check that fits this story. In the files you write (beats, reports, notes), record its ID with a short note of what it found in this story, or `n/a` with a reason. Never show IDs or skill names to the writer: in conversation, ask or say the substance in the craft language the settings name. A deliberate break of a framework is a valid answer, not a defect: say it is deliberate and do not push the story back toward the formula. Load the skill listed for a check's family (after the list) only when you need its full reasoning.

- `plot.bridges.01` For each major turn, can you name the pressure, the actor who interprets it, their goal, and their method?
- `plot.bridges.02` Why this person, why now, and why this method?
- `plot.bridges.03` If this event were removed, would the next decision change? If not, it is off the spine or a bridge is missing.
- `plot.bridges.04` Does any turn rest on a summary jump (A happened, so B) with no one choosing?
- `plot.bridges.05` Is every place, group, or person established before it carries an event?
- `scene.access.04` Is each consequential choice made by the character who owns that decision, and does it follow from what they perceived or misread?
- `character.entry.01` At first entry, has the prose shown the character's role or identity, or has only the author known it?
- `character.entry.02` Is the character's link to the current event or to the viewpoint character clear?
- `scene.dialogue.03` Is any procedural action (opening, reading, moving things) connected to human pressure, or is the scene static with props?
- `plot.ppp.02` For this stretch, name what tells the reader the story is moving toward one of those promises. A stretch with no signpost reads as a stall.
- `plot.bigp.02` For each chapter, name its little p plot and whether it advances a Big P promise or makes a promise of its own that the book keeps.
- `plot.progress.03` For this sequence, what does the reader think it is moving toward, and what signals tell them so?
- `plot.progress.04` Does the pace vary, with breathers between pushes, and are time skips set up at a structural break?
- `plot.coldopen.01` Can the opening be described as a small version of the book's central conflict? If not, are a tone promise and a likable character with a hard problem doing that work instead?
- `plot.coldopen.02` Does the full book echo the opening's shape, or deliberately break it?
- `plot.coldopen.03` Does the opening make a promise the book keeps?
- `plot.threeact.01` Write the major dramatic question in one sentence. Is it posed by the end of Act I, and does the climax answer it?
- `plot.threeact.02` Name the point after which the character cannot go back.
- `plot.threeact.03` Does the midpoint change what the reader believes the story is about, escalate it, or make it personal?
- `plot.threeact.04` Does each attempt in the second act make things worse, or do the attempts merely repeat?
- `plot.threeact.05` Is there a low point that the last realization climbs out of?
- `plot.tryfail.01` For each major success, what failed before it, and did the failure cost something or teach something?
- `plot.tryfail.02` Is any big problem solved on the first clever attempt?
- `plot.tryfail.03` Is it visible whether each failure comes from the character, the opposition, or both?
- `plot.tryfail.05` If successes run in a long streak, are the stakes, the danger, and the competence strong enough to carry it?
- `plot.yesbut.01` Does each "but" or "and" grow out of the specific event before it?
- `plot.yesbut.02` Do the complications escalate in cost, or only change in kind?
- `plot.cheer.02` What internal decision comes before the external win? The reverse order is fine when it reads better.
- `plot.cheer.03` If several plotlines resolve in one scene, does each get its own distinct beat?
- `plot.cheer.04` Is each payoff in a cascade larger than or different from the last, and not only louder?
- `plot.climax.01` Name each climax and what it pays off. Is an early one a plot payoff and the late one an emotional payoff?
- `plot.climax.02` If one viewpoint or plotline is far stronger than another, is strengthening the weaker one the fix?
- `plot.climax.04` Does the aftermath fit the format and deliver the last small promises?
- `plot.foreshadow.01` For each reveal that must feel earned, where does the reader get the first clue, and how many clues are there?
- `plot.foreshadow.02` Is the likely guess point a page or a paragraph before the reveal, and not "never" or "the first act"?
- `plot.foreshadow.03` If readers guess too early, would turning the twist into suspense serve better than hiding it harder?
- `plot.layering.01` For each important scene, name the outer goal and the inner struggle. Does the outer obstacle press on the inner flaw?
- `plot.layering.03` How many chapters pass between inner-conflict beats? Look for long gaps.
- `plot.layering.04` Does the climax return to the early problem in a larger form?
- `plot.cycles.02` Do the big payoffs land one after another, not all at once?
- `plot.cycles.03` Is any minor character's cycle better resolved earlier, so it does not compete with the lead at the climax?
- `plot.payoff.01` Which promise is being paid off, and where was it planted?
- `plot.payoff.02` At the moment of payoff, what does the reader currently believe will happen? If the answer is "exactly this", add deniability or let the promise fade first.
- `plot.payoff.03` If the promise is meant to be forgotten, is it planted clearly enough that it still reads as inevitable?
- `plot.payoff.04` Are the obstacles that create doubt honest, and not tricks that make the outcome impossible or the hero foolish?
- `plot.twist.01` What exactly did the story promise, and in which scene?
- `plot.twist.02` Where does the reader start to prefer the alternative? If nowhere, the twist is a surprise and not a swap.
- `plot.twist.03` Can you name two earlier moments that point to the real outcome?
- `plot.twist.04` Does the new outcome serve the theme and the character, or only startle?
- `plot.scale.03` Where can a reader put the book down, and what pulls them back?
- `character.arc.01` Does the reader see the flaw hurting the character before the lesson arrives?
- `character.arc.02` Is the decisive choice explained by who the character has become, not by how many times they have tried?
- `character.proactive.03` For a reluctant hero, where does the push land, and what small act of initiative comes before it?
- `character.proactive.04` Is the villain driving events while the hero only reacts?
- `character.dialogue.01` Can you say in one sentence what each speaker wants from the other?
- `magic.first.02` At the climax, could a reader have predicted the move from what they were shown? If they learn the rule only as it is used, expect a cheat reaction.
- `magic.first.03` If the magic is soft, does the resolution rest on what the characters do and want, not on the magic saving the day?
- `magic.first.04` If the magic is hard, were its pieces seeded earlier as tools that the characters now combine?
- `worldbuilding.gorilla.01` List the most exciting elements in the book (a creature, a magic, a faction). Where does each first appear?
- `worldbuilding.gorilla.02` At that point, what thread is the reader following, and is the new element stronger than that thread? If so, raise the main thread, move the element, or cut it.
- `worldbuilding.gorilla.03` Does the new element serve the promise the reader is already holding, or create a rival one?
- `worldbuilding.gorilla.04` In the last quarter, does anything arrive that nobody has mentioned? A long-foreshadowed threat is fine; an unforeshadowed new problem is not.
- `scene.sequel.01` After each scene that ends with a change, is there a sequel where the characters take in the result, sized to the pace you want?
- `scene.sequel.02` Is a dragging stretch a run of sequels with no scene between them?
- `scene.sequel.03` Is a numbing stretch a run of scenes with no sequel to feel the consequences?
- `scene.sequel.04` Does each sequel carry something (a revelation, a joke, a relationship beat), and does its decision launch the next scene?

Skill for each check family: `plot.bridges` plot-causal-bridges; `scene.access` scene-access-limits; `character.entry` character-first-entry; `scene.dialogue` scene-dialogue-behavior; `plot.ppp` plot-promise-progress-payoff; `plot.bigp` plot-big-p-little-p; `plot.progress` plot-types-of-progress; `plot.coldopen` plot-cold-open-microcosm; `plot.threeact` plot-three-act-structure; `plot.tryfail` plot-try-fail-cycle; `plot.yesbut` plot-yes-but-no-and; `plot.cheer` plot-cheer-moment-sanderlanche; `plot.climax` plot-climax-placement-aftermath; `plot.foreshadow` plot-foreshadowing-twists; `plot.layering` plot-layering-conflict; `plot.cycles` plot-outline-interwoven-cycles; `plot.payoff` plot-payoff-deniability-forgotten-promise; `plot.twist` plot-twists-promise-and-wish; `plot.scale` plot-scale-of-plot; `character.arc` character-arc-types; `character.proactive` character-proactivity-toolkit; `character.dialogue` character-floating-outline-for-dialogue; `magic.first` magic-first-law; `worldbuilding.gorilla` worldbuilding-gorilla-in-the-phone-booth; `scene.sequel` scene-and-sequel.
<!-- generated:checks:end beats -->
