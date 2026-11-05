---
name: story-edits
compatibility: Needs Python 3 (standard library only) to run the bundled script. Install the whole skill set together; some skills read sibling skill folders.
metadata:
  type: workflow
description: >
  Use after the writer has edited a chapter the AI drafted and wants the AI to learn from those edits. Compares the delivered text with the edited chapter, groups the changes by what they did, asks about the ones it cannot explain, and saves approved lessons to the voice file.
---

# Story edits

The writer edited a chapter you drafted. Their changes are the clearest statement of taste they will give you. Your job is to read them, understand what each one was for, and carry the confirmed lessons into every later chapter. You never change the chapter.

## Before you start

1. **Read the settings** (who drafts, the craft language) and the project's own conventions, especially where its voice files live. If the project has no voice file, ask where lessons should go before proposing any.
2. **Find the chapters.** The inspector's `chapters_edited_since_delivery` line lists them; or the writer names one. Each needs a copy in `work/drafts/_delivered/`. With none, say there is nothing to compare and stop.
3. **Run `diff_chapter.py`** from this skill's folder with its full path, giving the delivered copy and then the current chapter. Do not `cd`. It reports kept, rewritten, cut, and added paragraphs with line numbers. If it says `unchanged`, delete the delivered copy, say the chapter came through untouched, and stop.

## Reading the changes

Read each changed paragraph beside the one it replaced. Then sort the changes by what they did, not by where they are. Typical groups:

- **Cut explanation**: a line that said what a beat meant, named a feeling, or restated the scene.
- **Tightened or loosened dialogue**: shorter speeches, more evasion, a different register for a speaker.
- **Concrete detail**: something specific added, or something generic replaced.
- **Rhythm and length**: sentences joined or split, a scene shortened or extended.
- **Word choice and voice**: a word or phrase swapped for the writer's own.
- **Story content**: a fact, name, order of events, or outcome changed.
- **Small fixes**: typos and punctuation. Do not draw lessons from these, and do not ask about them.

Pair a cut with an addition only when the diff reports them as one rewritten paragraph, or they sit in the same place. A cut in one scene and an addition in another are two separate changes, and you do not know they are related.

Before asking anything, decide which groups you can explain. A group explains itself when at least two changes point the same way (five cut explanations in one chapter is a preference, not an accident). A change that stands alone, with nothing else in the chapter pointing the same way, is never a lesson on its own: an added line, a rewrite, or a cut with no match. Those are exactly what to ask about, along with two changes that seem to pull in opposite directions.

## Asking

Ask at most three questions in one round, each with your best reading and a recommended answer, in the craft language the settings name. Never ask about small fixes, and never ask the writer to justify taste. Wait for the answers.

## Lessons

Turn what is now clear into short lessons. A lesson needs at least two changes pointing the same way, or the writer's confirmation of one: one line each, written as an instruction to the drafter, specific enough to act on and general enough to reuse.

- Good: "Cut the sentence after a gesture that says what the gesture meant."
- Too vague: "Be more subtle."
- Too narrow: "Remove the line about the ferry."

Mark a lesson that only applies to part of the book (one character, one phase, one kind of scene) with that scope. Show the lessons as a numbered list with the evidence for each in one short phrase, and let the writer keep, change, or drop each.

**Story content the writer changed** is theirs, so it is already decided. Offer to update the matching `kb/` page and the beats; do it only on their yes.

## Saving

When the writer has answered:

1. Add each approved lesson to the project's own voice file, one line, unmarked. Trust is the default, so approved material carries no marker and no record of who approved it or when. If the voice file already says the same thing, tighten that line instead of adding another.
2. Apply any approved `kb/` or beats updates.
3. Delete the chapter's copy in `work/drafts/_delivered/`.
4. Record each lesson the writer declined as `- [rejected] lesson: <the lesson>` in the project's single register for open items (or `work/brainstorm/pending-facts.md` only if it names none), so it is never proposed again. Add nothing else about the lessons.
5. If the chapter has a card in `work/cards/`, rewrite it from the edited chapter and stamp it (see Chapter cards in `story-continue`).

Never edit the chapter. Once the writer has answered, keep only the voice-file lines and any `[rejected]` line: no delivered copy, no diff, no note about who approved what.

## Rules

- A lesson is a pattern across changes, not a single edit. One cut is not a rule, and a lone addition is a question, not a lesson.
- Learn the writer's preferences, not your own. Never use a lesson to push a style on them.
- Do not argue about taste, and do not turn the lessons into a critique of the chapter.
- If the changes contradict a lesson already in the voice file, say so and ask which wins.
- Show no skill names and no check IDs to the writer.
