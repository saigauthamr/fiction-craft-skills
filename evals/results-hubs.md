# Eval results: knowledge hubs, with and without the skills

Six realistic prompts, one per area, each answered twice: once by an agent given the hub and the child skills it points to, once by an agent with no skills and no tools. One run per condition, Sonnet. Scored by reading; this is a judgment, not a measurement.

| Prompt | Without skills | With skills | What the skills added |
| --- | --- | --- | --- |
| A flat villain (character) | Good generic advice: give him a reason, a contradiction, a want of his own, competence | Same ground, organized by the three scales (find his lowest one), plus the villain's fall pattern and a check that he changes the plot when the hero is absent | **Clear.** A diagnostic and a pattern the baseline lacked |
| New power at the climax feels like a cheat (magic) | Already names the First Law and gives sound fixes | Same law and fixes, plus "over-seed then trim", the point that a surprise rescue suits the early book and not the final third, and a test using only the chapters before the climax | **Modest.** The baseline knows this material |
| Chapter one explains the whole empire (worldbuilding) | Good: start with a person, one fact per scene, spread the rest | Names the hollow iceberg, a two-part test, a first-chapter audit (count the new names), and notes a dense opening can be a deliberate choice | **Modest** |
| Beta readers guessed the twist (plot) | Good: find what gave it away, add a competing explanation, bury clues | Adds a target (readers should guess about a page before the reveal), clue-placement techniques tied to viewpoint attention, the promise-and-wish alternative, and the warning that turning foreshadowing down is harder than up | **Moderate to clear** |
| Outline killed my interest, pantsing wanders (foundations) | Landmarks, plan destinations and discover routes | Nearly the same, plus a guard against reworking the opening, heavier-revision warning, and a tip for many viewpoints | **Small** |
| Six viewpoint characters: person and tense (scene craft) | Rotating third limited, past tense; treats omniscient as risky | Same recommendation, but treats omniscient as a real option and distinguishes mystery from suspense under it; strict on the page once limited is chosen | **Small to moderate** |

## Reading

- The skills do not win on knowledge on well-known craft questions. The baseline already gives sound advice and, for magic, already knows the First Law by name.
- They win on **specific, runnable checks and patterns** (the three-scale diagnostic, the guess-timing target, the first-chapter audit) and on reducing generic advice.
- The result is consistent with the earlier plot, setup, grill, and router evals: the clearest gains come where a skill gives the writer something to do, not something to know.

## Limits

- One run per condition, one model, six prompts out of roughly seventy written. Most hub eval prompts have not been run.
- The agents were handed the skill files. Whether a real agent loads the right one from a plain request is covered separately, and depends on the routing table in the project's instructions file.
- Scored by the maintainer reading the answers. A blind, scripted score would be stronger.
