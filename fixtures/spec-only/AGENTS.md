# Project instructions

<!-- story-project:start v2 -->
## Story project

### How we work (You write, AI checks)

<!-- story-settings:start -->
| setting | value |
| --- | --- |
| preset | you-write-ai-checks |
| plan | writer |
| draft | writer |
| revise | writer |
| craft-language | full |
| check-in | three-chapters |
<!-- story-settings:end -->

You plan; you draft; you revise. The AI checks any chapter on request. Only you make story facts canon.

### Where things go

Facts the story has committed to live in `kb/`. Working documents live in `work/`. If this file names other places for any of these, those take priority.

- `kb/characters/`, `kb/world/`, `kb/timeline/`, `kb/canon/`: settled story facts, one topic per file
- `kb/styles/`: voice and style files; `kb/samples/`: prose samples
- `kb/issues/`: problems and open questions that span chapters
- `kb/vocab.md`: canonical story terms, aliases, and terms to avoid
- `work/spec/`, `work/beats/`: the approved spec and chapter beats, saved only after the writer approves them
- `work/drafts/`: chapters; `work/critique-reports/`: check reports; `work/brainstorm/`: undecided notes

Trust is the default: anything unmarked is trusted, and only untrusted material carries a marker. When the writer approves something, its marker is removed, and nothing records who approved it or when.

- A chapter the AI drafted starts with `<!-- status: draft -->`, `<!-- status: awaiting check-in -->`, or `<!-- status: needs revision: <reason> -->`. The writer's approval removes the line. A chapter with no status line is trusted, including every chapter the writer wrote.
- A fact proposed but not yet approved is a list item starting `[pending major]` or `[pending minor]`. Approval moves it into `kb/`, unmarked, and removes it from the list. A fact the writer turned down starts `[rejected]` and is never proposed again. Nothing goes into `kb/` until the writer approves it.
- Each open finding in a check report starts `[open]`. A fixed finding is deleted. One kept on purpose becomes `[resolved] declined: <reason>`.

### Skills for story work

For the requests below, load the named skill before answering. For this story they take priority over generic skills for the same job. Every skill reads the settings above.

| The writer... | Use |
| --- | --- |
| asks what to do next, where to start, or says they are stuck | `story-next` |
| wants to set up the project, or change how we work (who writes, how much craft talk, check-ins) | `story-onboard` |
| has existing chapters, notes, or spreadsheets to bring in | `story-adopt` |
| wants the idea, premise, world, or a character questioned, sharpened, or decided ("grill me", "help me design") | `story-develop` |
| wants a spec, chapter beats, or a plot plan | `story-plan` |
| wants a chapter or scene written, or says "go" | `story-draft` |
| wants a chapter checked or reviewed, or asks whether it is any good | `story-check` |
| wants a chapter revised, or a check report's findings fixed | `story-revise` |
| wants to change the story in plain words ("darker", "slower", "I don't like this character") | `story-steer` |
| wants the next chapter of a serial written from what is already on the page | `story-continue` |
| wants to learn a craft technique, without writing anything | `story-learn` |
| wants magic, powers, or the rules of the world designed or stress-tested | `story-worldbuild` |
| wants characters, a villain, or relationships designed | `story-cast` |
| wants to choose how the story sounds | `story-voice` |
| asks about plot, pacing, a dragging middle, an opening, or a payoff | `plot` |
| asks about a character: flat, passive, villain, motivation, arc, or writing someone they have not lived | `character` |
| asks about magic, worldbuilding, naming, or how much of the world to explain | `magic-worldbuilding` |
| asks about outlining versus discovery writing, feedback, revision, or early readers | `foundations` |
| asks how a scene is built or told: point of view, tense, showing versus telling, scene structure | `scene-craft` |
| asks to find or fix prose that sounds machine-written | `prose-ai-tells` |
<!-- story-project:end -->
