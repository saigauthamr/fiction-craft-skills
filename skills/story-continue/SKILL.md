---
name: story-continue
metadata:
  type: workflow
description: >
  Use to continue an existing story or serial from its chapters, especially without a spec or beats. Summarizes open promises, offers a next-chapter choice, then hands drafting to whoever owns it.
---

# Story continue

The story already exists. Carry it forward without breaking what is settled and without dropping what it promised.

## Steps

1. **Read the settings and the project's own rules**: who owns planning and drafting, the craft language, voice and style files, chapter naming and length, any header every chapter opens with, and where open questions live. Follow them. Load only what the task needs.
2. **Read the story so far** in tiers (below), plus the `kb/` pages that bear on the next chapter. If beats exist for the next chapter, read them and skip to step 5.
3. **Say where the story stands** in a short note: where the viewpoint characters are, what just happened, and the state of each live thread.
4. **List the open promises**: what the story set up and has not paid off, which threads went quiet, which questions are open. If the project keeps a promise ledger, start from it (the inspector's `promises` and `promises_oldest_unpaid` lines count it) and check it against the chapters, since a ledger can be out of date. The writer decides which ones the next chapter serves. Use the craft checks below, in the craft language the settings name.
5. **Propose the next chapter** in a few lines: its goal, what it advances, the main scenes, the hook out. Offer one or two real alternatives if they differ. When the writer owns planning, ask for their plan instead and offer this as a starting point only if they want it. Wait for the choice.
6. **Hand to the drafter.** Draft following `story-draft` when the AI owns drafting. When the writer drafts, give them the agreed plan as a scene list and offer a check when they are done. When drafting alternates, write only the next scene.
7. **Continuity before handing over** (when you drafted): re-read the chapter against the earlier ones and `kb/`. Fix or flag any contradiction, however small.

## Reading a long story

Once the story has five or more chapters, read it in tiers instead of loading every chapter:

1. The chapter in hand and its beats, in full.
2. The chapters just before and just after it, in full.
3. Every other chapter as its card in `work/cards/`. Open the prose only when a card is missing or stale, when the task needs the exact wording, or when a card disagrees with another source. The prose wins: correct the card from it.

Run `cards.py report <project folder>` from the `story-continue` skill folder (full path, no `cd`) to see missing and stale cards. A card that agrees with everything else is enough: do not open its chapter just to be thorough. A card points to its chapter; a fact that is only on a card is not settled.

Writing a card is housekeeping, not a fix. When you had to open a chapter because its card was missing or stale, rewrite the card from the chapter and stamp it (see Chapter cards in `story-continue`), and say so in one line. Never change a chapter to match its card.

## Chapter cards

A card is a short derived summary of one chapter, saved as `work/cards/<chapter file name>`: about 100 words in six plain lines.

- Where and when: the setting and time, and whose viewpoint.
- What happens: the events in order.
- What changed: what is true at the end that was not true at the start.
- Promises: what the chapter opened, advanced, or paid off.
- Open threads: what a later chapter must honor.
- New names and facts: anything introduced, called settled only if it is in `kb/`.

After writing or rewriting a card, stamp it with the chapter's current content hash: `cards.py stamp <project folder> <chapter file name>`. A changed chapter makes its card stale; approving a chapter, which only removes its status line, does not. Never edit a chapter to match its card. Delete the card of a chapter that no longer exists. Cards are derived, so they carry no approval marks.

## Hand-over

Where the chapter is (with `<!-- status: draft -->` first), new facts it invented, each as a `[pending major]` or `[pending minor]` line in the project's single register for open items (or `work/brainstorm/pending-facts.md` only if it names none) and never approved into `kb/`, which open promises it advanced, and anything that strains a settled fact. When the story has five or more chapters, write the chapter's card. Offer a check.

## Rules

- Do not resolve an open question the writer has not resolved.
- One chapter at a time.
- Never write facts into `kb/` without the writer's approval.

<!-- generated:checks:start -->
## Craft checks (generated)

Apply each check that fits this story. In the files you write (beats, reports, notes), record its ID with a short note of what it found in this story, or `n/a` with a reason. Never show IDs or skill names to the writer: in conversation, ask or say the substance in the craft language the settings name. A deliberate break of a framework is a valid answer, not a defect: say it is deliberate and do not push the story back toward the formula. Load the skill listed for a check's family (after the list) only when you need its full reasoning.

- `plot.ppp.02` For this stretch, name what tells the reader the story is moving toward one of those promises. A stretch with no signpost reads as a stall.
- `plot.promises.05` Does each new character, sequence, or chapter make its own small promise, and does the chapter signal it was delivered?
- `plot.progress.03` For this sequence, what does the reader think it is moving toward, and what signals tell them so?
- `character.proactive.01` What does the character want in their first scene, and does an action follow from it?
- `scene.sequel.04` Does each sequel carry something (a revelation, a joke, a relationship beat), and does its decision launch the next scene?
- `prose.craft.09` Against the earlier chapters, does this one open and close in a different way, and avoid leaning on the same devices?
- `prose.tells.13` An emotion named right after it is shown.
- `prose.tells.15` Dialogue that states its own subtext.

Skill for each check family: `plot.ppp` plot-promise-progress-payoff; `plot.promises` plot-kinds-of-promises; `plot.progress` plot-types-of-progress; `character.proactive` character-proactivity-toolkit; `scene.sequel` scene-and-sequel; `prose.craft` prose-craft; `prose.tells` prose-ai-tells.
<!-- generated:checks:end -->
