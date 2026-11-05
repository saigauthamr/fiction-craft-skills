---
name: story-adopt
compatibility: Needs Python 3 (standard library only) to run the bundled script. Install the whole skill set together; some skills read sibling skill folders.
metadata:
  type: workflow
description: >
  Use to bring existing chapters, notes, Word files, spreadsheets, or another writing tool's project into this layout. Shows an import plan, preserves originals and provenance, resumes safely, and proposes facts for approval.
---

# Adopt

Bring a writer's existing material into a Story project. The writer's files are the source of truth. You organize copies and propose facts; they decide what is true. Adopt does not decide how the writer and the AI split the work: `story-onboard` does that afterward.

## Rules that never bend

- **Originals are never modified, moved, or deleted.** Everything is copied or converted into new files.
- **Show the plan and wait for approval** before anything is written. A "looks fine" is approval; silence is not.
- **Nothing you mine is canon.** Proposed facts wait in a queue until the writer confirms each one.
- **Follow the project's own conventions.** If the instructions file names a place or pattern for something (open questions, chapter files, voice files), use it. Never create a second register or a competing layout.

## Steps

1. **Plan.** Run the script next to this file, with its full path; do not `cd`. Nothing is written.

   `python3 adopt.py plan <project-folder> --json <plan-file>`

   Put the plan file outside the project. Read the plan to the writer in plain words: what will be created and where, what already exists, what is left in place and why. Unsupported formats (old `.doc`, PDFs, Scrivener projects) are never touched; ask the writer to export them to `.docx` or `.txt` if they want them in. Point out anything the plan marks as already imported, changed since it was last imported, or sharing a name with another file.
2. **Approval.** Ask whether to go ahead. The writer may drop items or change a destination; edit the plan file's `items` to match (for example, to follow a chapter-naming pattern their instructions specify). Do not apply until they agree.
3. **Apply.**

   `python3 adopt.py apply <project-folder> <plan-file> --yes`

   Report what the script printed. Exit code 5 means some items failed and the rest were imported: name each failure and its reason, and say that re-running Adopt retries only those. Exit code 3 means an existing file changed: stop and tell the writer exactly which.
4. **Mine facts.** The script converts and files; you read what was imported (chapters in `work/drafts/`, notes in `work/brainstorm/imported/`) and propose facts. Put every proposal in the project's own register if it names one, otherwise in `work/brainstorm/adopt-facts.md`, grouped by the page each fact would go to. One line per fact:

   `- [pending major] (established) <the fact, in the writer's words as far as possible>. Source: <file>, "<quote of fifteen words or fewer>". Goes to: kb/characters/<name>.md`

   - **Major or minor.** Major: anything about plot, rules, motive, relationships, or the timeline. Minor: texture, background, names of unimportant things.
   - **What kind of statement it is.** This matters most:
     - `(established)`: the narrative states it as true.
     - `(claimed by <who>)`: a character says or believes it. A claim is not a fact about the world. A character can lie or be wrong, so never file a claim as established.
     - `(planned)`: the writer's notes say it, but no chapter shows it yet.
   - **Only what the text supports.** Do not fill gaps. A guess about someone's job, family, or past is not a fact; leave it out and ask the writer if it matters.
   - **Contradictions.** When sources disagree, record one line that names both versions and both sources, starting `[pending major] conflict:`. Never pick one yourself.
5. **Review with the writer.** Walk through the queue, most important first. For each line the writer says confirm, correct, or drop.
   - On confirm or correct: write the fact into its `kb/` page and remove the line from the queue.
   - On drop: change the line to start with `[rejected]` and keep it, so it is never proposed again.

   Imported spreadsheet tables that need your confirmation carry a "Status: needs review" line, and nothing else is marked; `python3 adopt.py review <project-folder>` lists them. Delete that line only when the writer has confirmed the table; trust is the default, so nothing replaces it. Never confirm on the writer's behalf.
6. **Hand back.** Say what exists now and hand off to `story-onboard`, which sets up how the writer wants to work. If there are chapters but no spec, mention that a spec and beats can be worked out from them (below).

## Optional: a spec and beats from existing chapters

Offer this after an import when the writer has chapters but no plan. Ask first.

1. Read every imported chapter and any notes. Summarize each chapter in a paragraph: who is in it, what happens, what changes. These become that chapter's beats.
2. Propose a spec in the sections `story-plan` uses: premise, promises, characters, rules of the world, progress, arcs, ending, open questions. Mark each line as **stated in the text** (with the chapter and a short quote) or **inferred**.
3. Do not invent an ending. An unwritten ending is an open question.
4. Confirm one section at a time. Save nothing unconfirmed.
5. Save the confirmed spec to `work/spec/spec.md` and the summaries as beats files in `work/beats/`, one per chapter, each marked "reconstructed from the draft".

## Chapter cards (long stories)

When the import brings in five or more chapters, offer to build a card for each (see Chapter cards in `story-continue`), so later work can read the story in tiers. Cards are derived and never change a chapter. Ask first.

## An established project

If the plan shows a populated `kb/`, the project already exists. The plan may have nothing to import; applying it then only records the adoption in `work/adopt/provenance.md`, which lets `story-onboard` set the project up. Knowledge-base pages, style files, the open-questions register, tool folders, and git history are left alone. An existing `work/outline/` counts as the project's beats; do not move it.

## What you tell the writer at the end

Only what the script printed and what you can see on disk: how many items were imported and where, what failed and why, what was left in place, what is waiting in the fact queue, any contradictions, and that the originals are exactly as they were.
