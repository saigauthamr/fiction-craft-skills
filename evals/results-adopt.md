# Results: story-adopt (v2)

Script behavior is covered by `scripts/test_story_adopt.py` (24 tests): the first build's import and conversion tests, plus re-run after a source changes (new version beside the old), partial failure (temp files, nothing half written, failure reported, retried on re-run), ledger method and status, an established project where apply writes only the ledger, and onboarding succeeding afterward.

Agent eval: one run, Sonnet given the skill file, scripted writer, checked on disk.

| Scenario | Expected | Result |
| --- | --- | --- |
| A chapter where a character lies ("I've never been to the hidden island") while the narrative shows wet outer-reef salt on his boots, plus notes that contradict the chapter (Ines is 24 in the chapter, 30 in the notes; the notes say Tomas ferries surveyors to the island) | Plan first, nothing written; after "yes", import; facts proposed in a queue, none in `kb/`; the lie tagged as a claim; contradictions recorded with both sources and no side picked; planned facts tagged | Pass. Folder unchanged before "yes". 11 proposals (7 major, 4 minor) in `work/brainstorm/adopt-facts.md`; the lie is `(claimed by Tomas)`; two `conflict:` lines; three `(planned)` facts; no `kb/` folder; originals unchanged; the inspector counts the queue and recommends `story-onboard` |

Flaw noticed: one proposal names a destination outside the layout (`kb/plot/open-threads.md`). Harmless while it waits in the queue; worth a line in the skill if it recurs.
