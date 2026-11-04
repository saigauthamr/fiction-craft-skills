# Results: story-plan

One run per scenario, Sonnet given the skill file, scripted writer, checked on disk.

| Scenario | Expected | Result |
| --- | --- | --- |
| AI owns planning, full craft terms, an existing spec with a deliberate rule break (an unexplained sea-song that never solves anything), "plan the first two chapters" | Beats shown, nothing saved before approval; turn kept in its own writer's-note field; inferred lines marked; checks recorded per chapter with specific evidence or `n/a`; the deliberate break respected | Pass. Nothing written before approval. It caught a real contradiction in the fixture (a permanent marker that moves) and asked instead of guessing. After approval: two beats files, a promise ledger with three payoff gaps listed and the sea-song marked deliberate, and a "Changes" note on the spec. Chapter 1 records 13 checks, each with a note specific to this story; `magic.first.02: n/a, the sea-song is deliberate and never solves problems` (negative eval passed) |
| Writer owns planning, empty project, "can you plan chapter one for me?" | Coaching and questions; no AI-written plan | Pass. Refused to write the plan, asked the questions the plan needs, offered to record the writer's own words; nothing written |

Substance (judged by reading, not by a separate grader agent): the recorded evidence notes name this story's events and characters; none would fit any story. Size note: with 114 compiled checks across its two operations, `story-plan` is about 3,400 words.
