# Contributing

Issues and pull requests are welcome. Please use the issue templates if a skill did not load or produced something unhelpful.

## Before you open a pull request

Run these from the repository root; all should pass:

```
python3 -B -I scripts/compile_checks.py   # regenerate the checks compiled into the stage skills
python3 -B -I scripts/lint.py   # reports advisory size targets and growth from the measured baseline
python3 -B -I scripts/skill_sizes.py   # current words beside baseline comparison tokens
for t in scripts/test_*.py; do python3 -B -I "$t"; done
```

Size targets are advisory. Keep useful instructions even when a skill exceeds 1,500 words. The lint warns
when either the hand-written or generated portion grows by both more than 25% and more than 100 words
from `scripts/size-baseline.json`. Review that growth before resetting the baseline. To deliberately record
a new baseline, run `uv run scripts/skill_sizes.py --write-baseline --tokens`. This uses the pinned tiktoken
`cl100k_base` encoding for reproducible comparisons; these counts are not Claude billing or context usage.
Ordinary lint and word reports need only Python's standard library.

## What a skill must be

- **Self-contained.** A skill never refers to files that are not in the installed skill folder, and never to the working notes or source material it was written from.
- **In your own words.** Frameworks are restated, not quoted. At most a short, clearly attributed defining line.
- **Checkable.** A framework skill ends in a `Checks` section with stable IDs (for example `plot.promise.01`), and every check is consumed by a stage skill through `scripts/check-map.txt`.
- **Honest about exceptions.** Say when a rule does not apply. Fiction breaks its own rules on purpose.

## Changing prose guidance

Guidance that changes how drafts sound (dialogue, narration, the AI-tells patterns) ships only if a reader prefers the result in a blind read of two drafts from the same beats. Counts and rubrics are guards against known failures, not proof of quality. Include the two drafts and the reader's preference in your pull request.

## Where things are

- `skills/`: every skill, one folder each
- `scripts/`: the lint, the check compiler, the install and export scripts, and their tests
- `evals/`: test prompts and recorded results
- `fixtures/`: small sample projects the tests use
- `examples/`: before-and-after teaching cases
