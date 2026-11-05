---
name: story-next
compatibility: Needs Python 3 (standard library only) to run the bundled script. Install the whole skill set together; some skills read sibling skill folders.
metadata:
  type: router
description: >
  Use when a writer asks what to do next, where to start, or says they are stuck. Inspects project state and ownership, recommends one available next step, and stops without starting it.
---

# Story next

Recommends one next step. The inspector works out the step from the project's files and settings; your job is to explain it in plain words and hand off. You never start the step yourself.

A specific request ("write the next scene", "check chapter 4") is not a question for this skill. It goes straight to the skill that does that job.

## Steps

1. **Run the inspector** next to this file, with its full path and the project folder; do not `cd`. Read its `next_step`, `next_skill`, `next_owner`, and `next_reason` lines, and the settings lines.
2. **Ask only what the files can't tell you**, at most two or three short questions, and only if the answer would change the recommendation. For example, whether there is writing somewhere outside this folder. Most of the time, ask nothing.
3. **Recommend** in this shape, using the craft language the settings name:

   > Recommended: <the step, in plain words>
   > Why: <the reason, from the inspector's facts, in one line>
   > First step: <what happens next, and who does it>

4. **Stop.** Do not start the step. Offer to hand off if the writer wants.

## Fitting the recommendation to who owns the step

The inspector's `next_owner` line says who acts.

- `ai`: offer to run `next_skill`.
- `writer`: the step is the writer's own work. Say what they would do and how the library supports it, for example: "Write chapter 3 from its beats. When it's done, ask me to check it." Never offer to do a stage the writer owns.
- `alternate`: the next scene is whoever's turn it is; say so.
- `writer-decides`: the step is a decision only the writer can make. Lay out what needs deciding (the pending facts, the chapters awaiting check-in) as a short numbered list with a recommended answer each, and wait.

## Special cases

- **Not set up, or set up by an earlier version** (`setup` is `none`, `malformed`, `duplicate`, or starts with `v1`): recommend `story-onboard`. For a `v1` setup, also say in one line how the project currently works, from its settings lines.
- **`conflicting`**: the settings in `AGENTS.md` are used. Mention in one line that `CLAUDE.md` also has a block, and that `story-onboard` can tidy it up. Then make the recommendation as usual.
- **Design complete** (design-only projects): say the design is approved and finished, and offer `story-worldbuild`, `story-cast`, or `story-plan` to refine it. Never suggest drafting.
- **The recommended skill is not installed** (`next_reason` says so): say so plainly, and offer the nearest installed skill or a plain next action. Never hand off to a skill that is not installed.

## Rules

- One recommendation. Mention an alternative only if the writer's own words point to it.
- If `promises_oldest_unpaid` names a promise and the step is to plan or draft, add one line naming it in plain words and how long it has waited. Skip it otherwise.
- Use the inspector's facts; do not guess at things the files can't show.
- Change nothing in the project.
