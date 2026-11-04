# Eval results: plot hub (tracer run)

Run during ticket 04. One run per condition, same model (Sonnet) both ways. "With" runs were given the hub file and told to read the child skills it points to. "Without" runs had no tools and no skill access. Scored by hand against the "must show" lists in `plot.md`.

| Eval | Without skills | With skills |
| --- | --- | --- |
| plot-01 (the drag) | 1 of 4, loosely. Generic advice (static stakes, midpoint shift, passive protagonist). Noted the brother had dropped out of mind. No promise/progress framing, no revised promise, no progress type. | 4 of 4. Framed as promise versus progress, checked the dropped thread, fixed by adding a promise and revising the early one, named information and relationship progress with signposts. |
| plot-02 (the opening) | About 2 to 3 of 4, loosely. Said to make a promise, asked what the detective wants, handled tone through voice. Did not list the kinds of promise or check which were missing. | 4 of 4. Listed tone, plot, character, series, checked the opening against each, said not all are required, added the stealth thesis paragraph and the revise-last advice. |

## Reading the results

- plot-01 separates the conditions clearly.
- plot-02 separates them less: the baseline already gives sound opening advice. The skill's added value there is structure and naming (a checklist of the kinds of promise, the "revise last" rule). If this eval is meant to catch a skill that adds nothing, tighten it to require the explicit list of kinds.
- The with-skills answers separated their own advice from the skills' ("the advice on cozy-mystery conventions is my own, not from the skills"), which is the behavior we want.

## Limits of this run

- One run per condition, so no variance estimate.
- The skills were supplied by explicit file reads. This does **not** test whether a real agent's description matching loads the hub from a plain request. That needs the skills installed in an agent and is part of the slice review gate (ticket 09).
- Four of the six plot evals plus the router eval have not been run yet (plot-03 through plot-06, router-plot-01).
