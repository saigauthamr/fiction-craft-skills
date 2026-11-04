# Eval results: prose-ai-tells (detect pass, review mode)

Run during ticket 08. Sonnet, one run per condition. "With skill" agents were given the skill file. "Without" agents had no tools and no skill.

## ai-tells-01: planted passage (nine planted tells)

| Condition | Result |
| --- | --- |
| With skill | 9 of 9 found. Each had the quoted text, a pattern name, and a fix. Kept the one good line ("Her brother's bed was made, his boots gone from the hook"). Did not rewrite the passage. Noticed a real contradiction ("It wasn't the cold" when the cottage is then called cold). |
| Without skill | 9 of 9 found. Also added craft opinions that are not machine tells: the scene is short, sentences are uniform, no surprising detail. |

**Reading:** detection of obvious planted tells does not separate the two conditions. Models already know these habits.

## ai-tells-02: clean passage (four deliberate devices that must not be flagged)

| Condition | Result |
| --- | --- |
| Without skill | **10 findings.** Flagged all four devices (the interruption dash, the counted horn, the parallel "once to you and once to the harbor", the closing one-line paragraph) and advised "roughening" the prose. |
| With skill, first run | "No firm tells" and three weak notes, each marked optional or "probably keep". No rewrite demanded. But it listed the closing line, a protected device. |
| With skill, after tightening | **2 weak notes, 0 strong.** No rewrite demanded. The closing line moved to "checked and found clean". One note was on a quip in dialogue (and it said not to change it); one on a possible accidental echo of "twice", which is a fair small observation. |

**Reading:** the skill's value is restraint, not detection. It cut false positives from 10 findings to 2 weak notes and stopped recommending that clean prose be roughened.

## Against the criteria

- Catches planted tells: **met** (9 of 9), though the baseline does too.
- Leaves the clean sample alone: **partially met.** No strong findings and no rewrites called for, but two weak notes against a bar of at most one. I did not change the bar after seeing the result. See the open question on ticket 09.

## Limits

- One run per condition, one model, short passages.
- Detect mode only. Avoid mode (steering a draft away from these habits) was not tested. It needs the Draft workflow (ticket 28).
- The tightening was made after the first clean run and tested once. Tuning a skill against the passage it was just scored on risks overfitting; a fresh clean passage should be tried at the slice review.
- The fiction-specific additions are not in the skill. They were proposals reviewed separately by the maintainer and then added as patterns 13 to 20.

## After owner decisions: fiction habits added (patterns 13 to 20)

| Eval | Result |
| --- | --- |
| ai-tells-03, planted fiction habits | **Pass.** Found patterns 13, 14, and 15 as strong, marked 16 and 17 as weak but counting because they came together, gave a fix for each, and did not rewrite. |
| ai-tells-04, fresh clean passage | **Pass.** Zero tells. It named the deliberate "He closed... He closed... He closed" repetition, the interrupted "Da—", the real count, and the one-line closer as devices and left them alone. This meets the original bar of at most one weak note, so the bar was kept unchanged. |

One run each. The fresh clean passage is a single test of overfitting, not proof.
