---
name: story-worldbuild
metadata:
  type: workflow
description: >
  Use to design or stress-test magic, powers, or world rules. Builds an ability table of costs, limits, and counters, hunts exploits, and tests what-ifs. Saves rules only after approval.
---

# Story worldbuild

Build the part of the world the story needs, and test it the way a game designer tests a ruleset: a system the story can lean on without cheating. A world is a means to a story, so stop when the story has what it needs.

## Before you start

Read the settings for the craft language, the project's own rules for where world notes live, and what exists in `kb/` and the spec. Work with an existing world; never start over. Ask what the writer has (a magic idea, a setting, a character, only a feeling) and what story they hope to tell, even loosely.

## Build

1. **Sort the ideas** into setting, character, and plot, find the holes, and combine ideas across them. Ask only about the gaps the story needs.
2. **Cover the three parts** (physical setting, cultural setting, magic) at the depth the story will use. Follow the chains of consequence between them.
3. **Set the dial** from mysterious to rule-bound, and say what each end lets the story do. A deliberately mysterious system is a valid choice: then it must not solve the plot.
4. **The ability table**, for anything with rules:

   | Ability | What it does | What it costs | What stops it | What counters it |
   | --- | --- | --- | --- | --- |

   Fill it from the writer's ideas. Where a column is empty, offer two or three options to choose from.

## Test

- **Balance pass.** Run the craft checks below that fit, and report each finding as a plain question and answer with a fix: an ability that solves too much, a cost that does not hurt, a limit that does not bite, a system growing wider instead of deeper, a climax that could be won with something the reader has not seen.
- **Exploit hunt.** Try to break it. List the most dangerous ways a clever character could abuse the rules: skipping a cost, an infinite loop, making an enemy irrelevant, solving the plot in one move. For each, offer a patch, or a way to use the exploit as a plot hook.
- **What-ifs.** Three or four scenarios of three to five lines: two users clash, a villain uses it, someone reaches the limit. Show the outcomes and let the writer adjust.
- **How much to build.** Separate what needs depth from what needs only a hint, and say when a detail will never reach the page. If the writer has been building for a long time without a story, say so kindly and set a stopping point.

## Record

Only what the writer approves: rules on `kb/world/<system>.md` (one system per page), terms in `kb/vocab.md`, rejected options in `work/brainstorm/`. In conversation, use the craft language the settings name and never show check IDs. Then name the next step (usually `story-develop` or `story-plan`) and stop. No scenes and no plot here.

<!-- generated:checks:start -->
## Craft checks (generated)

Apply each check that fits this story. In the files you write (beats, reports, notes), record its ID with a short note of what it found in this story, or `n/a` with a reason. Never show IDs or skill names to the writer: in conversation, ask or say the substance in the craft language the settings name. A deliberate break of a framework is a valid answer, not a defect: say it is deliberate and do not push the story back toward the formula. Load the named skill only when you need its full reasoning.

