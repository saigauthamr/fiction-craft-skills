---
name: prose-ai-tells
metadata:
  type: other
description: >
  Use when drafting fiction or asked to humanize, de-slop, or check machine-sounding prose. Detects and avoids over-explanation, stock rhythms, stilted dialogue, and narration that states the subtext.
---

# Prose AI Tells

A model writes the choice that fits the widest range of readers and scenes. A human writer chooses for one reader and one scene, so their choices are uneven and specific. Every pattern here is a default choice, a way of sounding finished without adding anything.

Two rules follow. Every sentence you keep must give the reader something new. A tell counts in proportion to how rarely a careful writer would do it on purpose, so a few patterns justify an edit on one sighting and the rest need company from other tells in the same passage.

Taking the tells out makes prose clean, not good. A passage with none of these patterns can still have no mind in it, no detail that belongs to it, and one temperature throughout. For what to put in, load `prose-craft`.

The full list, with fiction examples, is in `patterns.md` next to this file. Load it for a detection pass or when you need an example.

## Avoid mode (while drafting)

Keep these out of new prose from the start:

1. **Not X but Y.** Do not deny something nobody claimed so the real thing sounds bigger. Say the real thing.
2. **Interpretive closers.** Do not end a beat or a scene with a line that explains what it meant.
3. **Aphorisms in the narration.** Do not hand the reader a wise saying in place of the specific moment.
4. **Narrated significance.** Do not announce that a moment mattered ("little did she know"). Show the consequence.
5. **Forced triads.** Do not list in threes unless there are three.
6. **Same-subject runs.** Do not start four sentences in a row with the same word out of habit.
7. **Reaction riders.** Do not bolt a phrase onto an action to explain it ("..., his silence speaking volumes").
8. **Stacked hedges.** Do not soften every perception with seemed, almost, somehow, and a kind of.
9. **Named emotion after a shown one.** If the gesture shows the feeling, do not add a sentence that names it. Avoid "a flicker of" and "a mix of".
10. **Dialogue that states the subtext.** Let the line carry the feeling without naming it.
11. **Wrapper text.** Deliver the prose. No greeting, no framing line, no offer to continue.
12. **Description by denial.** Do not describe a thing by what it did not do or was not. Say what happened.
13. **Hollow depth.** Do not write a line that sounds meaningful and states nothing ("something shifted between them"). Say what changed.
14. **Reflex comparisons.** Do not reach for "like a", "as if", or "the way a" where the literal sentence would do.

Avoiding one habit often produces its nearest cousin: a named emotion becomes a tight chest, a cut explanation becomes a comparison, a banned phrase becomes its synonym. Replace a default with the specific thing, not with the next default.

## Detect mode (review and revise)

1. Read the whole passage once before marking anything.
2. Mark each tell. Look at paragraph shape, not only sentences: three parallel beats, or the same closer after every scene, is the same tell at a larger scale.
3. Report each finding with the quoted text, where it is, the pattern, and a suggested fix. Report only what you would act on. If you looked at something and decided it is fine, leave it out of the list; do not report a device you are keeping.
4. In review, report. In revise, apply the fix: state the point directly, merge or vary sentences, or cut the line. Keep the writer's events, characters, and facts. Do not add story facts to repair a sentence.
5. Check the result: read it aloud, then search again for the tells that survive a rewrite (not X but Y, closers, triads, repeated openings, dashes) and for the cousins a rewrite introduces (body reports, comparisons, denials). The habit counter `habits.py` in the `story-check` skill folder lists several of these with line numbers.

If the writer gives a sample of their own prose, match its sentence length, word choice, and punctuation. The sample overrides the patterns here, including the dash rule.

## When not to flag

- **Dialogue and in-world text.** A character may say anything. Flag a pattern in speech only when every character speaks in the same polished rhythm, or when the speech explains what the scene already showed.
- **Deliberate repetition.** Repeated openings used for rhythm or emphasis, and refrains.
- **A short paragraph that lands.** A one-line paragraph is a normal device. Flag it only when it restates or explains the beat before it.
- **Dashes for interruption** in dialogue, and in a writer's own style.
- **A real contrast.** Keep a "not X" when a character or the narrator corrects a belief that was actually stated or held.
- **Real uncertainty.** A hedge is fine when the point-of-view character really cannot tell.
- **Text before late 2022** and anything the writer wrote and can explain.

One tell is a hint. Several together, in one passage, are the signal. Do not rewrite a passage to remove a single weak tell.

## Checks

Each check is one pattern from `patterns.md`, with the same number. Weak patterns count only when they appear with others.

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

## Report format

```
1. "<quoted text>" (chapter or line)
   Pattern: <name>
   Fix: <what to do>
```

End with a one-line count and the two or three patterns that recur most, so the writer can watch for them in their own drafting.
