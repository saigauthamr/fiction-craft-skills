---
name: story-develop
metadata:
  type: workflow
description: >
  Use to grill a story idea, poke holes in a premise, or decide the story before planning. Asks questions or offers choices according to who leads, records settled decisions, and ends with a summary for confirmation.
---

# Story develop

Sharpen a story idea until nothing important is left assumed. The writer decides; you ask, recommend, and keep the record. Do not write prose, a spec, or beats here; `story-plan` writes the spec afterward.

## Before the first question

1. **Read the settings** in the project's instructions file (the Story project block): who owns planning, and how much craft language to use. If there is no valid block, work as if the writer leads and uses full craft terms, and mention that `story-onboard` can set this up.
2. **Read the project's own rules** in the instructions file and any `kb/README.md`. If they name where decisions, terms, or open questions go, use those places; the locations below are only defaults. Never create a second register.
3. **Read what exists**: `kb/vocab.md`, the `kb/` pages, `work/spec/`, `work/brainstorm/`. Never ask about something already written down. If the story is already worked out, say in three lines what is settled and ask only about what the project leaves open.

## Two ways to run it

**When the writer owns planning: questions.** Work the idea as a tree. Find the frontier (every open question whose prerequisites are settled) and ask it in one round, numbered, with your recommended answer and one line of why for each:

```
Q1 - <short title>: <the question, with options if there are any>
Recommended: <your answer, and why>
```

Wait for the answers, recompute the frontier, and ask the next round. If the writer discovers the story as they write, ask only what the story cannot do without (the premise, what the main character wants, what the opening promises) and record the rest as open.

**When the AI owns planning: choices.** Run rounds of at most four choices, each with a recommended default and one line on what each option does to the story, so the writer can answer with a number or "go". The usual order is the idea (restate theirs, or offer three two-line premises), tone and how much danger is real, the main character, the central problem or power and what it costs, the opposing force with a plan of its own, and how the ending should feel. Skip any round they have already answered. Fill in what they do not care about (names, minor characters, texture) and list it under "Defaults I picked" for them to veto. Anything touching the plot, the rules, a motive, a relationship, or the ending needs their explicit choice. When they say "use the defaults", those are your choices, not theirs: mark them as yours.

After a round about rules or characters, offer once: "Want to tinker with this? Say 'lab'." Send rules and powers to `story-worldbuild`, characters to `story-cast`. Never push it.

## What to ask about

Shape the questions with the craft checks listed under "Craft checks" below, not generic prompts. With `craft-language: full`, name the idea you are using ("the character promise", "the Big P Plot"); with `brief`, add a one-line explanation; with `none`, ask the plain question and name nothing. Never show skill names to the writer.

## Language and contradictions

- When the writer uses a story term loosely, or two terms for one thing, stop and settle it: "You've called it both a marker and a buoy. Are they the same?"
- When something they say contradicts the project, say so at once and ask which is right.
- Test boundaries with a concrete scenario: "If a marker fixes a channel's route, what happens when the tide has already moved it?"

## Record as you go

Write each answer down when it is settled, not at the end. The writer settling it is the approval; your defaults are not settled until the writer approves them.

- **Terms**: an entry in `kb/vocab.md` with the canonical name, a short definition, and aliases. No record of where or when it was decided.
- **Facts about people, places, rules, events**: the matching `kb/` page, one concept per page. When a placeholder name is settled, rename the page and update every mention.
- **Decisions about the book itself** (genre, tone, form, what it is about, its promises): a running list in `work/brainstorm/develop-decisions.md`, not `kb/`.
- **Open questions and rejected options**: the project's own register, or `work/brainstorm/` if it has none.

Never record a guess or a rule the writer did not state.

## Finishing

The session is done when the frontier is empty: every branch visited, nothing silently assumed.

1. Summarize: the premise in a sentence or two, the settled decisions, your defaults still awaiting a yes, and the open questions.
2. Ask the writer to confirm. If they disagree, treat it as new answers and keep going.
3. After they confirm, save the summary to `work/brainstorm/develop-summary.md` and record any defaults they approved.
4. Name the next step: the spec, with `story-plan`. Do not start it.

<!-- generated:checks:start -->
## Craft checks (generated)

Apply each check that fits this story. In the files you write (beats, reports, notes), record its ID with a short note of what it found in this story, or `n/a` with a reason. Never show IDs or skill names to the writer: in conversation, ask or say the substance in the craft language the settings name. A deliberate break of a framework is a valid answer, not a defect: say it is deliberate and do not push the story back toward the formula. Load the named skill only when you need its full reasoning.

- `plot.bigp.01` State the Big P Plot in one or two sentences. If you cannot, the book is not focused yet. (`plot-big-p-little-p`)
- `plot.promises.01` Which kinds of promise does the opening make (tone, plot, character, series), and which does it skip? Not every kind is required; mark each skip as deliberate or accidental. (`plot-kinds-of-promises`)
- `plot.promises.03` Does the character promise show what the character wants, what they need, and why they cannot have it yet? (`plot-kinds-of-promises`)
- `plot.progress.01` Name the kind of progress the story measures (information, relationship, skill, distance, or another) and check that the climax resolves that kind. (`plot-types-of-progress`)
- `plot.progress.02` With several threads, name the soul of the story, the thread that drives the ending, and check that the climax turns on it and not on the trappings. (`plot-types-of-progress`)
- `plot.archetypes.01` Name the archetypes the story layers, and which one carries the Big P Plot. (`plot-archetypes`)
- `plot.archetypes.02` For each arc, has the story decided whether it heads for success or failure, and promised accordingly? (`plot-archetypes`)
- `character.scales.01` Place the character low, middle, or high on proactive, relatable, and capable, per domain where it matters. (`character-proactive-relatable-capable`)
- `character.motivation.01` Can you name what the character wants, why they cannot have it, what they need, and what they must sacrifice? (`character-motivation-discovery-questions`)
- `character.weakness.01` For each weakness, is it a flaw, a restriction, or a limitation, and is it handled that way: an arc for a flaw, pressure scenes for a restriction, ingenuity for a limitation? (`character-flaws-restrictions-limitations`)
- `magic.hardsoft.01` For each magical element, could a reader predict what it will do and what it cannot do? Place each element separately. (`magic-hard-and-soft`)
- `worldbuilding.ideas.02` For each setting idea, is there a character or plot idea that presses on it? (`worldbuilding-idea-intersection`)
- `worldbuilding.ideas.03` Is any idea just sitting there, affecting nothing else? Either connect it or save it for another book. (`worldbuilding-idea-intersection`)
- `scene.pov.01` Does the viewpoint mode fit the cast size and the information the story needs to withhold? (`viewpoint-and-tense`)
<!-- generated:checks:end -->
