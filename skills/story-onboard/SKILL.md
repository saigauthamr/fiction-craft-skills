---
name: story-onboard
compatibility: Needs Python 3 (standard library only) to run the bundled script. Install the whole skill set together; some skills read sibling skill folders.
metadata:
  type: setup
description: >
  Use to set up a story project, including "I'm not a writer; write it for me", or change stage ownership, craft language, or check-ins. Inspects existing material, offers presets, and shows the settings change for confirmation before writing.
---

# Story onboard

Sets up a Story project, or changes how one works, by asking a few questions and recording the answers in the project's instructions file. Every other story skill reads those answers. You never write anything until the writer confirms what you showed them.

## Steps

1. **Look first.** Run the inspector script in the `story-next` skill folder on the project folder, with its full path; do not `cd`. Read the project's instructions file (`AGENTS.md`, `CLAUDE.md`). Note the `setup` line and any current settings.
2. **Say what you found** in three to five plain lines: is it empty, does it hold chapters or notes, does it have story facts already, and is it set up, and how.
3. **Existing material comes first.** If the inspector reports existing material, or an established knowledge base with no setup (`setup: none` and `established_kb: True`), the writer's files must be brought in before anything else. Say so in one line and hand off to `story-adopt`. Come back here afterward.
4. **Ask one section at a time**, recommended answer first, so the writer can accept with a number or "go". Skip any section the writer has already answered in what they said.
   - **How we split the work.** Offer the presets as numbered options, one plain line each:
     1. AI writes, you direct: you make the decisions, the AI plans, drafts, and revises.
     2. AI drafts, you revise: the AI plans and drafts, you rework the prose.
     3. You outline, AI drafts: you give the plan or beats, the AI writes the prose, you revise.
     4. AI outlines, you write: the AI lays out what each chapter and scene needs, you write it, the AI checks it.
     5. You write, AI checks: you do everything, the AI questions, coaches, and checks, and never writes your prose.
     6. Design only: the AI helps you design the world, cast, and plot, and there is no prose.

     Recommend from what the writer said: "I'm not a writer" points to 1, "I write" points to 5, "I just want to build the world" points to 6. If nothing points anywhere, recommend 5 and say the AI's role can grow later.
   - **Adjust a stage?** Only if the writer wants something between the presets. The three stages are planning, drafting, and revising. Drafting can also be traded scene by scene. If a combination can't work, the setup script says which rule it breaks: explain it in plain words and offer the nearest one that works. The two rules are: no prose means no drafting and no revising, and the AI can only revise prose it drafted.
   - **How much craft talk.** No craft terms, one-line explanations, or full terms. Recommend the preset's default: none when the AI writes, full when the writer does, brief otherwise.
   - **Check-ins.** Only when the AI drafts: every chapter, every three chapters (recommended), or every part of the book.
5. **Show before writing.** Run the setup script next to this file with its full path, the folder, the chosen settings, and `--dry-run`:

   `python3 scaffold.py <folder> --preset <name> [--plan X --draft X --revise X --craft-language X --check-in X] --dry-run`

   Tell the writer, in plain words, the settings line it prints, which folders it would create, and which file it would change. Offer to show the full block. If they want changes, go back to the section that changes.
6. **Write only after a yes.** Run the same command without `--dry-run`. Report what was created and changed in two or three lines.
7. **Name the first step** in one line, from the inspector's state: usually `story-develop` for a new idea, or the step `story-next` would recommend. Do not start it.

## Changing how we work later

Run the same steps on a set-up project. State the current settings in one line, ask only what the writer wants to change, show the `--dry-run` diff, and write after a yes. Only the block changes. Story facts, plans, drafts, and every other line of the instructions file stay exactly as they are.

## First-build setups

The inspector reports `v1-director` or `v1-standard` for a project set up by an earlier version of this library.

- `v1-director` becomes "AI writes, you direct". Say so and confirm.
- `v1-standard` becomes "You write, AI checks", unless the drafts look AI-drafted (the writer used the old drafting workflow, or says so). Then ask which preset fits.

To migrate with the same meaning, use `--keep` in place of the preset options; to migrate to a different preset, pass it as usual. Show the dry run first either way.

## Problems the inspector reports

- `malformed`: say exactly what is wrong (the inspector's detail line). If the block has no end marker, the writer must fix it by hand; do not guess where it ends. Otherwise, rewriting the block with the chosen settings fixes it.
- `duplicate` or `conflicting`: explain that there is more than one block, and that `AGENTS.md` wins. With the writer's approval, re-run with `--repair`, which keeps one block and leaves a pointer in the other file.
- Exit code 3 ("existing project"): the folder has an established knowledge base and no setup. Hand off to `story-adopt`. Use `--force` only if the writer, after hearing why, insists.

## Rules

- Nothing is written before the writer confirms what you showed them.
- One section at a time; at most one question per message unless the writer asked for all of them.
- Plain words. Do not teach craft here.
- Never touch `kb/`, `work/`, or any text outside the block. The project's own rules in its instructions file stay exactly as written, and they take priority over the defaults the block describes.
