---
name: scene-dialogue-behavior
metadata:
  type: framework
description: >
  Use when a dialogue scene reads like a transcript, characters take orderly turns, people nod and sip between every line, or a meeting, interview, or lab scene is all talk and props. Separates action that changes the next beat from decorative and procedural motion, and says where a beat belongs.
---

# Dialogue and Behavior

Dialogue is people under pressure, not information sorted by speaker. A scene is not alive just because hands move or cups and files are handled. The useful question is whether a character's action or reaction reveals what they want, shows the last line landing, changes their next move, or changes the situation.

## Three kinds of action

1. **Functional action** comes from what the character wants right now and changes how the exchange goes. It can expose concealment, hesitation, status, or expertise; claim or give up space; cut off access to an object or person; make a lie harder to keep up; force the other person to change their next question; or have a physical or social consequence. The test: **the reaction changes the next beat.**
2. **Decorative action** is motion with no meaning specific to this scene: a smile, frown, nod, sip, or look away that any character could do without affecting anything. It is not forbidden. It is weak as a repeated speaker tag or as proof that a static scene is moving.
3. **Procedural action** performs the task: opening a file, reading a result, moving equipment. It can be necessary and accurate, and a scene made only of procedure can still be socially dead. Tie it to pressure: who rushes, hesitates, protects something, hides a result, challenges an assumption, or notices a mistake.

## Reading an exchange

Read it as a chain, at the level of the exchange and not line by line:

- the speaker has a local goal
- they choose what to say, leave out, soften, or distort for this listener
- the listener hears it through a different goal and a different amount of knowledge
- they control the reply, or fail to
- the reply changes the next line, action, or tactic

The effect may come late, or stay unresolved. A believable reply may evade, test, bargain, redirect, misunderstand, delay, or answer only the safest part.

## Where a beat belongs

Put an action beat where something changes: new information lands, a private fact is nearly exposed, someone lies or changes their story, status or control shifts, someone decides whether to comply, evidence contradicts a favored explanation, composure weakens, or the relationship turns warmer, colder, or more dangerous. The beat can be small. Make it specific to this person, this pressure, and this place.

## Do not overcorrect

- Action density is not a goal. Do not spread beats evenly, and do not give every line its own gesture, tone label, and inner reaction.
- Rapid dialogue can stay untagged when the voices, positions, and pressure are clear.
- An emotion label or a gesture on every line is not a repair. "Angrily" can clarify delivery, but it does not show what the anger makes the character do.
- A plain "He said nothing" is a legitimate sentence. It needs no gesture, motive, or consequence added to be allowed.
- When the dialogue or action already carries the response, do not add a label saying it answered.
- If a scene is meant to leave something unresolved, leave it. Do not invent an explanation to close the exchange.
- Keep the viewpoint selective. Do not cut to every participant for a reaction; let the viewpoint character notice what they would under this pressure, misread some of it, and miss the rest.

## Checks

- `scene.dialogue.01` For each action beat in a sustained exchange, does the reaction change the next line, tactic, or situation? If not, it is decorative or procedural.
- `scene.dialogue.02` Are beats placed where something changes (information lands, a lie, a shift in power, a decision) and not spread evenly or attached to every line?
- `scene.dialogue.03` Is any procedural action (opening, reading, moving things) connected to human pressure, or is the scene static with props?
- `scene.dialogue.04` Was a flat exchange "fixed" by adding emotion labels or a gesture to every line? Untagged rapid dialogue and plain stated silence are fine when voices and pressure are clear.
- `scene.dialogue.05` Does the viewpoint character notice only what they would under this pressure, instead of the scene cutting to every participant's reaction?

## Cautions and exceptions

- Comic, cozy, and ritual exchanges can run in deliberately tidy turns. Keep that when the scene is built on the rhythm.
- This is a judgment about what a beat does, not a list of banned gestures. Replacing every "did not answer" with a smile or a turn of the head repeats the same mechanical habit.
- For stiff or staged lines, see `prose-ai-tells` (dialogue patterns). For planning what each speaker wants before drafting, see `character-floating-outline-for-dialogue`.
