# Results: story-draft (core)

One run per scenario, Sonnet given the skill file, checked on disk.

| Scenario | Expected | Result |
| --- | --- | --- |
| "Write the next scene", AI owns planning and drafting, one accepted chapter and no spec or beats | Draft with an assumptions list, not a redirect; status line; new facts queued, not in `kb/` | Pass. Chapter 2 (453 words) with `<!-- status: draft -->`; assumptions listed; one major and four minor facts in `work/brainstorm/pending-facts.md`; `kb/` and chapter 1 unchanged |
| "Write chapter one for me", writer owns drafting, beats exist | A scene list and questions, no prose | Pass. Scene list from the beats plus questions; folder unchanged. Wording fixed afterward: it offered to switch the drafting setting itself; the skill now sends settings changes to `story-onboard` |
| "Draft chapter 1" in a project with its own rules: a voice file per part of the book, an italic dateline, a 600 to 900 word range, and a single open-questions register | Use the Part One voice file, the dateline, the length; put new facts in the project's register; create nothing parallel | Pass. 774 words, dateline first after the status line, Part One voice (no sea metaphors); four new facts appended to `kb/issues/open-questions.md`; the only other change is the chapter; the beats' "turn" note does not appear in the prose |

## Found in real use, then fixed

The owner read a chapter drafted with no beats (made from the original, which has none) and found it competent but "random": it did not move or set up the story. The skill told the AI to draft with listed assumptions and nothing more, so nothing made it decide what the chapter was for. The same run also queued new facts in a second file, though the project names one register for open and review items.

| Change | Check |
| --- | --- |
| With no beats and the AI planning, `story-draft` writes a short visible working plan first: what the chapter changes, what it sets up or pays off, the main scenes, the hook out, drawn from the project's timeline, spec, ledger, open questions, and the previous chapter's ending. It asks one question instead of guessing when the project does not say what comes next | Two runs from a fresh copy of the owner's original. Both saved a working plan from the timeline's October 1906 row naming what the chapter sets up. Not a verdict on quality: the owner reads and judges |
| Pending facts go into the project's single register when it names one; the fallback file is used only when it names none (`story-draft`, `story-continue`; `story-adopt` already did). The lint now fails a skill that names a fallback file without saying to use the project's register first | The first run wrote a second register. The rerun appended five pending facts to `kb/issues/open-questions.md` and created no new register |
| With the owner's own beats (chapter 2 of the director project) | Followed all three beat scenes in order and ended on the beats' hook out; one self-check pass; one major and six minor facts queued for approval; `kb/` and chapter 1 unchanged |

## Implicit trust

Principle (owner's): trust is the default; only untrusted material carries a marker, and approving something removes the marker and leaves no record. Applied to chapter status lines (no `accepted` marker; the AI deletes the line on the writer's word), check findings (a fixed finding is deleted), imported-file banners (one origin comment, no date, no visible banner), and vocabulary entries (no "where it was decided"). The inspector treats an unmarked chapter, and the first build's `accepted` line, as trusted: it is never recommended for a check.

| Check | Result |
| --- | --- |
| Script tests: an unmarked chapter is trusted and not recommended for a check; a chapter marked `draft` still is; a first-build `accepted` line is read as trusted; a finding kept on purpose is settled | Pass (`test_story_block.py`) |
| The owner's real director project, before and after | Before: the Router said "check the latest draft" about the owner's own chapter 1. After: it counts that chapter as trusted and recommends drafting chapter 2 from the owner's beats |
| Agent: two AI-drafted chapters awaiting check-in, open findings, one major and one minor pending fact and one rejected; "Chapters 1 and 2 are good, I accept both. Yes to the lamp bargain and yes to Hobb selling oil." | Pass. Both status lines deleted (chapters trusted); both facts written to `kb/` as plain one-liners and removed from the queue; the rejected line kept; open findings deleted; no `accepted`, date, or approval note anywhere. The report files were left as empty shells; the skill now deletes a report when its last finding goes |
