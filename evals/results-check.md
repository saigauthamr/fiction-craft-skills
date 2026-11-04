# Results: story-check

One run per scenario, Sonnet given the skill file, checked on disk. The fixture chapter plants: an echoing, tidy paired exchange; a cornered character's explanatory speech; packaged emotion ("a flicker of hope mixed with a hint of resentment"); a pride paragraph that explains; and a closing that states the meaning ("It was the moment everything changed. She understood, finally, ..."). The project's spec also contains a deliberate rule break: an unexplained sea-song that never solves anything.

| Scenario | Expected | Result |
| --- | --- | --- |
| Check report, full craft terms, "check chapter 1" | Report saved with `[open]` findings carrying check IDs; the planted problems found; the deliberate break not flagged; chapter unchanged | Pass. 8 `[open]` findings, including `prose.tells.21` (tidy pairs), `prose.tells.22` (the speech), `prose.tells.02`/`09` (the explaining ending), `prose.tells.14`; also found the beats' promised concession missing from the chapter. `magic.first.02: n/a, the sea-song is deliberate ... Not a defect.` Chapter byte-identical; the inspector counts the findings and recommends `story-revise` |
| Reader's report, no craft language, "is chapter 1 any good?" | Five plain parts, the three biggest problems, the twist test; no IDs or craft terms; no file | Pass. Found every planted problem in plain words, praised the sea-song as "a good quiet hook", caught the plan mismatch, guessed the secret at about 60 percent and named the clue; folder unchanged |

Fixed after the run: one continuity finding borrowed an unrelated framework ID. The skill now gives continuity and plan mismatches their own labels (`continuity`, `plan`).

New in this ticket: `prose-ai-tells` patterns 21 (lines that answer each other in tidy pairs) and 22 (a cornered character explains their position in a tidy speech), with original examples, mapped to drafting and checking.
