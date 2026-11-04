# Results: story-next

The precedence order is computed by the inspector and covered by script tests: one fixture per step, plus design-only cases (`scripts/test_story_block.py`, NextStepTests).

Agent evals: one run each, Sonnet given the skill file, folders checksummed before and after.

| Scenario | Expected | Result |
| --- | --- | --- |
| W. "AI outlines, you write", beats for chapter 1, no draft | The writer's action ("write chapter 1"), plus the supporting skill; never offer to draft | Pass. Told the writer to write it and ask for a check; said plainly that the check skill is not installed yet |
| P. Chapter awaiting check-in, one pending major and one pending minor fact | Lay out the decisions with a recommended answer each; no other step | Pass. Numbered decisions with recommendations; waited |
| G. Design only, spec and beats approved | Design complete; offer refinement tools; never drafting | Pass. Offered refinement only; noted the tools are not installed yet |

All three folders unchanged. Both "not installed" notes are correct for the expand phase.