- `magic.first.01` Name the emotion the resolution should give, and ask whether the reader's understanding of the magic can support it. (`magic-first-law`)
- `magic.first.02` At the climax, could a reader have predicted the move from what they were shown? If they learn the rule only as it is used, expect a cheat reaction. (`magic-first-law`)
- `magic.first.03` If the magic is soft, does the resolution rest on what the characters do and want, not on the magic saving the day? (`magic-first-law`)
- `magic.first.04` If the magic is hard, were its pieces seeded earlier as tools that the characters now combine? (`magic-first-law`)
- `magic.hardsoft.01` For each magical element, could a reader predict what it will do and what it cannot do? Place each element separately. (`magic-hard-and-soft`)
- `magic.hardsoft.02` Does each element's place on the spectrum fit its job: problem-solving and training for hard magic, wonder and lack of control for soft? (`magic-hard-and-soft`)
- `magic.hardsoft.03` Across a series, are earlier inventions' consequences remembered, or is the drift toward softness chosen on purpose? (`magic-hard-and-soft`)
- `magic.logic.01` Are the internal rules written in plain story terms a reader could use without any science? (`magic-internal-and-external-logic`)
- `magic.logic.02` Would the story still work if the external explanation vanished? If so, it is flavor, not rules. (`magic-internal-and-external-logic`)
- `magic.logic.03` Is any system called hard because of its vocabulary, not because of what a reader can predict? (`magic-internal-and-external-logic`)
- `magic.logic.04` Does the reader know something from real-world science that the characters cannot, making them look foolish? (`magic-internal-and-external-logic`)
- `magic.second.01` List what the magic can do, what it costs the user, and what stops it, including who or what is stronger. (`magic-second-law`)
- `magic.second.02` If the first list is long and the others short, does the magic solve problems too easily? (`magic-second-law`)
- `magic.second.03` Do the most interesting scenes come from the costs and the limits? (`magic-second-law`)
- `magic.second.04` Is each power described with rules specific enough to make a tactical puzzle, not a generic effect? (`magic-second-law`)
- `magic.third.01` Before adding a new element, could something already in the story do this job: a changed rule, a second use of an existing magic, a branch of an existing group? (`magic-third-law`)
- `magic.third.02` For each core rule, have its consequences for economy, war, family, religion, or crime been followed? (`magic-third-law`)
- `magic.third.03` If a new element is added, is it linked to something already on the page? (`magic-third-law`)
- `magic.zeroth.01` For the elements of the world you are most excited about, what is the one-sentence in-world reason each one exists? (`magic-zeroth-law`)
- `magic.zeroth.02` For the elements that exist only because they are realistic, would something more striking serve the story as well? (`magic-zeroth-law`)
- `worldbuilding.ideas.01` Can you name at least two ideas in each column that you are excited about? (`worldbuilding-idea-intersection`)
- `worldbuilding.ideas.02` For each setting idea, is there a character or plot idea that presses on it? (`worldbuilding-idea-intersection`)
- `worldbuilding.ideas.03` Is any idea just sitting there, affecting nothing else? Either connect it or save it for another book. (`worldbuilding-idea-intersection`)
- `worldbuilding.ideas.04` Do your own fascinations and expertise show up somewhere? (`worldbuilding-idea-intersection`)
- `worldbuilding.split.01` Does each part (physical setting, cultural setting, magic) hold the items your characters will actually run into? (`worldbuilding-three-part-split`)
- `worldbuilding.split.02` Does a change in one part ripple through the others, such as food customs into manners or materials into architecture? (`worldbuilding-three-part-split`)
- `worldbuilding.split.03` Do the chosen items make each other more interesting, with everything else left vague on purpose? (`worldbuilding-three-part-split`)
- `worldbuilding.iceberg.01` Is worldbuilding keeping you from drafting, measured against your own deadline? (`worldbuilding-hollow-iceberg`)
- `worldbuilding.iceberg.02` Is each piece of world detail on the page there because it supports stakes, character, or plot, or because you invested time in it? (`worldbuilding-hollow-iceberg`)
- `worldbuilding.iceberg.03` Is the world built deeply only where it shapes choices and plot, with a passing hook for everything else? (`worldbuilding-hollow-iceberg`)
- `worldbuilding.naming.01` Search the name. Does it accidentally make a real word, in the source language or another one? (`worldbuilding-naming`)
- `worldbuilding.naming.02` Is it, or does it contain, a slur or swear word in a language your readers are likely to know? (`worldbuilding-naming`)
- `worldbuilding.naming.03` Has someone who knows the source region or language looked at it? (`worldbuilding-naming`)
- `worldbuilding.naming.04` Does it trigger a different mythology or brand than you meant, for people who have not seen the project? (`worldbuilding-naming`)
- `worldbuilding.naming.05` Does it collide with a huge, famous work? A small overlap with an obscure one rarely matters. (`worldbuilding-naming`)
- `worldbuilding.disease.01` How many months since you began building, and what have you written in the story itself? (`worldbuilding-worldbuilders-disease`)
- `worldbuilding.disease.02` For the last five things you built, can you name a scene or decision they affect? (`worldbuilding-worldbuilders-disease`)
- `worldbuilding.disease.03` Is the next worldbuilding task something the draft needs, or something you enjoy more than drafting? (`worldbuilding-worldbuilders-disease`)
- `worldbuilding.gorilla.01` List the most exciting elements in the book (a creature, a magic, a faction). Where does each first appear? (`worldbuilding-gorilla-in-the-phone-booth`)
<!-- generated:checks:end -->
